from datetime import datetime
from typing import TextIO


class Main:

    MENU = (
        """1- View Due Tasks
    2- Add Task
    3- Delete Task
    4- Complete Task"""
    )
    OPTIONS_NO = 4
    FILE_NAME = "repeated_tasks.csv"

    @classmethod
    def run(cls):

        def main():
            close = False

            while not close:
                option = take_option()

                if option == 1:
                    print_due_tasks()
                elif option == 2:
                    add_task()
                elif option == 3:
                    delete_task()
                elif option == 4:
                    complete_task()

                while True:
                    option = input("Go back to the menu? (Y/N): ").upper()

                    if option in ("Y", "N"):
                        close = (option == "N")
                        break

        def take_option() -> int:
            print(cls.MENU)

            option = None

            while True:
                try:
                    option = int(input(f"Please pick an option (1-{cls.OPTIONS_NO}): "))

                    if 0 < option < cls.OPTIONS_NO + 1:
                        break

                except ValueError as e:
                    continue

            return option

        def add_task() -> None:
            replace = "Y"
            task_name = input("Task Name: ")

            line_no, task_details = task_exist(task_name)

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
                except ValueError as e:
                    continue

            if replace == "Y":
                replace_task(line_no, task_name, task_repetition)
            else:
                write_task(task_name, task_repetition)

        def get_csv_line(task_name: str, task_repetition: int, last_completion_date: str = "") -> str:
            return f"{task_name},{task_repetition},{last_completion_date}"

        def task_exist(task_name: str) -> tuple[int, str]:
            with open(cls.FILE_NAME, "r") as file:
                lines = file.readlines()

                for line_index in range(len(lines)):
                    if lines[line_index].split(",")[0] == task_name:
                        return line_index, lines[line_index]

                return -1, ""

        def is_due(last_completion_date: str) -> bool:
            pass

        def get_tasks() -> list:
            with open(cls.FILE_NAME, "r") as file:
                return file.read().splitlines()

        def print_tasks() -> None:
            lines = get_tasks()

            print(f"{'Task No.':<10}{'Name':<25}{'Repetition':<5}{'last_completion_date':<20}")
            for line_no, task_details in enumerate(lines, start=1):
                task_name, repetition, last_completion_date = task_details.split(",")

                print(f"{line_no:<10}{task_name:<25}{repetition:<5}{last_completion_date:<20}")

        def print_due_tasks() -> None:
            lines = get_tasks()

            print(f"{'Task No.':<10}{'Name':<25}{'Repetition':<5}{'last_completion_date':<20}")
            for line_no, task_details in enumerate(lines, start=1):
                task_name, repetition, last_completion_date = task_details.split(",")

                if is_due(last_completion_date):
                    print(f"{line_no:<10}{task_name:<25}{repetition:<5}{last_completion_date:<20}")

        def write_task(task_name: str, task_repetition) -> None:
            with open(cls.FILE_NAME, "a") as file:
                file.write(get_csv_line(task_name, task_repetition))

        def move_to_line(file: TextIO, line_index) -> None:
            for _ in range(line_index):
                file.readline()

        def replace_task(line_index: int, task_name: str, task_repetition: int) -> None:
            with open(cls.FILE_NAME, "w+") as file:
                move_to_line(file, line_index)
                file.write(get_csv_line(task_name, task_repetition))

                # file.writelines([*lines[:line_index], get_csv_line(task_name, task_repetition), *lines[line_index +
                # 1:]])

        def delete_task(task_name: str) -> bool:
            task_exists = False

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

        def complete_task(task_name: str) -> bool:
            task_exists = False

            with open(cls.FILE_NAME, "r") as file:
                lines = file.readlines()

                for line_no, line_details in enumerate(lines):
                    if line_details.split(",")[0] == task_name:
                        task = line_details.split(",")
                        task[2] = datetime.now()  # Updating Last Completion Date
                        lines[line_no] = ",".join(task)

                        task_exists = True

            if task_exists:
                with open(cls.FILE_NAME, "w") as file:
                    file.writelines(lines)

            return task_exists

        if __name__ == "__main__":
            main()