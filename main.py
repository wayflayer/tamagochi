from game.clicker import SimpleRandomClicker
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def main() -> None:
    """точка входа в игру тамагочи кликер"""
    all_food = [
        Food(name="Бургер", satiety=20, price=40),
        Food(name="Салат", satiety=10, price=20),
        Food(name="Яблоко", satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(name="Ибупрофен", price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(income_per_click=15)
    game = SimpleGame(tamagochi, clicker, all_food, all_medicine)

    print("Добро пожаловать в тамагочи-кликер!")
    
    while True:
        status = game.get_status()
        if not status["is_alive"]:
            print("\nGame Over! Ваш питомец погиб.")
            break

        print("\n--- СТАТУС ИГРЫ ---")
        print(f"Монеты: {status['money']}")
        print(f"Питомец: {status['pet']}")
        print(f"Болен: {status['is_sick']}")
        print(f"Сумка с едой: {status['inventory_food']}")
        print(f"Сумка с лекарствами: {status['inventory_medicine']}")
        
        print("\nВыберите действие:")
        print("1. Работать (клик)")
        print("2. Купить еду")
        print("3. Купить лекарство")
        print("4. Покормить питомца")
        print("5. Лечить питомца")
        print("6. Поиграть с питомцем")
        print("7. Отдохнуть")
        print("0. Выход")

        choice = input("Ваш выбор: ").strip()

        try:
            if choice == "1":
                earned = game.work()
                print(f"Вы поработали и заработали {earned} монет!")
            elif choice == "2":
                print("Доступная еда:")
                for i, f in enumerate(game.food):
                    print(f"{i + 1}. {f.name} (сытность: {f.satiety}, цена: {f.price})")
                f_idx = int(input("Номер еды для покупки: ")) - 1
                game.buy_food(game.food[f_idx].name)
                print("Еда успешно куплена!")
            elif choice == "3":
                print("Доступные лекарства:")
                for i, m in enumerate(game.medicine):
                    print(f"{i + 1}. {m.name} (лечит: {m.heal_hp}, цена: {m.price})")
                m_idx = int(input("Номер лекарства для покупки: ")) - 1
                game.buy_medicine(game.medicine[m_idx].name)
                print("Лекарство успешно куплено!")
            elif choice == "4":
                if not status["inventory_food"]:
                    print("У вас нет еды в инвентаре!")
                    continue
                f_name = input("Введите название еды из сумки: ").strip()
                game.feed_tamagochi(f_name)
                print("Питие/кормление прошло успешно.")
            elif choice == "5":
                if not status["inventory_medicine"]:
                    print("У вас нет лекарств в инвентаре!")
                    continue
                m_name = input("Введите название лекарства из сумки: ").strip()
                game.heal_tamagochi(m_name)
                print("Питомец подлечен.")
            elif choice == "6":
                game.play_with_tamagochi()
                print("Вы поиграли с питомцем.")
            elif choice == "7":
                game.rest()
                print("Питомец отдохнул.")
            elif choice == "0":
                print("Выход из игры...")
                break
            else:
                print("Неверный выбор, попробуйте снова.")
        except Exception as e:
            print(f"[Ошибка]: {e}")


if __name__ == "__main__":
    main()