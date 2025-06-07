from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class Article:
    url: str
    parsed_text: str
    id: UUID | None = None
    summary: str = field(default='')
    siblings: list['Article'] = field(default_factory=list)
