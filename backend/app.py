#!/usr/bin/env python
import json
import os
import flask
from threading import Lock
from flask import Blueprint, render_template
from flask import Flask, session, request, copy_current_request_context
from flask_session import Session
from flask_socketio import SocketIO, emit, disconnect
from rasa.nlu.model import Interpreter
from data_structure.database import get_db_uri, db, database
from geco_conversation import *
from data_structure.context import Context

from engineio.payload import Payload

Payload.max_decode_packets = 10000
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "gevent"

base_url = '/geco_agent/'
socketio_path = base_url + 'socket.io/'

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db.init_app(app)

app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
# session config
# app.config['SESSION_FILE_DIR'] = 'flask_session'
# DEFAULT 31 days
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
interpreter = Interpreter.load("./model_dir/latest_model")

Session(app)

# previous:
# socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*',
#                     ping_timeout= 5000000, manage_session=True)

# TODO check if we need cors_allowed_origins, I think we don't need anymore.
socketio = SocketIO(app, manage_session=False, async_mode=async_mode, cors_allowed_origins='*',
                    path=socketio_path, logger=False, engineio_logger=False, debug=False)


simple_page = Blueprint('root_pages',
                        __name__,
                        static_folder='../frontend/dist/static',
                        template_folder='../frontend/dist')

thread = None
thread_lock = Lock()


if not os.path.exists('logger.json'):
    with open('logger.json', 'w') as f:
        json.dump({}, f)

all_db = database()

class ConversationDBExplore(object):

    def __init__(self):
        #all_db = database()
        self.context = Context(all_db)
        #session['context']=self.context
        self.context.add_step(bot_msgs=Utils.chat_message(messages.initial_greeting), action= StartAction(self.context))
        self.enter()

    def clear_msgs(self):
        self.bot_messages = []

    def enter(self):
        node, on_enter = self.context.top_action().on_enter()
        if node==None:
            self.context.add_step(action=self.context.top_action())
        else:
            self.context.add_step(action=node)
            if on_enter:
                self.enter()


    def run(self, message, intent, entities):
        next_state, enter = self.context.top_action().run(message, intent, entities)
        if next_state is not None:
            self.context.add_step(action=next_state)
            if enter:
                self.enter()
        else:
            self.context.add_step(action=self.context.top_action())


    def receive(self, message):
        interpretation = interpreter.parse(message)
        intent = interpretation['intent']['name']
        # if intent == 'reset_session':
        #     session['dm'].context.add_bot_msg(Utils.chat_message('Are you sure to reset the session?'))
        #     session['previous_intent'] = 'reset_session'
        # elif session.get('previous_intent') == 'reset_session':
        #     if intent == 'affirm':
        #         reset(session)
        #     elif intent == 'deny':
        #         session['dm'].context.add_bot_msg(Utils.chat_message('Ok, I don\'t reset the session.\n The last message was:'))
        #         session['dm'].context.add_bot_msg(Utils.chat_message(session['messages'][-4]['text']))
        #     else:
        #         session['dm'].context.add_bot_msg(Utils.chat_message('Sorry, I didn\'t understand.\n Are you sure to reset the session?'))
        # elif intent == 'back':
        if intent == 'back':
            self.context.pop()
        else:
            self.context.add_user_msg(message)
            entities = {}
            for e in interpretation['entities']:
                if e['entity'] in entities and e['value'].lower().strip() not in entities[e['entity']]:
                    entities[e['entity']].append(e['value'].lower().strip())
                else:
                    entities[e['entity']] = [e['value'].lower().strip()]
            #Utils.pyconsole_debug(intent)
            #Utils.pyconsole_debug(entities)
            self.context.modify_status(entities)
            self.run(message, intent, entities)

@simple_page.route('/')
def index():
    flask.current_app.logger.info("serve index")
    return render_template('index.html', async_mode=socketio.async_mode)

#@app.route('/')
#def index():
 #   flask.current_app.logger.info("serve index")
 #   return render_template('my_index.html', async_mode=socketio.async_mode)

@socketio.on('my_event', namespace='/test')
def test_message(message):
    user_message = message['data'].strip()
    add_session_message(session, {'type':'message', 'payload':{'text':user_message, 'sender':'user'}})

    data = json.loads(open("logger.json").read())

    data[request.sid].append(user_message)
    session['dm'].receive(user_message)
    #if (session['dm'].context.top_bot_msgs()!=None):
    for msg in session['dm'].context.top_bot_msgs():
        id = add_session_message(session, msg)
        msg['message_id'] = id
        emit('json_response', msg)

        if msg['type'] == 'message':
            data[request.sid].append(msg['payload']['text'])
   # with open("logger.json", "w") as file:
       # json.dump(data, file)

    #session['status'].clear_msgs()
    #session['previous_intent']= intent

def add_session_message(session, message):

    msg = session['messages']
    if len(msg)==0:
        id = 0
    else:
        id = msg[-1]['message_id']+1

    if (message['type'] == "message"):
        payload = message['payload']
        msg.append({'sender': payload['sender'], 'text': payload['text'], 'message_id':id})
        session['messages'] = msg
    elif (message['type']!='tools_setup'):
        temp_d = dict(message)
        temp_d['message_id'] = id
        session['last_json'][message['type']] = temp_d
    else:
        for x in message['payload']['remove']:
            if x in session['last_json']:
                del session['last_json'][x]

    return id


@socketio.on('ack', namespace='/test')
def test_ack_message(message):
    user_message = int(message['message_id'])
    print(user_message)
    if 'messages' in session:
        if user_message == -1:
            for x in session['messages']:
                emit('json_response',
                     {"type": "message", "payload": {'sender': x['sender'], 'text': x['text']}, 'message_id': x['message_id']})
            for x in session['last_json']:
                emit('json_response', session['last_json'][x])
        else:
            for x in session['messages']:
                if x['message_id']> user_message+1:
                    emit('json_response',
                         {"type": "message", "payload": {'sender': x['sender'], 'text': x['text']}, 'message_id': x['message_id']})

            for x in session['last_json']:
                if session['last_json'][x]['message_id'] > user_message+1:
                    emit('json_response', session['last_json'][x])


@socketio.on('reset', namespace='/test')
def reset_button(message):
    with open('logger.json', 'r') as f:
        data = json.load(f)
        data[request.sid] = []
    reset(session)

        #emit('json_response', msg)
    #with open("logger.json", "w") as file:
    #    json.dump(data, file)

    #session['status'].clear_msgs()

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

def reset(session):
    for k in list(session.keys()):
        if not k.startswith("_"):
            del session[k]
    session['messages'] = []
    session['last_json'] = {}
    session['dm']= ConversationDBExplore()

    for msg in session['dm'].context.top_bot_msgs():
        id = add_session_message(session, msg)
        msg['message_id'] = id



@socketio.on('connect', namespace='/test')
def test_connect():
    if 'dm' not in session:
        reset(session)

    # TO PUT FOR SAVE EVERY CONVERSATION FROM ALL CONNECTIONS AND REMOVE data= {} and data[request.sid]=[]
    with open('logger.json', 'r') as f:
        data = json.load(f)
        data[request.sid] = []
    # data = {}
    # data[request.sid] = []
    if session['dm'].context.top_bot_msgs()!=None:
        for msg in session['dm'].context.top_bot_msgs():
            if msg['type'] == 'message':
                data[request.sid].append(msg['payload']['text'])

    with open('logger.json', 'w') as file:
        json.dump(data, file)

    #session['status'].clear_msgs()
    #session['status'].clear_entities()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


app.register_blueprint(simple_page, url_prefix=base_url)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5980)