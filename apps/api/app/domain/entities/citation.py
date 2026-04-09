from dataclasses import dataclass


@dataclass(frozen=True)
class Citation:
    filename: str
