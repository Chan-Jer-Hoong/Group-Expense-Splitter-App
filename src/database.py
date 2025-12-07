import psycopg2

class Database:

    ''' == Creating Tables == '''
    def create_user_table():
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Creating User Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                    user_id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    user_email_key TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    balance INTEGER,
                    date_joined DATE DEFAULT NOW()
                )
        """)

        # Commit changes to the sql server
        conn.commit()

        print("table created!")

        cur.close()
        conn.close()
    
    def create_group_member_table():
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Creating Group Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS group_members(
                    user_id INTEGER NOT NULL,
                    group_id INTEGER NOT NULL,
                    member_expense_id INTEGER NOT NULL,
                    date_joined DATE DEFAULT NOW(),
                    PRIMARY KEY(user_id, group_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (group_id) REFERENCES groups(group_id),
                    FOREIGN KEY (member_expense_id) REFERENCES member_expenses(member_expense_id)
                )
        """)

        # Commit changes to the sql server
        conn.commit()

        cur.close()
        conn.close()
    
    def create_group_table():
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Creating Group Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS groups(
                    group_id SERIAL PRIMARY KEY,
                    created_by INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    date_created DATE DEFAULT NOW(),
                    FOREIGN KEY (created_by) REFERENCES users(user_id)
                )
        """)

        # Commit changes to the sql server
        conn.commit()

        cur.close()
        conn.close()

    def create_expense_table():
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Creating Expense Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                    expense_id SERIAL PRIMARY KEY,
                    group_id INTEGER NOT NULL,
                    created_by INTEGER NOT NULL,
                    description TEXT,
                    date_created DATE DEFAULT NOW(),
                    FOREIGN KEY (created_by) REFERENCES users(user_id),
                    FOREIGN KEY (group_id) REFERENCES groups(group_id)
                )
        """)

        # Commit changes to the sql server
        conn.commit()

        cur.close()
        conn.close()

    def create_pending_invite_table():
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Creating pending invites Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pending_invites(
                    invite_id SERIAL PRIMARY KEY,
                    group_id INTEGER NOT NULL,
                    date_invited DATE DEFAULT NOW(),
                    FOREIGN KEY (group_id) REFERENCES groups(group_id)
                )
        """)

        # Commit changes to the sql server
        conn.commit()

        cur.close()
        conn.close()

    def create_member_expense_table():
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Creating pending invites Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS member_expenses(
                    member_expense_id SERIAL PRIMARY KEY,
                    expense_id INTEGER NOT NULL,
                    expense_amount FLOAT NOT NULL,
                    date_invited DATE DEFAULT NOW(),
                    FOREIGN KEY (expense_id) REFERENCES expenses(expense_id)
                )
        """)

        # Commit changes to the sql server
        conn.commit()

        cur.close()
        conn.close()

    ''' == Query Tables == '''

    def is_email_exist(user_email) -> bool:
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Search for if email exists
        cur.execute("""
            SELECT EXISTS(
                    SELECT user_email_key
                    FROM users 
                    WHERE user_email_key = %s
                )
        """, (user_email,))

        user_exists = cur.fetchone()[0]

        cur.close()
        conn.close()

        return user_exists

    def get_hashed_password(user_email) -> str:
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Search for password
        cur.execute("""
                SELECT user_email_key, password
                FROM users 
                WHERE user_email_key = %s
        """, (user_email,))

        hashed_password = cur.fetchone()[1]

        cur.close()
        conn.close()

        return hashed_password

    def get_user_id(user_email) -> int:
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Search for password
        cur.execute("""
                SELECT user_email_key, user_id
                FROM users 
                WHERE user_email_key = %s
        """, (user_email,))

        user_id = cur.fetchone()[1]

        cur.close()
        conn.close()

        return user_id

    def get_username(user_id) -> str:
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Search for password
        cur.execute("""
                SELECT user_id, name
                FROM users 
                WHERE user_id = %s
        """, (user_id,))

        username = cur.fetchone()[1]

        cur.close()
        conn.close()

        return username

    ''' == Insert Records == '''
    def insert_user(self, user_name, user_email, user_password):
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Insert user into table
        cur.execute("""
            INSERT INTO users (name, user_email_key, password)
            VALUES (%s, %s, %s)
        """, (user_name, user_email, user_password))

        # Commit changes to the sql server
        conn.commit()

        print("user inserted!")

        cur.close()
        conn.close()

    def insert_group_data(self, user_id, group_name):
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Insert group data
        cur.execute("""
            INSERT INTO groups (created_by, name)
            VALUES (%s, %s)
        """, (user_id, group_name))

        # Commit changes to the sql server
        conn.commit()

        print("group created!")

        cur.close()
        conn.close()

    ''' == Delete Records == '''

    ''' == Delete Tables == '''
    def delete_table():
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                                password="12345678", port="5432")

        cur = conn.cursor()

        # Creating User Table
        cur.execute("""
            DROP TABLE users, groups, group_members, expenses, pending_invites, member_expenses
        """)

        # Commit changes to the sql server
        conn.commit()

        print("table removed!")

        cur.close()
        conn.close()