from dataclasses import dataclass


@dataclass(frozen=True)
class LessonDecoded:
    # Index in Subjects list
    idx: int


@dataclass(frozen=True)
class LessonsList:
    # <lessonData>;<nextLesson>;etc.
    str_repr: str

    def decode(self) -> list[LessonDecoded]:
        return [LessonDecoded(idx) for idx in self.str_repr.split(';')]


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
class User:
    # Primary key
    uid: int
    general_schedule: Schedule
    subjects: Subjects


class Database:
    @staticmethod
    def update_user(uid: int, **fields):
        raise NotImplementedError

    @staticmethod
    def fetch_user(uid: int) -> User:
        raise NotImplementedError
