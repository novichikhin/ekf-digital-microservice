import enum


class Popularity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
