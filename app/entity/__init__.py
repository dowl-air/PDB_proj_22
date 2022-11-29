from enum import Enum

RESERVATION_DAYS_LENGTH = 7
BORROWAL_DAYS_LENGTH = 30


class UserRole(str, Enum):
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    ADMIN = "admin"


class BookCopyState(Enum):
    DELETED = 0
    NEW = 1
    GOOD = 2
    DAMAGED = 3


class ReservationState(Enum):
    CLOSED = 0
    ACTIVE = 1


class BorrowalState(Enum):
    RETURNED = 0
    ACTIVE = 1
    LOST = 2
