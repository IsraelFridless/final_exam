from dataclasses import dataclass
from typing import Optional


@dataclass
class Date:
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None