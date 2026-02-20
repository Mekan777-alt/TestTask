from enum import Enum


class UserStatus(str, Enum):
    """Статусы пользователей"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
