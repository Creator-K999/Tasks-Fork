class FileHandler:

    def __init__(self, file_name: str):
        self._file_name = None

        self.file_name = file_name
        self.file_instance = open(file_name)

    def get_tasks(self):
        return self.file_instance.read().splitlines()

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        if type(value) != str:
            raise ValueError(f"file_name must be str, got {type(value)!r} instead!")

        self._file_name = value

    def __del__(self):
        self.file_instance.close()
