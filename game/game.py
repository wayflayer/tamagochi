from abc import ABC, abstractmethod
from game.clicker import AbstractClicker
from game.exceptions import NotEnoughMoneyError, ItemNotFoundError, PetIsDeadError
from game.models import Food, Medicine
from game.tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Абстрактный интерфейс игровой логики."""

    @abstractmethod
    def __init__(self, tamagochi: AbstractTamagochi, clicker: AbstractClicker,
                 all_food: list[Food], all_medicine: list[Medicine]) -> None:
        """Инициализирует игру."""

    @abstractmethod
    def work(self) -> int:
        """Зарабатывает деньги."""

    @abstractmethod
    def buy_food(self, food_name: str | None = None) -> None:
        """Покупает еду."""

    @abstractmethod
    def buy_medicine(self, medicine_name: str | None = None) -> None:
        """Покупает лекарство."""

    @abstractmethod
    def feed_tamagochi(self, food_name: str | None = None) -> None:
        """Кормит питомца."""

    @abstractmethod
    def heal_tamagochi(self, medicine_name: str | None = None) -> None:
        """Лечит питомца."""

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Отправляет питомца отдыхать."""

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Играет с питомцем."""

    @abstractmethod
    def get_status(self) -> dict:
        """Возвращает состояние игры."""

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Возвращает ассортимент еды."""

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Возвращает ассортимент лекарств."""


class SimpleGame(AbstractGame):
    """Реализация игровой логики, денег и инвентаря."""

    def __init__(self, tamagochi: AbstractTamagochi, clicker: AbstractClicker,
                 all_food: list[Food], all_medicine: list[Medicine]) -> None:
        """Сохраняет компоненты игры и создаёт инвентарь."""
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._money = 100
        self._inventory_food: list[Food] = []
        self._inventory_medicine: list[Medicine] = []

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """Возвращает питомца для отображения состояния."""
        return self._tamagochi

    def _check_alive(self) -> None:
        """Запрещает действия с погибшим питомцем."""
        if not self._tamagochi.is_alive():
            raise PetIsDeadError("Питомец погиб")

    def work(self) -> int:
        """Выполняет клик, начисляет деньги и обновляет питомца."""
        self._check_alive()
        self._clicker.click()
        earned = self._clicker.income_per_click
        self._money += earned
        self._tamagochi.update()
        return earned

    def buy_food(self, food_name: str | None = None) -> None:
        """Покупает названную еду или первую доступную."""
        self._check_alive()
        item = next((f for f in self._all_food if food_name is None or f.name == food_name), None)
        if item is None:
            raise ItemNotFoundError("Еда не найдена")
        if self._money < item.price:
            raise NotEnoughMoneyError("Недостаточно средств для покупки еды")
        self._money -= item.price
        self._inventory_food.append(item)
        self._tamagochi.update()

    def buy_medicine(self, medicine_name: str | None = None) -> None:
        """Покупает названное лекарство или первое доступное."""
        self._check_alive()
        item = next((m for m in self._all_medicine if medicine_name is None or m.name == medicine_name), None)
        if item is None:
            raise ItemNotFoundError("Лекарство не найдено")
        if self._money < item.price:
            raise NotEnoughMoneyError("Недостаточно средств для покупки лекарства")
        self._money -= item.price
        self._inventory_medicine.append(item)
        self._tamagochi.update()

    def feed_tamagochi(self, food_name: str | None = None) -> None:
        """Кормит питомца выбранной едой из инвентаря."""
        self._check_alive()
        item = next((f for f in self._inventory_food if food_name is None or f.name == food_name), None)
        if item is None:
            raise ItemNotFoundError("Еда не найдена в инвентаре")
        self._tamagochi.feed(item)
        self._inventory_food.remove(item)
        self._tamagochi.update()

    def heal_tamagochi(self, medicine_name: str | None = None) -> None:
        """Лечит питомца доступным лекарством."""
        self._check_alive()
        item = next((m for m in self._inventory_medicine
                     if (medicine_name is None or m.name == medicine_name) and not m.is_empty()), None)
        if item is None:
            raise ItemNotFoundError("Доступное лекарство не найдено в инвентаре")
        self._tamagochi.heal(item)
        if item.is_empty():
            self._inventory_medicine.remove(item)
        self._tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Восстанавливает силы питомца."""
        self._check_alive()
        self._tamagochi.rest()
        self._tamagochi.update()

    def rest(self) -> None:
        """Совместимый псевдоним метода отдыха."""
        self.rest_tamagochi()

    def play_with_tamagochi(self) -> None:
        """Играет с питомцем и обновляет состояние."""
        self._check_alive()
        self._tamagochi.play()
        self._tamagochi.update()

    def get_status(self) -> dict:
        """Возвращает деньги, показатели и инвентарь."""
        pet_status = self._tamagochi.status()
        return {**pet_status, "coins": self._money, "money": self._money,
                "hp": pet_status.get("hp", pet_status.get("health", 0)),
                "pet": pet_status, "is_alive": self._tamagochi.is_alive(),
                "is_sick": self._tamagochi.is_sick(),
                "inventory_food": [f.name for f in self._inventory_food],
                "inventory_medicine": [m.name for m in self._inventory_medicine]}

    @property
    def food(self) -> list[Food]:
        """Возвращает каталог еды."""
        return self._all_food

    @property
    def medicine(self) -> list[Medicine]:
        """Возвращает каталог лекарств."""
        return self._all_medicine
