class GameError(Exception):
    """базовое исключение для игры"""


class NotEnoughMoney(GameError):
    """возникает при нехватке монет для покупки"""


class TamagochiIsGone(GameError):
    """возникает при попытке действовать с погибшим питомцем"""


class ItemNotFoundError(GameError):
    """возникает, если предмет не найден"""


NotEnoughMoneyError = NotEnoughMoney
PetIsDeadError = TamagochiIsGone
