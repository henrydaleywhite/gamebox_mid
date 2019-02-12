import json
import requests


from flask import Flask,redirect,render_template,request,session,url_for, jsonify


from .controllers.public import controller as public
from .controllers.private import controller as private


UPLOADS_FOLDER = '/mnt/c/Users/Henry/desktop/byte/week6/ipfs_testing/new_test/run/src/static'

app = Flask(__name__, static_folder = 'static')

app.register_blueprint(public)
app.register_blueprint(private)

app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER
app.secret_key = 'very secret1'

# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html')


# @app.route('/', methods=['GET','POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     elif request.method == 'POST':
#         session['user'] = request.form['username']
#         return redirect(url_for('dashboard'))


# @app.route('/dashboard', methods=['GET', 'POST'])


# # @app.route('/game', methods=['GET','POST'])
# # def gamepage():
# #     if request.method == 'GET':
# #         # TODO dynamic gameid from session
# #         gameid='1'
# #         # get game state record from DB for current player
# #         game_row = get_game_info_for_cur_player(session['user'], gameid)
# #         game_state = game_row['game_state']
# #         # create a list with the turn order
# #         turn_order = game_row['turn_order'].split(',')
# #         num_players = len(turn_order)
# #         session['turn_number'] = game_row['turn_number']
# #         user_turn_id = turn_order[(session['turn_number'] % num_players)]
# #         if user_turn_id == session['user']:
# #             user_turn = "Yes"
# #         else:
# #             user_turn = "No"
# #         response = requests.get(f"{endpoint}get", 
# #                                     json = {
# #                                         'state': game_state,
# #                                         'user_turn': user_turn,
# #                                         'players': turn_order,
# #                                         'turn_number': session['turn_number']
# #                                     }
# #                                 )
# #         html_stuff = response.text
# #         return render_template('index.html', html_stuff = html_stuff,
# #                                 user=session['user'])
# #     elif request.method == 'POST':
# #         testvar = request.form['test']
# #         # TODO dynamic gameid from session
# #         gameid='1'
# #         # increment turn number for each move made
# #         session['turn_number'] += 1
# #         # get the game state back after being updated for the post request
# #         post_response = requests.post(f"{endpoint}post", 
# #                                         json = {'state': testvar})
# #         # update DB for new info
# #         update_game_info(testvar, session['turn_number'], gameid)
# #         # win state will have the string "WIN -" in it
# #         if testvar.find("WIN -") > -1:
# #             return redirect(url_for('game_end_page'))
# #         return redirect(url_for('gamepage'))