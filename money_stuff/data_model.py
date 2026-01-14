from dataclasses import dataclass, field
from datetime import datetime

from typing import List, Optional


@dataclass
class Article:
    title: str
    text: str
    id: Optional[int] = None
    html: Optional[str] = None


@dataclass
class Newsletter:
    sent_date: datetime
    subject: str
    articles: List[Article] = field(default_factory=list)
    id: Optional[int] = None
