import json
import requests


from flask import Blueprint,redirect,render_template,request,session,url_for


from ..models.model import *


controller = Blueprint('private',__name__)

@controller.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'GET':
        # receive json with key user info which contains a dict with 
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
        user = User(row=session['user_dict'])
        game_params = user.game_start_params(pk=session['to_start'])
        # search for users to invite
        # choose the number of players/turn order
        return render_template('setup.html', params=game_params)
    elif request.method == 'POST':
        user = User(row=session['user_dict'])
        user_list = [user.pk]
        game_pk = request.form['game_pk']
        max_num = int(request.form['max_num'])
        for i in range(1, max_num):
            form_req = 'player ' + str(i)
            username = request.form.get(form_req)
            if username:
                player_pk = get_pk_from_username(username)
                user_list.append(player_pk)
        session['game'] = user.make_game(game_pk, user_list)
        # request.form['button']
        # use make_game method
        # set session['game'] off of the new entries
        return redirect(url_for('private.gamepage'))


@controller.route('/gamepage', methods=['GET','POST'])
def gamepage():
    if request.method == 'GET':
        user = User(row=session['user_dict'])
        game_pk = user.game_pk_from_id(session['game'])
        game = GameStatus(pk=game_pk)
        game_state = game.game_state
        turn_order = game.turn_order.split(',')
        num_players = len(turn_order)
        turn_number = game.turn_number
        user_turn_id = turn_order[(turn_number % num_players)]
        print(type(user_turn_id))
        print(type(user.pk))
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
        return render_template('game.html', html_to_pass = html_to_pass,
                                user=user.username)
    elif request.method == 'POST':
        user = User(row=session['user_dict'])
        game_pk = user.game_pk_from_id(session['game'])
        game = GameStatus(pk=game_pk)
        endpoint = game.endpoint
        game.game_state = request.form['next_state']
        # increment turn number for each move made
        game.turn_number += 1
        # get the game state back after being updated for the post request
        post_response = requests.post(f"{endpoint}post", 
                                        json = {'state': game.game_state})
        # update DB for new info
        game.save()
        # win state will have the string "WIN -" in it
        if game.game_state.find("WIN -") > -1:
            return redirect(url_for('game_end_page'))
        return redirect(url_for('private.gamepage'))