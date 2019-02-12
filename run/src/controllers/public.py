from flask import Blueprint,redirect,render_template,request,session,url_for


from ..models.model import *


controller = Blueprint('public',__name__)

@controller.route('/', methods=['GET','POST'])
def frontpage():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        if request.form['button'] == 'Login':
            username = request.form['Username']
            password = request.form['Password']
            user = User(username=username, password=password)
            if user:
                session['user_dict'] = {'username':user.username, 'pk':user.pk,
                                        'display_name':user.display_name,
                                        'email':user.email}
                return redirect(url_for('private.dashboard'))
            else:
                return redirect(url_for('public.frontpage'))
        elif request.form['button'] == 'Register New Account':
            return redirect(url_for('public.registration'))


@controller.route('/registration', methods=['GET','POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        disp_name = request.form['Display Name']
        email = request.form['Email']
        user_dict = {'username':username, 'password':password,
                    'display_name':disp_name, 'email':email}
        new_user = User(row=user_dict)
        new_user.save()
        return redirect(url_for('public.frontpage'))
