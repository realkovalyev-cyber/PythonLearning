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


def mark_task_done(task_list):
    if not task_list:
        console.print("[red]Список задач пуст. Нечего отмечать как выполненное.[/red]")
        return

    if not any(not task["is_done"] for task in task_list):
        console.print("[yellow]Все задачи уже выполнены.[/yellow]")
        return

    task_index = ask_task_number(task_list, "Введите номер задачи для отметки как выполненной: ")
    if task_index is None:
        return

    marked_task = task_list[task_index]
    if marked_task["is_done"]:
        console.print(f"[yellow]Задача '{escape(marked_task['title'])}' уже выполнена.[/yellow]")
    else:
        marked_task["is_done"] = True
        console.print(f"[green]Задача '{escape(marked_task['title'])}' отмечена как выполненная.[/green]")


def delete_task(task_list):
    if not task_list:
        console.print("[red]Список задач пуст. Нечего удалять.[/red]")
        return

    task_index = ask_task_number(task_list, "Введите номер задачи для удаления: ")
    if task_index is None:
        return

    deleted_task = task_list.pop(task_index)
    console.print(f"[green]Задача '{escape(deleted_task['title'])}' удалена.[/green]")


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


def show_all_tasks(task_list):
    if not task_list:
        console.print("[red]Список задач пуст.[/red]")
        return

    show_tasks(task_list)


def show_done_tasks(task_list):
    if not any(task["is_done"] for task in task_list):
        console.print("[red]Список выполненных задач пуст.[/red]")
        return

    show_tasks(task_list, filter_done=True)


def show_not_done_tasks(task_list):
    if not any(not task["is_done"] for task in task_list):
        console.print("[red]Список невыполненных задач пуст.[/red]")
        return

    show_tasks(task_list, filter_done=False)


def exit_program(task_list):
    global is_running
    if not task_list:
        console.print("[yellow]Список задач пуст. Выход из программы.[/yellow]")
    else:
        console.print("[yellow]Выход из программы. Все несохраненные данные будут потеряны.[/yellow]")
    is_running = False


ACTIONS = {
    Action.ADD_TASK: add_task,
    Action.MARK_DONE: mark_task_done,
    Action.DELETE_TASK: delete_task,
    Action.SHOW_ALL_TASKS: show_all_tasks,
    Action.SHOW_DONE_TASKS: show_done_tasks,
    Action.SHOW_NOT_DONE_TASKS: show_not_done_tasks,
    Action.EXIT: exit_program
}

try:
    while is_running:
        choice = show_menu()

        if choice is None:  # Пользователь нажал Ctrl+C
            console.print("[red]Выход по Ctrl+C.[/red]")
            is_running = False

        elif choice in ACTIONS:
            ACTIONS[choice](tasks)

        else:
            console.print("[red]Некорректный выбор действия.[/red]")

except KeyboardInterrupt:
    console.print("[red]Выход по Ctrl+C.[/red]")
