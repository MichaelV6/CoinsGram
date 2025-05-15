from django.http import Http404
from rest_framework.views import exception_handler
from .exceptions import BaseAPIException, NotFoundError, ValidationError

def custom_exception_handler(exc, context):
    """
    Преобразует стандартные исключения Django и DRF в наши собственные исключения API
    """
    # Сначала пробуем обработать исключение стандартным обработчиком
    response = exception_handler(exc, context)
    
    # Если это уже наше исключение или было обработано DRF, возвращаем ответ
    if response is not None or isinstance(exc, BaseAPIException):
        return response
    
    # Преобразуем Django Http404 в наше NotFoundError
    if isinstance(exc, Http404):
        exc = NotFoundError()
        return exception_handler(exc, context)
    
    # Преобразуем ValidationError Django в наше APIValidationError
    if isinstance(exc, django.core.exceptions.ValidationError):
        exc = ValidationError(detail=str(exc))
        return exception_handler(exc, context)
    
    # Если что-то неизвестное, логируем и возвращаем общую ошибку
    import logging
    logger = logging.getLogger('django')
    logger.error(f"Необработанное исключение: {exc}")
    
    # Возвращаем стандартный ответ или общую ошибку сервера
    return response