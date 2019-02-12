import json
import requests


from flask import Blueprint,redirect,render_template,request,session,url_for


from ..models.model import *


controller = Blueprint('private',__name__)

@controller.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'GET':
        # receive json with key user_info which contains a dict with 
        # keys 'username', 'pk', 'email', and 'display_name'
        user_credentials = request.get_json()
        user = User(row=user_credentials['user_info'])
        # get list of games that can be created
        start_game_list = user.get_available_games()
        # get list of unfinished games user is involved with
        cur_game_list = user.get_user_active_games()
        # get list of finished games user has played
        fin_game_list = user.get_user_finished_games()
        return jsonify({'start_list':start_game_list,
                        'continue_list':cur_game_list,
                        'finished_list':fin_game_list})


@controller.route('/setup', methods=['GET','POST'])
def setup():
    if request.method == 'GET':
        """receive json with keys game_pk and user info :
        user_info contains a dict with keys 'username', 'pk',
        'email', and 'display_name'.
        game_pk is the pk of the game from the available_games table"""
        request = request.get_json()
        user = User(row=request['user_info'])
        game_params = user.game_start_params(pk=request['game_pk'])
        return jsonify({'game_params': game_params})
    elif request.method == 'POST':
        """receive json with keys game_params and user info :
        user_info contains a dict with keys 'username', 'pk',
        'email', and 'display_name'.
        game_params contains a dict with keys game_pk and user_list
        user_list has the pks of all users playing the game"""
        request = request.get_json()
        user = User(row=request['user_info'])
        user_list = request['game_params']['user_list']
        game_pk = request['game_params']['game_pk']
        game_id = user.make_game(game_pk, user_list)
        return jsonify({'game_id': game_id})


@controller.route('/gamepage', methods=['GET','POST'])
def gamepage():
    if request.method == 'GET':
        """receive json with keys game_id and user info :
        user_info contains a dict with keys 'username', 'pk',
        'email', and 'display_name'.
        game_id is the unique id of the game from the available_games table
        """
        request = request.get_json()
        user = User(row=request['user_info'])
        game_pk = user.game_pk_from_id(request['game_id'])
        game = GameStatus(pk=game_pk)
        game_state = game.game_state
        turn_order = game.turn_order.split(',')
        num_players = len(turn_order)
        turn_number = game.turn_number
        user_turn_id = turn_order[(turn_number % num_players)]
        if user_turn_id == str(user.pk):
            user_turn = "Yes"
        else:
            user_turn = "No"
        endpoint = game.endpoint
        response = requests.get(f"{endpoint}get", 
                                    json = {
                                        'state': game_state,
                                        'user_turn': user_turn,
                                        'players': turn_order,
                                        'turn_number': turn_number
                                    }
                                )
        html_to_pass = response.text
        return jsonify({'html': html_to_pass})
        
    elif request.method == 'POST':
        """receive json with keys game_params and user info :
        user_info contains a dict with keys 'username', 'pk',
        'email', and 'display_name'.
        game_params contains a dict with keys 'game_id' and 'next_state'
        game_id is the unique id of the game from the available_games table
        next_state is a string representing the state of the game after the
        most recent move"""
        request = request.get_json()
        user = User(row=request['user_info'])
        game_pk = user.game_pk_from_id(request['game_params']['game_id'])
        game = GameStatus(pk=game_pk)
        endpoint = game.endpoint
        game.game_state = request['game_params']['next_state']
        game.turn_number += 1
        # update DB for new info
        game.save()
        # win state will have the string "WIN -" in it
        if game.game_state.find("WIN -") > -1:
            return jsonify({'win': True})
        return jsonify({'win': False})