import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def select_times(self) -> dict[str, float]:
        table_name = 'times'
        with self.connection:
            return {
            name: duration / 1000.0
            for name, duration in self.cursor.execute(
                f"SELECT name, duration FROM {table_name}"
            ).fetchall()
        }

    def select_volumes(self) -> dict[str, int]:
        table_name = 'volumes'
        with self.connection:
            volume_list = self.cursor.execute(
                f"SELECT rsb, value FROM {table_name}"
                ).fetchall()
            return dict(volume_list)

    def update_volume_by_rsb(self, rsb, value):
        table_name = 'volumes'
        with self.connection:
            return self.cursor.execute(f"UPDATE {table_name} SET value = (?) WHERE rsb = {rsb}", (value,))


db = Database('settings.db')
print(db.select_times())