from abc import ABC, abstractmethod
from game.clicker import AbstractClicker
from game.exceptions import NotEnoughMoneyError, ItemNotFoundError
from game.models import Food, Medicine
from game.tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """интерфейс для сущности игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """инициализация игры"""
        pass

    @abstractmethod
    def work(self) -> int:
        """логика действия пойти на работу"""
        pass

    @abstractmethod
    def buy_food(self, food_name: str) -> None:
        """логика действия покупка еды"""
        pass

    @abstractmethod
    def buy_medicine(self, medicine_name: str) -> None:
        """логика действия купить лекарство"""
        pass

    @abstractmethod
    def feed_tamagochi(self, food_name: str) -> None:
        """логика действия покормить питомца"""
        pass

    @abstractmethod
    def heal_tamagochi(self, medicine_name: str) -> None:
        """логика действия вылечить питомца"""
        pass

    @abstractmethod
    def rest(self) -> None:
        """логика действия отдохнуть"""
        pass

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """логика действия поиграть с питомцем"""
        pass

    @abstractmethod
    def get_status(self) -> dict:
        """Получение статуса игры"""
        pass

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """свойство для доступа к еде"""
        pass

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """свойство для доступа к лекарствам"""
        pass


class SimpleGame(AbstractGame):
    """реализация основного игрового процесса"""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """инициализация игры, питомца, кликера и инвентаря магазина"""
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._money = 100
        self._inventory_food: list[Food] = []
        self._inventory_medicine: list[Medicine] = []

    def work(self) -> int:
        """зарабатывает монеты с помощью кликера и обновляет состояние питомца"""
        earned = self._clicker.income_per_click
        self._money += earned
        self._tamagochi.update()
        return earned

    def buy_food(self, food_name: str) -> None:
        """покупает еду по имени, если хватает денег"""
        target_food = next((f for f in self._all_food if f.name == food_name), None)
        if not target_food:
            raise ItemNotFoundError(f"Еда '{food_name}' не найдена")
        if self._money < target_food.price:
            raise NotEnoughMoneyError("Недостаточно средств для покупки еды")
        
        self._money -= target_food.price
        self._inventory_food.append(target_food)
        self._tamagochi.update()

    def buy_medicine(self, medicine_name: str) -> None:
        """покупает лекарство по имени, если хватает денег"""
        target_med = next((m for m in self._all_medicine if m.name == medicine_name), None)
        if not target_med:
            raise ItemNotFoundError(f"Лекарство '{medicine_name}' не найдено")
        if self._money < target_med.price:
            raise NotEnoughMoneyError("Недостаточно средств для покупки лекарства")
        
        self._money -= target_med.price
        self._inventory_medicine.append(target_med)
        self._tamagochi.update()

    def feed_tamagochi(self, food_name: str) -> None:
        """кормит питомца едой из инвентаря"""
        target_food = next((f for f in self._inventory_food if f.name == food_name), None)
        if not target_food:
            raise ItemNotFoundError(f"У вас нет еды '{food_name}' в инвентаре")
        
        self._tamagochi.feed(target_food)
        self._inventory_food.remove(target_food)
        self._tamagochi.update()

    def heal_tamagochi(self, medicine_name: str) -> None:
        """лечит питомца лекарством из инвентаря"""
        target_med = next((m for m in self._inventory_medicine if m.name == medicine_name and not m.is_empty()), None)
        if not target_med:
            raise ItemNotFoundError(f"Доступное лекарство '{medicine_name}' не найдено в инвентаре")
        
        self._tamagochi.heal(target_med)
        if target_med.is_empty():
            self._inventory_medicine.remove(target_med)
        self._tamagochi.update()

    def rest(self) -> None:
        """отправляет питомца на отдых"""
        self._tamagochi.rest()
        self._tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """играет с питомцем"""
        self._tamagochi.play()
        self._tamagochi.update()

    def get_status(self) -> dict:
        """возвращает общую информацию о состоянии игры"""
        return {
            "money": self._money,
            "pet": self._tamagochi.status(),
            "is_alive": self._tamagochi.is_alive(),
            "is_sick": self._tamagochi.is_sick(),
            "inventory_food": [f.name for f in self._inventory_food],
            "inventory_medicine": [m.name for m in self._inventory_medicine],
        }

    @property
    def food(self) -> list[Food]:
        """доступный ассортимент еды в магазине"""
        return self._all_food

    @property
    def medicine(self) -> list[Medicine]:
        """доступный ассортимент лекарств в магазине"""
        return self._all_medicine