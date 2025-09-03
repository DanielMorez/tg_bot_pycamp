class AuthError(Exception):
    """Исключение для ошибок авторизации"""

    pass


class CacheError(Exception):
    """Исключение для ошибок кеширования"""

    pass


class APIError(Exception):
    """Исключение для ошибок API"""

    pass
