from abc import ABC, abstractmethod
from game.models import Food, Medicine


class AbstractTamagochi(ABC):
    """абстрактный интерфейс питомца"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """кормит питомца"""

    @abstractmethod
    def play(self) -> None:
        """играет с питомцем"""

    @abstractmethod
    def rest(self) -> None:
        """восстанавливает силы питомца"""

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """лечит питомца"""

    @abstractmethod
    def status(self) -> dict[str, int]:
        """возвращает показатели питомца"""

    @abstractmethod
    def is_alive(self) -> bool:
        """проверяет, жив ли питомец"""

    @abstractmethod
    def is_sick(self) -> bool:
        """проверяет, болен ли питомец"""

    @abstractmethod
    def update(self) -> None:
        """обновляет состояние питомца за тик"""


class SimpleTamagochi(AbstractTamagochi):
    """простая реализация питомца"""

    def __init__(self, hunger: int = 50, fatigue: int = 0, hp: int = 100, energy: int = 100) -> None:
        """инициализирует показатели питомца"""
        self._hunger = self._bound(hunger)
        self._fatigue = self._bound(fatigue)
        self._hp = self._bound(hp)
        self._energy = self._bound(energy)
        self._sick = False

    @staticmethod
    def _bound(value: int) -> int:
        """ограничивает показатель диапазоном от 0 до 100"""
        return max(0, min(100, value))

    def feed(self, food: Food) -> None:
        """уменьшает голод, немного снижая энергию"""
        self._hunger = self._bound(self._hunger - food.satiety)
        self._energy = self._bound(self._energy - 5)

    def play(self) -> None:
        """повышает усталость и снижает энергию"""
        self._fatigue = self._bound(self._fatigue + 15)
        self._energy = self._bound(self._energy - 20)
        self._hunger = self._bound(self._hunger + 5)

    def rest(self) -> None:
        """восстанавливает энергию и уменьшает усталость"""
        multiplier = 0.5 if self._sick else 1
        self._energy = self._bound(self._energy + int(30 * multiplier))
        self._fatigue = self._bound(self._fatigue - int(25 * multiplier))

    def heal(self, medicine: Medicine) -> None:
        """восстанавливает здоровье и использует дозу лекарства"""
        if medicine.is_empty():
            return
        self._hp = self._bound(self._hp + medicine.heal_hp)
        medicine.uses += 1
        self._sick = False

    def status(self) -> dict[str, int]:
        """возвращает все числовые показатели питомца"""
        return {"hunger": self._hunger, "fatigue": self._fatigue,
                "hp": self._hp, "health": self._hp, "energy": self._energy}

    def is_alive(self) -> bool:
        """возвращает True, если здоровье выше нуля"""
        return self._hp > 0

    def is_sick(self) -> bool:
        """возвращает состояние болезни"""
        return self._sick

    def update(self) -> None:
        """увеличивает голод и усталость; болезнь снижает здоровье"""
        if not self.is_alive():
            return
        self._hunger = self._bound(self._hunger + 5)
        self._fatigue = self._bound(self._fatigue + 3)
        if self._hunger >= 80 or self._fatigue >= 80:
            self._sick = True
        if self._sick:
            self._hp = self._bound(self._hp - 10)
