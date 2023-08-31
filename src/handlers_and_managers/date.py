class Date:

    def __init__(self, year: int, month: int, day: int):
        self._year = None
        self._month = None
        self._day = None

        self.year = year
        self.month = month
        self.day = day

    #
    # GETTERS
    #
    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    #
    # SETTERS
    #
    @year.setter
    def year(self, value):
        if type(value) != int:
            raise ValueError(f"year must be integer, got {type(value)!r} instead!")

        self._year = value

    @month.setter
    def month(self, value):
        if type(value) != int:
            raise ValueError(f"month must be integer, got {type(value)!r} instead!")

        self._month = value

    @day.setter
    def day(self, value):
        if type(value) != int:
            raise ValueError(f"day must be integer, got {type(value)!r} instead!")

        self._day = value
