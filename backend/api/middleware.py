from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework.views import exception_handler

from .exceptions import BaseAPIException, NotFoundError, ValidationError

import logging
logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    """
    Преобразует стандартные исключения Django/DRF в собственные
    исключения API и формирует унифицированный ответ JSON.
    """
    # Сначала пробуем штатный обработчик DRF
    response = exception_handler(exc, context)
    if response is not None:
        return response

    # Наши собственные исключения уже содержат нужный статус-код/детали
    if isinstance(exc, BaseAPIException):
        return exception_handler(exc, context)

    # 404 → NotFoundError
    if isinstance(exc, Http404):
        exc = NotFoundError()
        return exception_handler(exc, context)

    # Django ValidationError → наш ValidationError
    if isinstance(exc, DjangoValidationError):
        exc = ValidationError(detail=str(exc))
        return exception_handler(exc, context)

    # Логируем всё остальное и возвращаем 500
    logger.error("Необработанное исключение", exc_info=exc)
    return response  # response == None, DRF автоматически отдаст 500
