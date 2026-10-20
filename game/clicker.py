from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """интерфейс для кликера"""

    @abstractmethod
    def __init__(self, income_per_click: int) -> None:
        """инициализация кликера"""
        pass

    @abstractmethod
    def click(self) -> None:
        """основная логика кликера"""
        pass

    @property 
    @abstractmethod
    def income_per_click(self) -> int:
        """свойство для доступа к количеству зарабатываемых монет за клик"""
        pass


class SimpleRandomClicker(AbstractClicker):
    """реализация простого кликера"""

    def __init__(self, income_per_click: int) -> None:
        """инициализация кликера заданным доходом за клик"""
        self._income_per_click = income_per_click

    def click(self) -> None:
        """выполняется клик"""
        pass

    @property
    def income_per_click(self) -> int:
        """возвращает доход за один клик"""
        return self._income_per_click