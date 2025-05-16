from django.http import Http404
from rest_framework.views import exception_handler
from .exceptions import BaseAPIException, NotFoundError, ValidationError

def custom_exception_handler(exc, context):
    """
    Преобразует стандартные исключения Django и DRF в наши собственные исключения API
    """

    response = exception_handler(exc, context)
    

    if response is not None or isinstance(exc, BaseAPIException):
        return response
    

    if isinstance(exc, Http404):
        exc = NotFoundError()
        return exception_handler(exc, context)
    

    if isinstance(exc, django.core.exceptions.ValidationError):
        exc = ValidationError(detail=str(exc))
        return exception_handler(exc, context)
    

    import logging
    logger = logging.getLogger('django')
    logger.error(f"Необработанное исключение: {exc}")

    return response