import sqlite3

def run(dbname="game.db"):
    conn = sqlite3.connect(dbname)
    cur  = conn.cursor()

    USER_SQL = """INSERT INTO users (
                display_name,
                email,
                username,
                password
            ) 
                VALUES (?, ?, ?, ?); """

    
    GAME_SQL = """INSERT INTO available_games (
                game_name,
                minimum_num_players,
                maximum_num_players,
                description,
                image,
                endpoint
            ) 
                VALUES (?, ?, ?, ?, ?, ?); """


    GAME_RECORDS_SQL = """INSERT INTO game_records (
                game_pk,
                playthrough_id,
                game_state,
                participant_pk,
                turn_order,
                turn_number
            ) 
                VALUES (?, ?, ?, ?, ?, ?); """
    
    sql_values_1 = ('Henry','email@domain.com','henry','white')
    sql_values_2 = ('Chase','email@domain.com','chase','ahn')
    sql_values_3 = ('Serik','email@domain.com','serdar','durbayev')
    sql_values_4 = (1, '1', '1', 1, '1,2', 1)
    sql_values_5 = (1, '1', '1', 2, '1,2', 1)
    sql_values_6 = ('test_game', 1, 3, 'Turn incrementing game to test multiplayer functionality from an external source', 'test_game.png', 'http://127.0.0.1:5001/')
    sql_values_7 = ('test_game2', 1, 3, 'Game2 for testing methods', 'test_game.png', 'http://127.0.0.1:5002/')
    sql_values_8 = ('test_game3', 1, 3, 'Game3 for testing methods', 'test_game.png', 'http://127.0.0.1:5003/')
    sql_values_9 = (2, '1', 'START', 2, '3,2', 1)
    sql_values_10 = (3, '1', 'START', 1, '1,3', 1)
    sql_values_11 = (3, '1', 'WIN - ME', 1, '1,3', 1)


    cur.execute(USER_SQL, sql_values_1)
    cur.execute(USER_SQL, sql_values_2)
    cur.execute(USER_SQL, sql_values_3)
    cur.execute(GAME_RECORDS_SQL, sql_values_4)
    cur.execute(GAME_RECORDS_SQL, sql_values_5)
    cur.execute(GAME_SQL, sql_values_6)
    cur.execute(GAME_SQL, sql_values_7)
    cur.execute(GAME_SQL, sql_values_8)
    cur.execute(GAME_RECORDS_SQL, sql_values_9)
    cur.execute(GAME_RECORDS_SQL, sql_values_10)
    cur.execute(GAME_RECORDS_SQL, sql_values_11)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    run()