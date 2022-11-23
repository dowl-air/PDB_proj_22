from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    ADMIN = "admin"
