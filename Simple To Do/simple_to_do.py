from enum import Enum


class Action(Enum):
    ADD_TASK = 1
    MARK_DONE = 2
    DELETE_TASK = 3
    SHOW_ALL_TASKS = 4
    SHOW_DONE_TASKS = 5
    SHOW_NOT_DONE_TASKS = 6
    EXIT = 7


ACTION_LABELS = {
    Action.ADD_TASK: "Добавить задачу",
    Action.MARK_DONE: "Отметить задачу как выполненную",
    Action.DELETE_TASK: "Удалить задачу",
    Action.SHOW_ALL_TASKS: "Показать все задачи",
    Action.SHOW_DONE_TASKS: "Показать выполненные задачи",
    Action.SHOW_NOT_DONE_TASKS: "Показать невыполненные задачи",
    Action.EXIT: "Выход",
}


is_running = True
tasks = [] 


def show_menu():
    """Показывает меню действий."""
    print("=== ПРОСТОЙ TO DO ===\n")
    for action, label in ACTION_LABELS.items():
        print(f"{action.value}. {label}")
    print()


def ask_task_number(task_list, prompt):
    """Спрашивает номер задачи. Возвращает индекс или None, если ввод неверный."""
    try:
        task_index = int(input(prompt))
    except ValueError:
        print("Некорректный ввод. Нужно ввести число.")
        return None
    if task_index < 1 or task_index > len(task_list):
        print(f"Задача с номером {task_index} не найдена.")
        return None
    return task_index - 1


def add_task(task_list):
    """Добавляет задачу в список."""
    title = input("Введите название задачи: ").strip()
    if not title:
        print("Название задачи не может быть пустым.")
    else:
        task_list.append({"title": title, "is_done": False})
        print(f"Задача '{title}' добавлена под номером {len(task_list)}.")


while is_running:
    show_menu()
    choice = input("Выберите действие: ")

    if choice == "1":
        add_task(tasks)

    elif choice == "2":
        if not tasks:
            print("Список задач пуст.")
            continue

        index = ask_task_number(
            tasks, "Введите номер задачи для отметки как выполненной: "
        )
        if index is None:
            continue

        task = tasks[index]
        if task["is_done"]:
            print(f"Задача '{task['title']}' уже выполнена.")
        else:
            task["is_done"] = True
            print(f"Задача '{task['title']}' отмечена как выполненная.")

    elif choice == "3":
        if not tasks:
            print("Список задач пуст.")
            continue
        else:
            index = ask_task_number(tasks, "Введите номер задачи для удаления: ")
            if index is not None:
                removed_task = tasks.pop(index)
                print(f"Задача '{removed_task['title']}' удалена.")

    elif choice == "4":
        if not tasks:
            print("Список задач пуст.")
            continue
        else:
            print("Список всех задач:")
            for index, task in enumerate(tasks, start=1):
                print(
                    f"{index}. {task['title']} - {'Выполнена' if task['is_done'] else 'Не выполнена'}"
                )

    elif choice == "5":
        if not tasks or not any(task["is_done"] for task in tasks):
            print("Список выполненных задач пуст.")
            continue
        else:
            print("Выполненные задачи:")
            for index, task in enumerate(tasks, start=1):
                if task["is_done"]:
                    print(f"{index}. {task['title']}")

    elif choice == "6":
        if not tasks or not any(not task["is_done"] for task in tasks):
            print("Список невыполненных задач пуст.")
            continue
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