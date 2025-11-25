# sql
import sqlite3
from datetime import datetime

DB = "tinytails.db"

# ---------------------------
# Table Creation
# ---------------------------
def create_table():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PetStats (
        user_id INTEGER PRIMARY KEY,
        user_name TEXT,
        pet_name TEXT,
        feed INTEGER DEFAULT 0,
        clean INTEGER DEFAULT 0,
        sleep INTEGER DEFAULT 0,
        happy INTEGER DEFAULT 0,
        xp_earned INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        score INTEGER DEFAULT 0,
        last_updated DATETIME
    )
    ''')
    conn.commit()
    conn.close()

# ---------------------------
# Helper Functions
# ---------------------------
def create_new_pet(user_id, user_name, pet_name):
    """Insert new pet entry if not exists."""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO PetStats (
        user_id, user_name, pet_name, feed, clean, sleep, happy, xp_earned, level, score, last_updated
    ) VALUES (?, ?, ?, 0, 0, 0, 0, 0, 1, 0, ?)
    ''', (user_id, user_name, pet_name, datetime.now()))
    conn.commit()
    conn.close()

def add_xp(user_id, xp_gain):
    """Add XP and handle level-up logic."""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT xp_earned, level FROM PetStats WHERE user_id=?", (user_id,))
    result = cursor.fetchone()

    if result:
        xp, level = result
        xp += xp_gain

        # Check level-up
        while xp >= level * 100:
            xp -= level * 100
            level += 1

        cursor.execute("UPDATE PetStats SET xp_earned=?, level=?, last_updated=? WHERE user_id=?",
                       (xp, level, datetime.now(), user_id))
        conn.commit()

    conn.close()

# ---------------------------
# Pet Actions
# ---------------------------
def feed_pet(user_id, user_name, pet_name, times=1):
    create_new_pet(user_id, user_name, pet_name)
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute('UPDATE PetStats SET feed = feed + ?, last_updated=? WHERE user_id=?',
                   (times, datetime.now(), user_id))
    conn.commit()
    conn.close()

    add_xp(user_id, times * 10)  # Feeding gives XP


def clean_pet(user_id, user_name, pet_name, times=1):
    create_new_pet(user_id, user_name, pet_name)
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute('UPDATE PetStats SET clean = clean + ?, last_updated=? WHERE user_id=?',
                   (times, datetime.now(), user_id))
    conn.commit()
    conn.close()

    add_xp(user_id, times * 5)  # Cleaning gives less XP


def sleep_pet(user_id, user_name, pet_name, times=1):
    create_new_pet(user_id, user_name, pet_name)
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute('UPDATE PetStats SET sleep = sleep + ?, last_updated=? WHERE user_id=?',
                   (times, datetime.now(), user_id))
    conn.commit()
    conn.close()

    add_xp(user_id, times * 8)  # Sleeping gives XP


def play_game(user_id, user_name, pet_name, session_score=0, times=1):
    create_new_pet(user_id, user_name, pet_name)
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Update happiness
    cursor.execute('UPDATE PetStats SET happy = happy + ?, last_updated=? WHERE user_id=?',
                   (times, datetime.now(), user_id))

    # Check high score
    cursor.execute("SELECT score FROM PetStats WHERE user_id=?", (user_id,))
    current_score = cursor.fetchone()[0]
    if session_score > current_score:
        cursor.execute("UPDATE PetStats SET score=?, last_updated=? WHERE user_id=?",
                       (session_score, datetime.now(), user_id))

    conn.commit()
    conn.close()

    add_xp(user_id, times * 15)  # Playing gives more XP


# ---------------------------
# Fetch / Print Stats
# ---------------------------
def get_pet_stats(user_id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PetStats WHERE user_id=?', (user_id,))
    stats = cursor.fetchone()
    conn.close()
    return stats

def print_pet_stats(user_id):
    stats = get_pet_stats(user_id)
    if stats is None:
        print("No stats found.")
        return

    (user_id, user_name, pet_name, feed, clean, sleep, happy,
     xp_earned, level, score, last_updated) = stats

    print("------ PET STATS ------")
    print(f"User ID: {user_id}")
    print(f"User Name: {user_name}")
    print(f"Pet Name: {pet_name}")
    print(f"Feed: {feed}")
    print(f"Clean: {clean}")
    print(f"Sleep: {sleep}")
    print(f"Happiness: {happy}")
    print(f"XP: {xp_earned}")
    print(f"Level: {level}")
    print(f"High Score: {score}")
    print(f"Last Updated: {last_updated}")
    print("-----------------------")


# ---------------------------
# Initialize DB on import
# ---------------------------
create_table()