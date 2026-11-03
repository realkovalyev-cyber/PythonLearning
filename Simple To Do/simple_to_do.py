is_running = True

tasks = []


def ask_task_number(task_list, prompt):
    """Спрашивает номер задачи. Возвращает индекс или None, если ввод неверный."""
    try:
        index = int(input(prompt))
    except ValueError:
        print("Некорректный ввод. Нужно ввести число.")
        return None
    if index < 1 or index > len(task_list):
        print(f"Задача с номером {index} не найдена.")
        return None
    return index - 1

def add_task(task_list):
    """Добавляет задачу в список."""
    title = input("Введите название задачи: ").strip()
    if not title:
        print("Название задачи не может быть пустым.")
    else:
        task_list.append({"title": title, "is_done": False})
        print(f"Задача '{title}' добавлена под номером {len(task_list)}.")


while is_running:
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
        add_task(tasks)

    elif choice == "2":
        if not tasks:
            print("Список задач пуст.")
        else:
            index = ask_task_number(
                tasks, "Введите номер задачи для отметки как выполненной: "
            )
            if index is not None:
                task = tasks[index]
                if task["is_done"]:
                    print(f"Задача '{task['title']}' уже выполнена.")
                else:
                    task["is_done"] = True
                    print(f"Задача '{task['title']}' отмечена как выполненная.")

    elif choice == "3":
        if not tasks:
            print("Список задач пуст.")
        else:
            index = ask_task_number(tasks, "Введите номер задачи для удаления: ")
            if index is not None:
                removed_task = tasks.pop(index)
                print(f"Задача '{removed_task['title']}' удалена.")

    elif choice == "4":
        if not tasks:
            print("Список задач пуст.")
        else:
            print("Список всех задач:")
            for index, task in enumerate(tasks, start=1):
                print(
                    f"{index}. {task['title']} - {'Выполнена' if task['is_done'] else 'Не выполнена'}"
                )

    elif choice == "5":
        if not tasks or not any(task["is_done"] for task in tasks):
            print("Список выполненных задач пуст.")
        else:
            print("Выполненные задачи:")
            for index, task in enumerate(tasks, start=1):
                if task["is_done"]:
                    print(f"{index}. {task['title']}")

    elif choice == "6":
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
        print("Неизвестный пункт меню, выберите от 1 до 7.")