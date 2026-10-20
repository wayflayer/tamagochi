from abc import ABC, abstractmethod
from game.models import Food, Medicine


class AbstractTamagochi(ABC):
    """интерфейс тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """накормить питомца"""
        pass

    @abstractmethod
    def play(self) -> None:
        """поиграть с питомцем"""
        pass

    @abstractmethod
    def rest(self) -> None:
        """отдохнуть"""
        pass

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """ылечить питомца"""
        pass

    @abstractmethod
    def status(self) -> dict[str, int]:
        """получить данные обо всех показателях питомца"""
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        """метод для проверки, жив ли питомец"""
        pass

    @abstractmethod
    def is_sick(self) -> bool:
        """метод для проверки, болен ли питомец"""
        pass

    @abstractmethod
    def update(self) -> None:
        """метод для обновления состояния питомца"""
        pass


class SimpleTamagochi(AbstractTamagochi):
    """реализация питомца-тамагочи"""

    def __init__(
        self,
        hunger: int = 50,
        fatigue: int = 0,
        health: int = 100,
        energy: int = 100,
    ) -> None:
        """инициализация базовых показателей питомца"""
        self._hunger = max(0, min(100, hunger))
        self._fatigue = max(0, min(100, fatigue))
        self._health = max(0, min(100, health))
        self._energy = max(0, min(100, energy))
        self._is_sick = False

    def feed(self, food: Food) -> None:
        """уменьшает голод питомца при кормлении"""
        self._hunger = max(0, self._hunger - food.satiety)

    def play(self) -> None:
        """увеличивает усталость и снижает энергию при игре"""
        self._fatigue = min(100, self._fatigue + 15)
        self._energy = max(0, self._energy - 20)

    def rest(self) -> None:
        """восстанавливает энергию и снижает усталость"""
        self._energy = min(100, self._energy + 30)
        self._fatigue = max(0, self._fatigue - 25)

    def heal(self, medicine: Medicine) -> None:
        """лечит питомца, повышая здоровье"""
        self._health = min(100, self._health + medicine.heal_hp)
        self._is_sick = False
        medicine.uses += 1

    def status(self) -> dict[str, int]:
        """возвращает текущие показатели питомца в виде словаря"""
        return {
            "hunger": self._hunger,
            "fatigue": self._fatigue,
            "health": self._health,
            "energy": self._energy,
        }

    def is_alive(self) -> bool:
        """проверяет, жив ли питомец"""
        return self._health > 0

    def is_sick(self) -> bool:
        """ароверяет статус болезни питомца"""
        return self._is_sick

    def update(self) -> None:
        """обновляет параметры питомца за один игровой тик"""
        self._hunger = min(100, self._hunger + 5)
        self._fatigue = min(100, self._fatigue + 3)
        if self._hunger >= 80 or self._fatigue >= 80:
            self._is_sick = True
        if self._is_sick:
            self._health = max(0, self._health - 10)