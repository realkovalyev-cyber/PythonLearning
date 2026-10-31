is_running = True

tasks = []


def ask_task_number(tasks, prompt):
    """Спрашивает номер задачи. Возвращает индекс или None, если ввод неверный."""
    try:
        index = int(input(prompt))
    except ValueError:
        print()
        print("Некорректный ввод. Нужно ввести число.")
        return None
    if index < 1 or index > len(tasks):
        print()
        print(f"Задача с номером {index} не найдена.")
        return None
    return index - 1


while is_running:
    print()
    print("=== ПРОСТОЙ TO DO ===\n")
    print("1. Добавить задачу")
    print("2. Отметить задачу как выполненную")
    print("3. Удалить задачу")
    print("4. Показать все задачи")
    print("5. Показать только выполненные задачи")
    print("6. Показать только невыполненные задачи")
    print("7. Выход\n")

    choice = input("Выберите действие: ")

    if choice == "1":
        title = input("Введите название задачи: ").strip()
        if not title:
            print()
            print("Название задачи не может быть пустым.")
        else:
            print()
            tasks.append({"title": title, "is_done": False})
            print(f"Задача '{title}' добавлена под номером {len(tasks)}.")


    elif choice == "2":
        print()
        if not tasks:
            print("Список задач пуст.")
        else:
            index = ask_task_number(
                tasks, "Введите номер задачи для отметки как выполненной: "
            )
            if index is not None:
                task = tasks[index]
                if task["is_done"]:
                    print()
                    print(f"Задача '{task['title']}' уже выполнена.")
                else:
                    task["is_done"] = True
                    print()
                    print(f"Задача '{task['title']}' отмечена как выполненная.")

    elif choice == "3":
        print()
        if not tasks:
            print("Список задач пуст.")
        else:
            index = ask_task_number(tasks, "Введите номер задачи для удаления: ")
            if index is not None:
                removed_task = tasks.pop(index)
                print()
                print(f"Задача '{removed_task['title']}' удалена.")

    elif choice == "4":
        print()
        if not tasks:
            print("Список задач пуст.")
        else:
            print("Список всех задач:")
            for index, task in enumerate(tasks, start=1):
                print(
                    f"{index}. {task['title']} - {'Выполнена' if task['is_done'] else 'Не выполнена'}"
                )

    elif choice == "5":
        print()
        if not tasks or not any(task["is_done"] for task in tasks):
            print("Список выполненных задач пуст.")
        else:
            print("Выполненные задачи:")
            for index, task in enumerate(tasks, start=1):
                if task["is_done"]:
                    print(f"{index}. {task['title']}")

    elif choice == "6":
        print()
        if not tasks or not any(not task["is_done"] for task in tasks):
            print("Список невыполненных задач пуст.")
        else:
            print("Невыполненные задачи:")
            for index, task in enumerate(tasks, start=1):
                if not task["is_done"]:
                    print(f"{index}. {task['title']}")

    elif choice == "7":
        print("Выход из программы.")
        is_running = False

    else:
        print()
        print("Неизвестный пункт меню, выберите от 1 до 7.")
