#!/usr/bin/env python
import json
import os
from threading import Lock

import flask
from flask import Blueprint, render_template
from flask import Flask, session, request, copy_current_request_context
from flask_session import Session
from flask_socketio import SocketIO, emit, disconnect
from rasa.nlu.model import Interpreter

import messages
from geco_conversation import StartAction, Utils

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "gevent"

base_url = '/geco_agent/'
socketio_path = base_url + 'socket.io/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
# session config
# app.config['SESSION_FILE_DIR'] = 'flask_session'
# DEFAULT 31 days
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

Session(app)

# previous:
# socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*',
#                     ping_timeout= 5000000, manage_session=True)

# TODO check if we need cors_allowed_origins, I think we don't need anymore.
socketio = SocketIO(app, manage_session=False, async_mode=async_mode, cors_allowed_origins='*',
                    path=socketio_path, logger=False, engineio_logger=False, debug=False, )

simple_page = Blueprint('root_pages',
                        __name__,
                        static_folder='../frontend/dist/static',
                        template_folder='../frontend/dist')

thread = None
thread_lock = Lock()
interpreter = Interpreter.load("./model_dir/latest_model")

if not os.path.exists('logger.json'):
    with open('logger.json', 'w') as f:
        json.dump({}, f)


class ConversationDBExplore(object):

    def say(self, msg):
        self.bot_messages.append(msg)

    def clear_msgs(self):
        self.bot_messages = []

    def clear_entities(self):
        for key in self.entities.keys():
            del (session['tmp_' + str(key)])
        self.entities = {}

    def set_logic(self, logic_class):
        self.logic = logic_class
        self.logic.add_additional_status({k: session[k] for k in self.logic.required_additional_status()})
        messages, next_state, delta_status = self.logic.on_enter_messages()
        for m in messages:
            self.say(m)
        for k in delta_status:
            session[k] = delta_status[k]
        if next_state is not None:
            print(type(next_state), next_state)
            self.set_logic(next_state)

    def run(self, message, intent, entities):
        messages, next_state, delta_status = self.logic.run(message, intent, entities)
        for m in messages:
            self.say(m)
        for k in delta_status:
            session[k] = delta_status[k]
        if next_state is not None:
            print(type(next_state), next_state)
            self.set_logic(next_state)

    def __init__(self):
        self.user_message = {}
        self.bot_messages = []
        self.last_intent = None
        self.entities = {}
        self.logic = None
        self.geno_surf=None
        session['selected_dataset'] = []
        session['dataset_list'] = []

        self.say(Utils.chat_message(messages.initial_greeting))
        self.set_logic(StartAction({}))


@simple_page.route('/')
def index():
    flask.current_app.logger.info("serve index")
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/')
def index():
    flask.current_app.logger.info("serve index")
    return render_template('my_index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    user_message = message['data'].strip()
    messages = session['messages']
    messages.append('USER: ' + user_message)
    session['messages'] = messages

    data = json.loads(open("logger.json").read())
    data[request.sid].append(user_message)

    interpretation = interpreter.parse(user_message)
    intent = interpretation['intent']['name']
    entities = {}
    for e in interpretation['entities']:
        if e['entity'] in entities and e['value'] not in entities[e['entity']]:
            entities[e['entity']].append(e['value'])
        else:
            entities[e['entity']] = [e['value']]

    Utils.pyconsole_debug(intent)
    Utils.pyconsole_debug(entities)

    session['status'].run(user_message, intent, entities)

    for msg in session['status'].bot_messages:
        emit('json_response', msg)
        Utils.pyconsole_debug(msg)
        # TODO CHECK
        messages = session['messages']
        messages.append(msg['payload'])
        session['messages'] = messages

        if msg['type'] == 'message':
            data[request.sid].append(msg['payload'])

    with open("logger.json", "w") as file:
        json.dump(data, file)

    session['status'].clear_msgs()


# TODO: maybe here we need to manage the session storing
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('json_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)

@socketio.on('connect', namespace='/test')
def test_connect():
    if 'status' not in session:
        session['status'] = ConversationDBExplore()
        session['messages'] = []
    else:
        for x in session['messages']:
            if type(x) == str:
                emit('json_response', Utils.chat_message('Previous chat: ' + x))

    #TO PUT FOR SAVE EVERY CONVERSATION FROM ALL CONNECTIONS AND REMOVE data= {} and data[request.sid]=[]
    with open('logger.json', 'r') as f:
        data = json.load(f)
        data[request.sid]=[]
    #data = {}
    #data[request.sid] = []

    for msg in session['status'].bot_messages:
        emit('json_response', msg)
        messages = session['messages']
        messages.append(msg['payload'])
        session['messages'] = messages
        if msg['type']=='message':
            data[request.sid].append(msg['payload'])

    with open('logger.json', 'w') as file:
        json.dump(data, file)

    session['status'].clear_msgs()
    session['status'].clear_entities()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


app.register_blueprint(simple_page, url_prefix=base_url)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5980)
