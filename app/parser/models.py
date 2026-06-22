from dataclasses import dataclass


@dataclass
class Vacancy:
    """A data model describing one vacancy."""

    title: str
    company: str
    link: str
