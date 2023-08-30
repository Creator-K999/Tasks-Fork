from datetime import datetime, timedelta
from os import system
from typing import TextIO


class Main:
    MENU: str = \
        """1- View Due Tasks
2- Add Task
3- Delete Task
4- Complete Task
0- Exit"""

    OPTIONS_NO: int = 4
    FILE_NAME: str = "repeated_tasks.csv"

    last_message = None

    @classmethod
    def run(cls):

        options_dict = (None, Main.get_due_tasks, Main.add_task, Main.delete_task, Main.complete_task)

        while True:
            system("cls")

            if cls.last_message:
                print(cls.last_message)

            option = cls.take_option()
            function = options_dict[option]

            if function:
                cls.last_message = function()
                continue

            break

    @classmethod
    def take_option(cls) -> int:
        print(cls.MENU)

        while True:
            try:
                option = int(input(f"Please pick an option (0-{cls.OPTIONS_NO}): "))

                if -1 < option < cls.OPTIONS_NO + 1:
                    return option

            except ValueError:
                continue

    @classmethod
    def add_task(cls) -> None:
        line_no = -1
        task_details = None
        replace = None

        task_name = input("Task Name: ")

        try:
            line_no, task_details = cls.task_exist(task_name)

        except FileNotFoundError:
            pass

        if line_no != -1:
            while True:
                replace = input(
                    f"Task with same name exists:\n{task_details}\n Do you want to replace it? (Y/N): ").upper()

                if replace in {"Y", "N"}:
                    break

            if replace == "N":
                return

        task_repetition = None

        while True:
            try:
                task_repetition = int(input("Repetition (# days): "))

                if task_repetition > 0:
                    break
            except ValueError:
                continue

        if replace == "Y":
            cls.replace_task(line_no, task_name, task_repetition)
        else:
            cls.write_task(task_name, task_repetition)

    @classmethod
    def get_csv_line(cls, task_name: str, task_repetition: int, last_completion_date: str = "") -> str:
        return f"{task_name},{task_repetition},{last_completion_date}"

    @classmethod
    def task_exist(cls, task_name: str) -> tuple[int, str]:
        with open(cls.FILE_NAME, "r") as file:
            lines = file.readlines()

            for line_index in range(len(lines)):
                if lines[line_index].split(",")[0] == task_name:
                    return line_index, lines[line_index]

            return -1, ""

    @classmethod
    def is_due(cls, last_completion_date: str, repetition: int) -> bool:
        repetition = timedelta(days=repetition)

        next_due_date = datetime.strptime(last_completion_date, "%d/%m/%Y") + repetition
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        return current_date > next_due_date

    @classmethod
    def get_tasks(cls) -> list:
        with open(cls.FILE_NAME, "r") as file:
            return file.read().splitlines()

    @classmethod
    def print_tasks(cls) -> None:
        lines = cls.get_tasks()

        print(f"{'Task No.':<10}{'Name':<25}{'Repetition':<5}{'last_completion_date':<20}")
        for line_no, task_details in enumerate(lines, start=1):
            task_name, repetition, last_completion_date = task_details.split(",")

            print(f"{line_no:<10}{task_name:<25}{repetition:<5}{last_completion_date:<20}")

    @classmethod
    def get_due_tasks(cls) -> str | None:
        due_tasks = [f"{'Task No.':<16}{'Name':<20}{'Repetition':<20}{'last_completion_date':<20}\n"]

        try:
            lines = cls.get_tasks()
        except FileNotFoundError as e:
            print("Error: File Not Found!!\nPlease add a task to auto-create a file.")
            return

        for line_no, task_details in enumerate(lines, start=1):
            task_name, repetition, last_completion_date = task_details.split(",")

            if cls.is_due(last_completion_date, int(repetition)):
                due_tasks.append(f"{line_no:<16}{task_name:<20}{repetition:<20}{last_completion_date:<20}\n")

        return "".join(due_tasks)

    @classmethod
    def write_task(cls, task_name: str, task_repetition) -> None:
        with open(cls.FILE_NAME, "a") as file:
            file.write(cls.get_csv_line(task_name, task_repetition))

    @classmethod
    def move_to_line(cls, file: TextIO, line_index) -> None:
        for _ in range(line_index):
            file.readline()

    @classmethod
    def replace_task(cls, line_index: int, task_name: str, task_repetition: int) -> None:
        with open(cls.FILE_NAME, "w+") as file:
            cls.move_to_line(file, line_index)
            file.write(cls.get_csv_line(task_name, task_repetition))

            # file.writelines([*lines[:line_index], get_csv_line(task_name, task_repetition), *lines[line_index +
            # 1:]])

    @classmethod
    def delete_task(cls) -> bool:
        task_exists = False

        task_name = input("Task Name: ")

        with open(cls.FILE_NAME, "r") as file:
            lines = file.readlines()

            for line_no, line_details in enumerate(lines):
                if line_details.split(",")[0] == task_name:
                    lines.pop(line_no)
                    task_exists = True

        if task_exists:
            with open(cls.FILE_NAME, "w") as file:
                file.writelines(lines)

        return task_exists

    @classmethod
    def complete_task(cls) -> str:
        task_exists = False

        task_name = input("Task Name: ")

        with open(cls.FILE_NAME, "r") as file:
            lines = file.readlines()

            for line_no, line_details in enumerate(lines):
                if line_details.split(",")[0] == task_name:
                    task = line_details.split(",")
                    task[2] = datetime.now().strftime("%Y-%m-%d")  # Updating Last Completion Date
                    lines[line_no] = ",".join(task)

                    task_exists = True

        if task_exists:
            with open(cls.FILE_NAME, "w") as file:
                file.writelines(lines)

        else:
            return f"Task {task_name!r} Doesn't Exist"
