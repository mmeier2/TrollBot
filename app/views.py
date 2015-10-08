from flask import render_template, request
from app import app
from cli_chat import analyze_input

def chat_bot_response(name, title, db):
    if request.method == 'GET':
        return render_template('chat_bot.html',
                                title=title,
                                name=name)



    return analyze_input(request.form['text'], db)


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='ChatBot',
                           user=user)

@app.route('/office_bot', methods=['GET', 'POST'])
def office_bot():
    return chat_bot_response('office_bot', 'Office Bot', 1)

@app.route('/trailer_bot', methods=['GET', 'POST'])
def trailer_bot():
    return chat_bot_response('trailer_bot', 'Trailer Park Boys Bot', 0)
    
@app.route('/arrdev_bot', methods=['GET', 'POST'])
def arrdev_bot():
    return chat_bot_response('arrdev_bot', 'Arrested Development Bot', 2)
    
    