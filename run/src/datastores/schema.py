import sqlite3

CON = None
CUR = None

def setup(dbname="game.db"):
    global CON
    global CUR
    CON = sqlite3.connect(dbname)
    CUR = CON.cursor()

def run(dbname="game.db"):
    SQL = "DROP TABLE IF EXISTS users;"
    
    CUR.execute(SQL)
    
    SQL = """CREATE TABLE users(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        display_name VARCHAR,
        email VARCHAR,
        username VARCHAR,
        password VARCHAR,
        CONSTRAINT unique_name UNIQUE(username)
        );"""
    
    CUR.execute(SQL)
    

    SQL = "DROP TABLE IF EXISTS available_games;"
    
    CUR.execute(SQL)
    
    SQL = """CREATE TABLE available_games(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        game_name VARCHAR,
        minimum_num_players INTEGER,
        maximum_num_players INTEGER,
        description VARCHAR,
        image VARCHAR,
        endpoint VARCHAR
        );"""
    
    CUR.execute(SQL)

    
    SQL = "DROP TABLE IF EXISTS game_records;"
    
    CUR.execute(SQL)
    
    SQL = """CREATE TABLE game_records(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        game_pk INTEGER,
        playthrough_id VARCHAR,
        game_state VARCHAR,
        participant_pk INTEGER,
        turn_order VARCHAR,
        turn_number INTEGER,
        FOREIGN KEY(participant_pk) REFERENCES users(pk),
        FOREIGN KEY(game_pk) REFERENCES available_games(pk)
        );"""
    
    CUR.execute(SQL)


    CON.commit()
    CUR.close()
    CON.close()


if __name__ == "__main__":
    setup()
    run()