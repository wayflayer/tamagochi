class GameError(Exception):
    """базовое исключение для игры"""

    pass


class NotEnoughMoneyError(GameError):
    """ыызывается, если недостаточно монет"""

    pass


class ItemNotFoundError(GameError):
    """вызывается, если предмет не найден"""

    pass


class PetIsDeadError(GameError):
    """вызывается при попытке совершить действие с мертвым питомцем"""

    pass