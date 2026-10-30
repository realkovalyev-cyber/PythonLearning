def start_game():
    hero = {
        "name": "Артур",
        "health": 100,
        "gold": 20,
        "level": 1
    }
    
    backpack = ["меч", "аптечка"]
    
    monster = {
    "name": "Гоблин",
    "health": 60,
    "damage": 2.5
    }
    
    while True:
        print()
        print("=== ПОДЗЕМЕЛЬЕ СОКРОВИЩ ===\n")
        print(f"Ваш герой: {hero['name']}, выбери действие:\n")
        print("1. Пойти в пещеру")
        print("2. Отправиться в лес")
        print("3. Посетить замок")
        print("4. Проверить героя")
        print("5. Использовать аптечку")
        print("6. Сразиться с монстром")
        print("7. Выйти из игры\n")

        input_choice = input("Введите номер действия: ")
        print()
        if input_choice == "7":
            break
        elif input_choice == "1":
            hero["gold"] = hero["gold"] + 10
            hero["health"] = hero["health"] - 20
            print("Вы нашли 10 золотых монет в пещере, но потеряли 20 очков здоровья!")
        elif input_choice == "2":
            if "аптечка" in backpack:
                print("У вас уже есть аптечка в рюкзаке.")
            elif len(backpack) < 3:
                backpack.append("аптечка")
                print("Вы нашли аптечку в лесу и положили её в рюкзак.")
            else:
                print("Ваш рюкзак полон! Вы не можете взять аптечку.")
        elif input_choice == "3":
            hero["level"] = hero["level"] + 1
            hero["gold"] = hero["gold"] + 20
            print("Посетив замок, вы повысили свой уровень и получили 20 золотых монет!")
        elif input_choice == "4":
            print("Информация о вашем герое:")
            print()
            for key, value in hero.items():
                if key == "health":
                    print(f"  {key}: {value:g}")
                else:
                    print(f"  {key}: {value}")
            print()
            print(f"Предметы в рюкзаке: {', '.join(backpack)}")
        elif input_choice == "5":
            if "аптечка" not in backpack:
                print("У вас нет аптечки в рюкзаке.")
            elif hero["health"] >= 100:
                print("Ваше здоровье и так полно.")
            elif hero["health"] < 100:
                healed = min(30, 100 - hero["health"])
                hero["health"] = hero["health"] + healed
                print(f"Вы использовали аптечку и восстановили {healed} очков здоровья!")
                backpack.remove("аптечка")
        elif input_choice == "6":
            if monster["health"] <= 0:
                print("Монстр уже побежден!")
            else:
                print("Вы сражаетесь с монстром!")
                while monster["health"] > 0 and hero["health"] > 0:
                    monster["health"] = monster["health"] - 20
                    print(f"Вы нанесли удар монстру! Его здоровье: {monster['health']}")
                    if monster["health"] <= 0:
                        print("Вы победили монстра!")
                        hero["gold"] = hero["gold"] + 30
                        print("Вы получили 30 золотых монет за победу над монстром!")
                        break
                    hero["health"] = hero["health"] - monster["damage"]
                    print(f"Монстр атакует вас! Ваше здоровье: {hero['health']:g}")
                    if hero["health"] <= 0:
                        print("Ваш герой погиб в бою с монстром. Игра окончена.")
                        break
        else:
            print("Неверный выбор. Пожалуйста, выберите действие от 1 до 7.")
        
        if hero["health"] <= 0:
            print("Ваш герой погиб. Игра окончена.")
            break

start_game()