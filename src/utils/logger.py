import logging
from typing import Optional

from aiogram import types


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Настраивает и возвращает логгер"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


def log_user_action(logger: logging.Logger, user: types.User, action: str, **kwargs):
    """Логирует действия пользователя"""
    user_info = f"User(id={user.id}, username={user.username})"
    extra_info = " ".join([f"{k}={v}" for k, v in kwargs.items()])
    message = f"{user_info} {action}"
    if extra_info:
        message += f" {extra_info}"
    logger.info(message)


def log_error(logger: logging.Logger, error: Exception, context: Optional[str] = None):
    """Логирует ошибки с контекстом"""
    message = f"Error: {error}"
    if context:
        message = f"{context}: {message}"
    logger.error(message, exc_info=True)
