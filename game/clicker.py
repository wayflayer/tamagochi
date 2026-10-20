from abc import ABC, abstractmethod
import random


class AbstractClicker(ABC):
    """Абстрактный интерфейс кликера."""

    @abstractmethod
    def __init__(self, income_per_click: int) -> None:
        """Создаёт кликер с заданным доходом."""

    @abstractmethod
    def click(self) -> None:
        """Выполняет клик."""

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Возвращает доход за клик."""


class SimpleRandomClicker(AbstractClicker):
    """Кликер с фиксированным доходом за действие."""

    def __init__(self, income_per_click: int = 10, max_income: int | None = None) -> None:
        """Инициализирует диапазон дохода (или фиксированное значение)."""
        self._min_income = income_per_click
        self._max_income = max_income if max_income is not None else income_per_click
        if self._max_income < self._min_income:
            raise ValueError("Максимальный доход не может быть меньше минимального")
        self._income = self._min_income

    @property
    def income_per_click(self) -> int:
        """Возвращает доход последнего клика."""
        return self._income

    def click(self) -> None:
        """Начисляет случайный доход в заданном диапазоне."""
        self._income = random.randint(self._min_income, self._max_income)
