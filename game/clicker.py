from abc import ABC, abstractmethod
import random


class AbstractClicker(ABC):
    """абстрактный интерфейс кликера"""

    @abstractmethod
    def __init__(self, income_per_click: int) -> None:
        """создаёт кликер с заданным доходом"""

    @abstractmethod
    def click(self) -> None:
        """выполняет клик"""

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """возвращает доход за клик"""


class SimpleRandomClicker(AbstractClicker):
    """кликер с фиксированным доходом за действие"""

    def __init__(self, income_per_click: int = 10, max_income: int | None = None) -> None:
        """инициализирует диапазон дохода"""
        self._min_income = income_per_click
        self._max_income = max_income if max_income is not None else income_per_click
        if self._max_income < self._min_income:
            raise ValueError("Максимальный доход не может быть меньше минимального")
        self._income = self._min_income

    @property
    def income_per_click(self) -> int:
        """возвращает доход последнего клика"""
        return self._income

    def click(self) -> None:
        """начисляет случайный доход в заданном диапазоне"""
        self._income = random.randint(self._min_income, self._max_income)
