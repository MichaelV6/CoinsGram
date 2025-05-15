from rest_framework.exceptions import APIException
from rest_framework import status


class BaseAPIException(APIException):
    """Базовое исключение для API"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Произошла ошибка в запросе'
    default_code = 'error'


class NotFoundError(BaseAPIException):
    """Объект не найден"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Запрашиваемый объект не найден'
    default_code = 'not_found'


class ValidationError(BaseAPIException):
    """Ошибка валидации данных"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Ошибка в данных запроса'
    default_code = 'validation_error'


class PermissionDeniedError(BaseAPIException):
    """Отказ в доступе"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'У вас недостаточно прав для выполнения этого действия'
    default_code = 'permission_denied'


class FileUploadError(BaseAPIException):
    """Ошибка загрузки файла"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Ошибка при загрузке файла'
    default_code = 'file_upload_error'


class AlreadyExistsError(BaseAPIException):
    """Объект уже существует"""
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Такой объект уже существует'
    default_code = 'already_exists'


# Специфические для монет исключения
class CoinNotFoundError(NotFoundError):
    default_detail = 'Монета не найдена'
    default_code = 'coin_not_found'


class TagNotFoundError(NotFoundError):
    default_detail = 'Тег не найден'
    default_code = 'tag_not_found'


class UserNotFoundError(NotFoundError):
    default_detail = 'Пользователь не найден'
    default_code = 'user_not_found'


class UnauthorizedError(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Необходима авторизация'
    default_code = 'authentication_required'


class DuplicateFavoriteError(AlreadyExistsError):
    default_detail = 'Эта монета уже добавлена в избранное'
    default_code = 'duplicate_favorite'


class InvalidImageError(FileUploadError):
    default_detail = 'Загруженный файл не является допустимым изображением'
    default_code = 'invalid_image'


class FileTooLargeError(FileUploadError):
    default_detail = 'Размер файла превышает допустимый лимит'
    default_code = 'file_too_large'


class InvalidEstimatedValueError(ValidationError):
    default_detail = 'Недопустимое значение оценочной стоимости'
    default_code = 'invalid_estimated_value'