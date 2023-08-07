from dataclasses import dataclass
from enum import Enum
from typing import List


class TideType(Enum):
    LOW = 0
    HIGH = 1

@dataclass
class TideInfo:
    timestamp: int
    height: float
    type: TideType

@dataclass
class TideInfoForDate:
    date: str
    sunrise: int 
    sunset: int
    tides: List[TideInfo]