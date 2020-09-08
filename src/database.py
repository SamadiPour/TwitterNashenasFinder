import os
import sqlite3
from datetime import datetime


class DatabaseHelper:
    def __init__(self) -> None:
        super().__init__()

        if not os.path.exists('../unknown.db'):
            open('../unknown.db', 'w').close()

        self.connection = sqlite3.connect('../unknown.db')
        self.cursor = self.connection.cursor()

        self.create()
        self.connection.commit()

    def add_item(self, tweet, link):
        try:
            tweet_timestamp = datetime.timestamp(
                datetime.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S')
            )
            data_tuple = (
                tweet.user.id, tweet.user.screen_name,
                tweet.user.name, tweet.user.followers_count,
                tweet.user.friends_count, str(tweet.created_at),
                tweet_timestamp, link
            )

            user = self.find(tweet.user.id)
            if user is not None:
                saved_tweet_timestamp = user[6]
                if tweet_timestamp > saved_tweet_timestamp:
                    self.remove(tweet.user.id)
                else:
                    return

            self.insert(data_tuple)
            self.connection.commit()
        except sqlite3.IntegrityError:
            return

    def create(self):
        query = """
        create table IF NOT EXISTS unknown
        (
            user_id           INTEGER not null primary key unique,
            username          TEXT,
            user_display_name TEXT,
            followers         INTEGER,
            following         INTEGER,
            tweet_date        TEXT,
            tweet_timestamp   NUMERIC,
            link              TEXT
        );
        """
        self.cursor.execute(query)

    def insert(self, data):
        self.cursor.execute(
            "INSERT INTO unknown "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
            data
        )

    def remove(self, user_id):
        self.cursor.execute(
            f"DELETE FROM unknown "
            f"WHERE user_id = {user_id};"
        )

    def find(self, user_id):
        self.cursor.execute(
            f"SELECT * FROM unknown "
            f"WHERE user_id = {user_id};"
        )
        return self.cursor.fetchone()

    def get_all_dates(self):
        self.cursor.execute(
            "SELECT tweet_date FROM unknown "
            "ORDER BY tweet_timestamp"
        )
        return self.cursor.fetchall()
