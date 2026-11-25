import questionary
from questionary import Choice
from enum import Enum
from rich.table import Table
from rich.console import Console
from rich import box
from rich.markup import escape


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
console = Console()


def show_menu():
    """Показывает интерактивное меню и возвращает выбранное действие. При Ctrl+C возвращает None."""
    choices = [
        Choice(title=label, value=action)
        for action, label in ACTION_LABELS.items()
    ]

    return questionary.select(
        "Выберите действие:",
        choices=choices
    ).ask()


def ask_task_number(task_list, prompt):
    """Спрашивает номер задачи. Возвращает индекс или None, если ввод неверный."""
    try:
        task_number = int(input(prompt))
    except ValueError:
        console.print("[red]Некорректный ввод. Нужно ввести число.[/red]")
        return None
    if task_number < 1 or task_number > len(task_list):
        console.print(f"[red]Задача с номером {task_number} не найдена.[/red]")
        return None
    return task_number - 1


def add_task(task_list):
    title = input("Введите название задачи: ").strip()
    if not title:
        console.print("[red]Название задачи не может быть пустым.[/red]")
    else:
        task_list.append({"title": title, "is_done": False})
        console.print(f"[green]Задача '{escape(title)}' добавлена под номером {len(task_list)}.[/green]")


def show_tasks(task_list, filter_done=None):
    """Нумерация до фильтрации, чтобы сохранить правильные номера задач для пользователя."""
    table = Table(
        title="Список задач",
        border_style="blue",
        show_header=True,
        header_style="bold magenta",
        box=box.ROUNDED
    )

    table.add_column("№", justify="center", style="cyan", no_wrap=True, min_width=3)
    table.add_column("Название задачи", style="magenta", max_width=35)
    table.add_column("Статус", justify="center")

    for task_number, current_task in enumerate(task_list, start=1):
        if filter_done is None or current_task["is_done"] == filter_done:
            status = "[green]☑[/green]" if current_task["is_done"] else "[yellow]☐[/yellow]"
            table.add_row(str(task_number), escape(current_task["title"]), status)

    console.print(table)


try:
    while is_running:
        choice = show_menu()

        if choice == Action.ADD_TASK:
            add_task(tasks)

        elif choice == Action.MARK_DONE:
            if not tasks:
                console.print("[red]Список задач пуст.[/red]")
                continue

            index = ask_task_number(
                tasks, "Введите номер задачи для отметки как выполненной: "
            )
            if index is None:
                continue

            task = tasks[index]
            if task["is_done"]:
                console.print(f"[yellow]Задача '{escape(task['title'])}' уже выполнена.[/yellow]")
                continue

            task["is_done"] = True
            console.print(f"[green]Задача '{escape(task['title'])}' отмечена как выполненная.[/green]")

        elif choice == Action.DELETE_TASK:
            if not tasks:
                console.print("[red]Список задач пуст.[/red]")
                continue

            index = ask_task_number(tasks, "Введите номер задачи для удаления: ")
            if index is not None:
                removed_task = tasks.pop(index)
                console.print(f"[green]Задача '{escape(removed_task['title'])}' удалена.[/green]")

        elif choice == Action.SHOW_ALL_TASKS:
            if not tasks:
                console.print("[red]Список задач пуст.[/red]")
                continue

            show_tasks(tasks)

        elif choice == Action.SHOW_DONE_TASKS:
            if not any(task["is_done"] for task in tasks):
                console.print("[red]Список выполненных задач пуст.[/red]")
                continue

            show_tasks(tasks, filter_done=True)

        elif choice == Action.SHOW_NOT_DONE_TASKS:
            if not any(not task["is_done"] for task in tasks):
                console.print("[red]Список невыполненных задач пуст.[/red]")
                continue

            show_tasks(tasks, filter_done=False)

        elif choice == Action.EXIT:
            console.print("[green]Выход из программы.[/green]")
            is_running = False

        elif choice is None:
            console.print("[red]Отменено пользователем. Выход из программы.[/red]")
            is_running = False

except KeyboardInterrupt:
    console.print("[red]Программа завершена пользователем.[/red]")
