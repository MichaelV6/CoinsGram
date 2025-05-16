from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Comment.objects.select_related('author', 'coin')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action in ['update', 'partial_update']:
            return CommentCreateSerializer  # текст и coin (coin можно сделать read_only, если не нужен)
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user
        # Только автор или staff может менять
        if not (user.is_staff or instance.author == user):
            raise permissions.PermissionDenied("Можно редактировать только свои комментарии")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if not (user.is_staff or instance.author == user):
            return Response({'detail': 'Можно удалять только свои комментарии'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='coin_comments')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "coin_id", int, OpenApiParameter.QUERY, required=True,
                description="ID монеты"
            )
        ]
    )
    def coin_comments(self, request):
        coin_id = request.query_params.get('coin_id')
        if not coin_id:
            return Response({'error': 'Необходимо указать coin_id'}, status=400)
        comments = Comment.objects.filter(coin_id=coin_id)
        return Response(CommentUpdateSerializer(comments, many=True).data)
