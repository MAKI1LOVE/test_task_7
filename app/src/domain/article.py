from dataclasses import dataclass, field


@dataclass
class Article:
    url: str
    parsed_text: str
    id: int = field(default=0)
    summary: str = field(default='')
    siblings: list['Article'] = field(default_factory=list)
