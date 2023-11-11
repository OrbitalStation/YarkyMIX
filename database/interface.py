from dataclasses import dataclass
from properties import const


@dataclass(frozen=True)
class LessonDecoded:
    # Index in Subjects list
    idx: int


@dataclass(frozen=True)
class LessonsList:
    # <lessonData>;<nextLesson>;etc.
    str_repr: str

    def decode(self) -> list[LessonDecoded]:
        return [LessonDecoded(idx) for idx in self.str_repr.split(';') if idx != ""]


@dataclass(frozen=True)
class WeekDaySchedule:
    lessons: LessonsList


@dataclass(frozen=True)
class Schedule:
    wd1: WeekDaySchedule
    wd2: WeekDaySchedule
    wd3: WeekDaySchedule
    wd4: WeekDaySchedule
    wd5: WeekDaySchedule
    wd6: WeekDaySchedule
    wd7: WeekDaySchedule


@dataclass(frozen=True)
class SubjectDecoded:
    name: str


@dataclass(frozen=True)
class Subjects:
    # physics;math;biology <-etc.
    str_repr: str

    def decode(self) -> list[SubjectDecoded]:
        return [SubjectDecoded(name=s) for s in self.str_repr.split(';')]


@dataclass(frozen=True)
class Homework:
    value: str


@dataclass(frozen=True)
class HWUser:
    # Primary key
    uid: int
    wd1: Homework
    wd2: Homework
    wd3: Homework
    wd4: Homework
    wd5: Homework
    wd6: Homework
    wd7: Homework


@dataclass(frozen=True)
class User:
    # Primary key
    uid: int
    general_schedule: Schedule
    subjects: Subjects

    @staticmethod
    def get_hw_db(uid: int):
        from .sqlite3 import SQLiteDB
        return SQLiteDB(const("dbMainPath"), f"hw{uid}", HWUser)


class Database:
    def update_user(self, uid: int, **fields):
        raise NotImplementedError

    def fetch_user(self, uid: int):
        raise NotImplementedError
