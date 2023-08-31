from ..date import Date


class Task:
    def __init__(self, task_name: str, task_frequency: int, task_last_completed: Date = None):
        self._task_name = None
        self._task_frequency = None
        self._task_last_completed = None

        self.task_name = task_name
        self.task_frequency = task_frequency
        self.task_last_completed = task_last_completed

    #
    # GETTERS
    #
    @property
    def task_name(self):
        return self._task_name

    @property
    def task_frequency(self):
        return self._task_frequency

    @property
    def task_last_completed(self):
        return self._task_last_completed

    #
    # SETTERS
    #

    @task_name.setter
    def task_name(self, value):
        if type(value) != str:
            raise ValueError(f"task_name must be string, got {type(value)!r} instead!")

        self._task_name = value

    @task_frequency.setter
    def task_frequency(self, value):
        if type(value) != int:
            raise ValueError(f"task_frequency must be integer, got {type(value)!r} instead!")

        self._task_frequency = value

    @task_last_completed.setter
    def task_last_completed(self, value):
        if type(value) != Date:
            raise ValueError(f"task_name must be Date, got {type(value)!r} instead!")

        self._task_last_completed = value
