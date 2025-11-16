import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="leads.db"):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                company TEXT,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_contacted TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                lead_id INTEGER,
                message TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(lead_id) REFERENCES leads(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_lead(self, name, email, company):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO leads (name, email, company) VALUES (?, ?, ?)',
            (name, email, company)
        )
        conn.commit()
        lead_id = cursor.lastrowid
        conn.close()
        return lead_id
    
    def get_leads(self, status='new'):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM leads WHERE status = ?', (status,))
        leads = cursor.fetchall()
        conn.close()
        return leads
    
    def update_lead_status(self, lead_id, status):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE leads SET status = ?, last_contacted = ? WHERE id = ?',
            (status, datetime.now(), lead_id)
        )
        conn.commit()
        conn.close()
    
    def save_message(self, lead_id, message):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO messages (lead_id, message) VALUES (?, ?)',
            (lead_id, message)
        )
        conn.commit()
        conn.close()
