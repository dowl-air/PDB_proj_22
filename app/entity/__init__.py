from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    ADMIN = "admin"


class BookCopyState(Enum):
    DELETED = 0
    NEW = 1
    GOOD = 2
    DAMAGED = 3
