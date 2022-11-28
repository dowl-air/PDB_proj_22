from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    ADMIN = "admin"


class BookCopyState(Enum):
    AVAILABLE = 1
    RESERVED = 2
    BORROWED = 3
    DELETED = 4
