from game.clicker import SimpleRandomClicker
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def main() -> None:
    """Запускает консольную игру."""
    all_food = [Food("Бургер", 20, 40), Food("Салат", 10, 20), Food("Яблоко", 10, 15)]
    all_medicine = [Medicine("Ибупрофен", 30, 20, 2)]
    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    game = SimpleGame(tamagochi, clicker, all_food, all_medicine)
    print("Добро пожаловать в тамагочи-кликер!")
    while True:
        status = game.get_status()
        if not status["is_alive"]:
            print("Game Over! Ваш питомец погиб.")
            break
        print(f"\nСтатус: голод {status['hunger']}, здоровье {status['hp']}, энергия {status['energy']}, монет {status['coins']}")
        print("1. Работа\n2. Купить еду\n3. Купить лекарство\n4. Покормить\n5. Вылечить\n6. Играть\n7. Отдых\n0. Выход")
        try:
            choice = input("Выберите действие: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        try:
            if choice == "0":
                break
            if choice == "1":
                print(f"Заработано {game.work()} монет")
            elif choice == "2":
                for i, item in enumerate(game.food, 1): print(f"{i}. {item.name} — {item.price}")
                idx = int(input("Номер еды: ")) - 1
                game.buy_food(game.food[idx].name)
            elif choice == "3":
                for i, item in enumerate(game.medicine, 1): print(f"{i}. {item.name} — {item.price}")
                idx = int(input("Номер лекарства: ")) - 1
                game.buy_medicine(game.medicine[idx].name)
            elif choice == "4":
                game.feed_tamagochi()
            elif choice == "5":
                game.heal_tamagochi()
            elif choice == "6":
                game.play_with_tamagochi()
            elif choice == "7":
                game.rest_tamagochi()
            else:
                print("Неверная команда")
        except (ValueError, IndexError, Exception) as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
