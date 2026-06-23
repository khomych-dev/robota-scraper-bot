import sqlite3


class Database:
    """A class for working with the SQLite database (Bot Memory)."""

    def __init__(self, db_name: str = "vacancies.db") -> None:
        # Connect to the file (if it doesn't exist, it will be created automatically)
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self) -> None:
        """Creates a table to save links if it doesn't exist yet."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS seen_vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT UNIQUE
            )
        """)
        self.connection.commit()

    def is_seen(self, link: str) -> bool:
        """Checks if such a link is already in the database."""
        self.cursor.execute("SELECT 1 FROM seen_vacancies WHERE link = ?", (link,))
        return self.cursor.fetchone() is not None

    def mark_as_seen(self, link: str) -> None:
        """Records a new link in the database (so as not to show it again)."""
        self.cursor.execute("INSERT INTO seen_vacancies (link) VALUES (?)", (link,))
        self.connection.commit()

    def close(self) -> None:
        """Closes the database connection."""
        self.connection.close()
