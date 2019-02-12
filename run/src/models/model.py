from time import time
from pprint import pprint


from .opencursor import OpenCursor


def get_pk_from_username(username):
    """select statement to get pk from users table based on username"""
    with OpenCursor() as cur:
            SQL = """ SELECT pk FROM users WHERE username = ?; """
            cur.execute(SQL, (username,))
            row = cur.fetchone()
    return row['pk']


class User:
    def __init__(self, row={}, username='', password=''):
        if username:
            self._set_from_credentials(username, password)
        else:
            self._set_from_row(row)

    def _set_from_row(self, row):
        row = dict(row)
        self.pk = row.get('pk')
        self.username = row.get('username')
        self.password = row.get('password')
        self.display_name = row.get('display_name')
        self.email = row.get('email')

    def _set_from_credentials(self, username, password):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM users WHERE
                username = ? AND password = ?; """
            cur.execute(SQL, (username, password))
            row = cur.fetchone()
        if row:
            self._set_from_row(row)
        else:
            self._set_from_row({})

    def save(self):
        if self:
            with OpenCursor() as cur:
                SQL = """ UPDATE users SET 
                    username = ?, password = ?,
                    display_name = ?, email = ?
                    WHERE pk=?; """
                values = (self.username, self.password,
                self.display_name, self.email, self.pk)
                cur.execute(SQL, values)
        else:
            with OpenCursor() as cur:
                SQL = """ INSERT INTO users (
                    username, password, display_name, email)
                    VALUES (?, ?, ?, ?); """
                values = (self.username, self.password,
                          self.display_name, self.email)
                cur.execute(SQL, values)
                self.pk = cur.lastrowid


    def get_available_games(self):
        """get a list of all playable games"""
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM available_games ORDER BY game_name ASC;"""
            cur.execute(SQL)
            rows = cur.fetchall()
        return [dict(game_row) for game_row in rows]


    def get_user_active_games(self):
        """get a list of the user's games that are not finished"""
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM game_records WHERE participant_pk = ? AND
            game_state NOT LIKE 'WIN -%' ORDER BY game_pk ASC;"""
            cur.execute(SQL, (self.pk,))
            rows = cur.fetchall()
        return [GameStatus(game_row) for game_row in rows]

    
    def get_user_finished_games(self):
        """get a list of the user's games that are finished"""
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM game_records WHERE participant_pk = ? AND
            game_state LIKE 'WIN -%' ORDER BY game_pk ASC;"""
            cur.execute(SQL, (self.pk,))
            rows = cur.fetchall()
        return [GameStatus(game_row) for game_row in rows]


    def make_game(self, game_pk, turn_order):
        """takes in a game's identifier and the turn order and populates
        the game_records database for all fields of a new game"""
        playthrough_id = str(self.pk) + "-" + str(game_pk) + "-" + str(time())
        order_str = ','.join(map(str, turn_order))
        for player_pk in turn_order:
            game_info = {
                'game_pk': game_pk,
                'playthrough_id': playthrough_id,
                'game_state': 'START',
                'participant_pk': player_pk,
                'turn_order': order_str,
                'turn_number': 1
            }
            new_game = GameStatus(row=game_info)
            new_game.save()
        return playthrough_id


    def game_pk_from_id(self, game_id):
        """select statement to get pk from game_records table based on id"""
        with OpenCursor() as cur:
            SQL = """ SELECT pk FROM game_records WHERE playthrough_id = ? and participant_pk = ?; """
            cur.execute(SQL, (game_id, self.pk))
            row = cur.fetchone()
        return row['pk']


    def game_start_params(self, pk):
        """get game parameters from available_games table based on selection"""
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM available_games WHERE pk = ?;"""
            cur.execute(SQL, (pk,))
            row = cur.fetchone()
        return row


    def __bool__(self):
        return bool(self.pk)


class GameStatus:
    def __init__(self, row={}, pk=''):
        if pk:
            self._set_from_credentials(pk)
        else:
            self._set_from_row(row)


    def _set_from_credentials(self, pk):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM game_records 
                WHERE pk = ?; """
            cur.execute(SQL, (pk,))
            row = cur.fetchone()
        if row:
            self._set_from_row(row)
        else:
            self._set_from_row({})


    def _set_from_row(self, row):
        row = dict(row)
        self.pk = row.get('pk')
        self.game_pk = row.get('game_pk')
        self.playthrough_id = row.get('playthrough_id')
        self.game_state = row.get('game_state')
        self.participant_pk = row.get('participant_pk')
        self.turn_order = row.get('turn_order')
        self.turn_number = row.get('turn_number')
        self.endpoint = self.get_avlb_game_info()['endpoint']


    def save(self):
        if self:
            with OpenCursor() as cur:
                SQL = """ UPDATE game_records SET 
                          game_state = ?,  turn_number = ?
                          WHERE playthrough_id=?; """
                values = (self.game_state, self.turn_number, 
                          self.playthrough_id)
                cur.execute(SQL, values)
        else:
            with OpenCursor() as cur:
                SQL = """ INSERT INTO game_records (
                          game_pk, playthrough_id, game_state,
                          participant_pk, turn_order, turn_number)
                          VALUES (?, ?, ?, ?, ?, ?); """
                values = (self.game_pk, self.playthrough_id,
                          self.game_state, self.participant_pk, 
                          self.turn_order, self.turn_number)
                cur.execute(SQL, values)
                self.pk = cur.lastrowid


    def get_avlb_game_info(self):
        """pull information from the available_games
        table based on game_records game pk"""
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM available_games WHERE
                pk = ?; """
            cur.execute(SQL, (self.game_pk,))
            row = cur.fetchone()
        return row


    def __repr__(self):
        return self.get_avlb_game_info()['game_name'] + "|" + str(self.pk) + "|" + self.game_state + "|" + self.turn_order


    def __bool__(self):
        return bool(self.pk)