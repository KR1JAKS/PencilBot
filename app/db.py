import sqlite3 as sq
import random as rand
import datetime

async def db_start():
    db = sq.connect('pencils.db')
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS accounts(
                id INTEGER,
                chat_id INTEGER,
                username TEXT,
                score INTEGER DEFAULT 0,
                last_update DATE,
                next_update DATE,
                PRIMARY KEY(id, chat_id))''')
    db.commit()
    db.close()

async def point_pluse(user_id, chat_id):
    today = datetime.date.today()
    db = sq.connect('pencils.db')
    cur = db.cursor()
    cur.execute('SELECT score, last_update, next_update FROM accounts WHERE id = ? AND chat_id = ?', (user_id, chat_id))
    result = cur.fetchone()

    if result:
        score, last_update, next_update = result
        current_time = datetime.datetime.now()

        if next_update and current_time < datetime.datetime.strptime(next_update, '%Y-%m-%d %H:%M:%S'):
            db.close()
            return None
        
        if last_update != today:
            new_score = rand.randint(0, 10)
            if rand.random() < 0.3 and score >= 0:
                new_score = -rand.randint(1, 10)

            next_update_time = current_time + datetime.timedelta(days=1)
            cur.execute('UPDATE accounts SET score = ?, last_update = ?, next_update = ? WHERE id = ? AND chat_id = ?', 
                        (score + new_score, today, next_update_time.strftime('%Y-%m-%d %H:%M:%S'), user_id, chat_id))
            db.commit()
            db.close()
            return new_score, score + new_score
        db.close()
        return None
    db.close()

async def add_player(user_id, username, chat_id):
    db = sq.connect('pencils.db')
    cur = db.cursor()
    cur.execute('''
        INSERT INTO accounts (id, chat_id, username) VALUES (?, ?, ?)
        ON CONFLICT(id, chat_id) DO UPDATE SET username = ?
    ''', (user_id, chat_id, username, username))
    db.commit()
    db.close()

async def top(chat_id):
    db = sq.connect('pencils.db')
    cur = db.cursor()
    cur.execute('SELECT id, username, score FROM accounts WHERE chat_id = ? ORDER BY score DESC LIMIT 15', (chat_id,))
    players = cur.fetchall()
    db.close()
    return players

async def add_chat_id(chat_id):
    db = sq.connect('pencils.db')
    cur = db.cursor()
    cur.execute('INSERT OR IGNORE INTO accounts (chat_id) VALUES (?)', (chat_id,))
    db.commit()
    db.close()