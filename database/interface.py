from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    # Primary key
    uid: int
    ar: bool

class Database:
    @staticmethod
    def update_user(uid: int, **fields):
        raise NotImplementedError

    @staticmethod
    def fetch_user(uid: int) -> User:
        raise NotImplementedError
