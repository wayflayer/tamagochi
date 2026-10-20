from dataclasses import dataclass


@dataclass
class Food:
    """класс модель для еды"""

    name: str
    satiety: int
    price: int


@dataclass
class Medicine:
    """класс модель для лекарства"""

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def is_empty(self) -> bool:
        """проверяет, остались ли ещё лекарства"""
        return self.uses >= self.number_of_uses