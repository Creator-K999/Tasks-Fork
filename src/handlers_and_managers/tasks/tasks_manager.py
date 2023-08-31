from datetime import datetime

from ..date import Date
from ..file_handler import FileHandler
from task import Task


class TasksManager:

    tasks = {}
    file_handler = None

    @classmethod
    def construct(cls):
        cls.file_handler = FileHandler("repeated_tasks.csv")
        cls.extract_tasks_info()

    @classmethod
    def extract_tasks_info(cls):
        tasks = cls.file_handler.get_tasks()
        for _, task_details in enumerate(tasks, start=1):
            task_name, task_frequency, task_last_completed = task_details.split(",")

            if task_last_completed is not None:
                date = datetime.strptime(task_last_completed, "%Y-%m-%d")
                task_last_completed = Date(date.year, date.month, date.day)

            cls.tasks[task_name] = Task(task_name, task_frequency, task_last_completed)

    @classmethod
    def task_exist(cls, task_name):
        return task_name in cls.tasks

    @classmethod
    def add_task(cls, task_name, task_frequency) -> None:
        replace = None

        task_exist = cls.task_exist(task_name)

        while task_exist:
            replace = input(f"Task with same name exists:{task_name!r}\n Do you want to replace it? (Y/N): ").upper()

            if replace in {"Y", "N"}:
                break

        if replace == "N":
            return

        requested_task_frequency = None

        while True:
            try:
                requested_task_frequency = int(input("Repetition (# days): "))

                if requested_task_frequency > 0:
                    break
            except ValueError:
                continue

        if replace == "Y":
            cls.replace_task(task_name, requested_task_frequency)
        else:
            cls.tasks[task_name] = Task(task_name, task_frequency)

    @classmethod
    def replace_task(cls, task_name: str, task_frequency: int) -> None:
        cls.tasks[task_name].task_frequency = task_frequency

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

    @classmethod
    def destruct(cls):
        del cls.file_handler
        cls.tasks.clear()
