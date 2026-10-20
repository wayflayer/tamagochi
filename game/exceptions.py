class GameError(Exception):
    """базовое исключение для игры"""


class NotEnoughMoneyError(GameError):
    """вызывается, если недостаточно монет"""


class ItemNotFoundError(GameError):
    """вызывается, если предмет не найден"""


class PetIsDeadError(GameError):
    """вызывается при попытке совершить действие с мёртвым питомцем"""
