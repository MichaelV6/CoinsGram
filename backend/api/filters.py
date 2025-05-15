from django_filters import rest_framework as filters
from coins.models import Coin

class CoinFilter(filters.FilterSet):
    min_price = filters.NumberFilter(
        field_name='estimated_value', lookup_expr='gte'
    )
    max_price = filters.NumberFilter(
        field_name='estimated_value', lookup_expr='lte'
    )
    tags      = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    author    = filters.NumberFilter(
        field_name='author__id'
    )

    class Meta:
        model  = Coin
        fields = ['min_price', 'max_price', 'tags', 'author']