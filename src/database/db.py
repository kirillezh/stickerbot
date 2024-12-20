"""
This module contains the Database class for managing the database operations.
"""
import sqlite3
import logging

class Database:
    """Class for database operations"""
    def __init__(self):
        self.conn = sqlite3.connect('bot_data.db')
        self.create_tables()

    def create_tables(self):
        """Create tables if they don't exist"""
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'ua'
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_packs (
            pack_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            pack_name TEXT NOT NULL,
            pack_title TEXT NOT NULL,
            pack_type TEXT CHECK(pack_type IN ('static', 'animated', 'video')) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_settings(user_id),
            UNIQUE(user_id, pack_name)
        )
        ''')
        self.conn.commit()

    async def get_user_language(self, user_id: int) -> str:
        """Get user language"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT language FROM user_settings WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 'ua'

    async def set_user_language(self, user_id: int, language: str):
        """Set user language"""
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO user_settings (user_id, language)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET language = ?
        ''', (user_id, language, language))
        self.conn.commit()

    async def create_pack(
            self,
            user_id: int,
            pack_name: str,
            pack_title: str,
            pack_type: str
    ) -> bool:
        """Create pack"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO user_packs (user_id, pack_name, pack_title, pack_type)
            VALUES (?, ?, ?, ?)
            ''', (user_id, pack_name, pack_title, pack_type))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    async def get_user_packs(self, user_id: int) -> list:
        """Get user packs"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM user_packs WHERE user_id = ?', (user_id,))
        return cursor.fetchall()

    async def get_pack(self, user_id: int, pack_name: str) -> tuple:
        """Get pack by user_id and pack_name
        Returns tuple: (pack_id, user_id, pack_name, pack_title, pack_type, created_at)
        """
        cursor = self.conn.cursor()
        try:

            cursor.execute('''
                SELECT pack_id, user_id, pack_name, pack_title, pack_type, created_at
                FROM user_packs
                WHERE user_id = ? AND pack_name = ?
            ''', (user_id, pack_name))

            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            logging.error("Database error: %s", str(e))
            return None

    async def delete_pack(self, user_id: int, pack_name: str) -> bool:
        """Delete pack"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('DELETE FROM user_packs WHERE user_id = ? AND pack_name = ?',
                          (user_id, pack_name))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    async def rename_pack(self, user_id: int, pack_name: str, new_title: str) -> bool:
        """Rename pack"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                UPDATE user_packs
                SET pack_title = ?
                WHERE user_id = ? AND pack_name = ?
            ''', (new_title, user_id, pack_name))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False
