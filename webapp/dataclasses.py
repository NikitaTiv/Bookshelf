import dataclasses


@dataclasses.dataclass()
class UserBook:
    name: str
    author: str
    description: str
