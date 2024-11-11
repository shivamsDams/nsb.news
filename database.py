import sqlite3

class Database:
    def __init__(self, db_name="used_headlines.db"):
        # Connect to SQLite database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Create a table to store used headlines if it doesn’t exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS headlines (
                id INTEGER PRIMARY KEY,
                headline TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def is_headline_used(self, headline):
        """Check if the headline is already in the database."""
        self.cursor.execute("SELECT 1 FROM headlines WHERE headline = ?", (headline,))
        return self.cursor.fetchone() is not None

    def add_headline(self, headline):
        """Add a headline to the database."""
        self.cursor.execute("INSERT INTO headlines (headline) VALUES (?)", (headline,))
        self.conn.commit()

    def delete_headline(self, headline):
        """Delete a headline from the database."""
        self.cursor.execute("DELETE FROM headlines WHERE headline = ?", (headline,))
        self.conn.commit()
        print(f"Deleted headline from database: {headline}")

    def close(self):
        """Close the database connection."""
        self.conn.close()
