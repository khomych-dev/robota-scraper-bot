from dataclasses import dataclass


@dataclass
class Vacancy:
    """A model describing a single job opening."""

    title: str
    company: str
    link: str
    description: str = ""
