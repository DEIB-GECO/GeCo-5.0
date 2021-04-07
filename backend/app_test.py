#!/usr/bin/env python
import json
import os
import flask
import time
from threading import Lock
import copy
import threading
from multiprocessing import Process
from flask import Blueprint, render_template
from flask import Flask, session, request, copy_current_request_context
from flask_session import Session
from flask_socketio import SocketIO, emit, disconnect
from rasa.nlu.model import Interpreter

from engineio.payload import Payload
from flask import Flask
from geco_conversation import *
from flask_executor import Executor
from waitress import serve

Payload.max_decode_packets = 10000
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "gevent"
#async_mode = "eventlet"
#async_mode= "threading"

if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    #monkey.patch_all()
    monkey.patch_all()#(thread=False, socket=False)

base_url = '/geco_agent/'
socketio_path = base_url + 'socket.io/'
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
# session config
# app.config['SESSION_FILE_DIR'] = 'flask_session'
# DEFAULT 31 days
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

# Load the model
interpreter = Interpreter.load("./model_dir/latest_model")
Session(app)
#executor = Executor(app)
# previous:
# socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*',
#                     ping_timeout= 5000000, manage_session=True)

# TODO check if we need cors_allowed_origins, I think we don't need anymore.
socketio = SocketIO(app, manage_session=False, async_mode=async_mode, cors_allowed_origins='*',
                    path=socketio_path, logger=False, engineio_logger=False, debug=False,pingTimeout= 5000)


simple_page = Blueprint('root_pages',
                        __name__,
                        static_folder='../frontend/dist/static',
                        template_folder='../frontend/dist')

thread = None
thread_lock = Lock()


# Creation of logger file to save conversations
if not os.path.exists('logger.json'):
    with open('logger.json', 'w') as f:
        json.dump({}, f)



# Creation of the main class of Dialogue Manager
class ConversationDBExplore(object):
    def __init__(self,sid):
        # Creation of the context
        self.bot_msgs = [Utils.chat_message(messages.initial_greeting)]
        # Add first step to the context to start chatting
        # Launch the conversation
        self.enter()

    def clear_msgs(self):
        self.bot_msgs = []

    # To call each time no messages are needed to pass from one action to the other
    def enter(self):
        self.bot_msgs.append(Utils.chat_message('What do you want?'))
        # Run the last action in the context

    # To call each time to run the needed action
    def run(self, message, intent, entities):
        self.bot_msgs.append(Utils.chat_message('Ok'))

    # To receive the messages from the user
    def receive(self, message):
        # Classify intent and extract entities
        interpretation = interpreter.parse(message)
        intent = interpretation['intent']['name']


        entities = {}
        for e in interpretation['entities']:
            if e['entity'] in entities and e['value'].lower().strip() not in entities[e['entity']]:
                entities[e['entity']].append(e['value'].lower().strip())
            else:
                entities[e['entity']] = [e['value'].lower().strip()]

        Utils.pyconsole_debug(intent)
        Utils.pyconsole_debug(entities)

        #time.sleep(3)
        self.run(message, intent, entities)


@simple_page.route('/')
def index():
    flask.current_app.logger.info("serve index")
    return render_template('index.html', async_mode=socketio.async_mode)


# Receive messages from user
@socketio.on('my_event', namespace='/test')
def test_message(message):
    # Read user message
    user_message = message['data'].strip()

    # Add messages to the session to save them in case of disconnection
    add_session_message(session, {'type': 'message', 'payload': {'text': user_message, 'sender': 'user'}})

    # Read the logger and save messages for improving nlu
    data = json.loads(open("logger.json").read())
    data[request.sid].append(user_message)

    error_to_raise = None
    try:
        # Call the dialogue manager that receive the message, interprets it and pass it to the correct action
        session['dm'].receive(user_message)
        # if (session['dm'].context.top_bot_msgs()!=None):
    except Exception as e:
        #session['dm'].context.add_bot_msg(Utils.chat_message("Something bad has happened, please start from beginning..."))
        error_to_raise = e

    Utils.wait_msg('iniziato thread ')
    def f():
        a=0
        while a<100000000:
            a+=1
            if a%10000000==0:
                #Utils.wait_msg('thread ' + str(a))
                #socketio.sleep(1)
                print('THREAD', a)
    #x = executor.submit(f)
    # x.result()
    #x = threading.Thread(target= f)
    #x.start()
    #x.join()
    #x = socketio.start_background_task(target=f)
    #print(type(x))
    #print(x.__dict__)
    #global thread
    #with thread_lock:
    #    if thread is None:
    #        thread = socketio.start_background_task(target=f)
        #thread.join()
    #while True:
    #    if x.is_alive():
    #        socketio.sleep(1)
    #    else:
    #        break



    # For each message in the top of the stack, we add it to the session and we send it to the user
    #print(session['dm'].context.top_bot_msgs())
    for msg in session['dm'].bot_msgs:
        id = add_session_message(session, msg)
        msg['message_id'] = id
        emit('json_response', msg)

        # If the msg is textual, we add it to the logger
        if msg['type'] == 'message':
            data[request.sid].append(msg['payload']['text'])
        with open("logger.json", "w") as file:
            json.dump(data, file)

    if error_to_raise:
        raise error_to_raise


    # session['status'].clear_msgs()
    # session['previous_intent']= intent

# To add the messages with an id to the session
def add_session_message(session, message):
    msg = session['messages']
    if len(msg) == 0:
        id = 0
    else:
        id = msg[-1]['message_id'] + 1

    if (message['type'] == "message"):
        payload = message['payload']
        msg.append({'sender': payload['sender'], 'text': payload['text'], 'message_id': id})
        session['messages'] = msg
    elif (message['type'] not in ['tools_setup']):
        temp_d = dict(message)
        temp_d['message_id'] = id
        session['last_json'][message['type']] = temp_d
    # elif (message['type']=='workflow'):
    #     temp_d = dict(message)
    #     temp_d['message_id'] = id
    #     if message['type'] not in session['last_json']:
    #         session['last_json'][message['type']] = [temp_d]
    #     session['last_json'][message['type']].append(temp_d)
    else:
        for x in message['payload']['remove']:
            print(session['last_json'].keys())
            keys_copy = [i for i in session['last_json'].keys()]
            if x in keys_copy:
                del session['last_json'][x]

    return id

#Get message id
def get_id(message):
    return message['message_id']

# Receive ack message and send the messages after the received ack number
# If -1 then from the beginning
@socketio.on('ack', namespace='/test')
def test_ack_message(message):
    print('ACKKKK ', message)
    # Check id of ack message received
    user_message = int(message['message_id'])

    if 'messages' in session:
        # If -1 we send all the messages in the conversation
        # if user_message == -1:
        #     for x in session['messages']:
        #         emit('json_response',
        #              {"type": "message", "payload": {'sender': x['sender'], 'text': x['text']},
        #               'message_id': x['message_id']})
        #     for x in session['last_json']:
        #         emit('json_response', session['last_json'][x])
        #
        # # Else we send from user_message + 1
        # else:
        last_msgs = [x for x in session['messages'] if x['message_id'] >= user_message + 1]
        for x in last_msgs:
            #if x['message_id'] > user_message + 1:
            emit('json_response',
                 {"type": "message", "payload": {'sender': x['sender'], 'text': x['text']},
                  'message_id': x['message_id']})

        last_json = [x for x in session['last_json'] if session['last_json'][x]['message_id'] >= user_message + 1]
        for x in last_json:
        #     if session['last_json'][x]['message_id'] > user_message + 1:
            emit('json_response', session['last_json'][x])

        #
        #
        # print(last_json)
        # workflow = list(filter(lambda i: i['type'] == 'workflow', last_json))
        # for i in workflow:
        #     emit('json_response',  workflow[i])
        # types = set([i['type'] for i in last_json if type!='workflow'])
        # for t in types:
        #     choice = list(filter(lambda i: i['type'] == t, last_json))[-1]
        #     emit('json_response', choice)




# Receive reset message
@socketio.on('reset', namespace='/test')
def reset_button(message):
    print('RESETTTTTTT ', message)
    # Empty the logger for that session id
    with open('logger.json', 'r') as f:
        data = json.load(f)
        data[request.sid] = []

    # Call function to reset the session
    reset(session, True)

    for msg in session['dm'].bot_msgs:
        id = add_session_message(session, msg)
        msg['message_id'] = id
        emit('json_response', msg)
    with open("logger.json", "w") as file:
        json.dump(data, file)

    # session['status'].clear_msgs()


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

# Reset the session
def reset(session, bool=False):
    # Delete everything in the session
    for k in list(session.keys()):
        if not k.startswith("_"):
            del session[k]

    # Starts a list of textual messages, a dict of visual messages and a dialogue manager
    session['messages'] = []
    session['last_json'] = {}
    session['dm'] = ConversationDBExplore(request.sid)

    # add the initial messages to the session
    if not bool:
        for msg in session['dm'].bot_msgs:
            id = add_session_message(session, msg)
            msg['message_id'] = id
            # emit('json_response', msg)

# Receive a new connection from the user
@socketio.on('connect', namespace='/test')
def test_connect():
    # If it is the first time that cookie appears we start from the beginning by calling reset
    if 'dm' not in session:
        reset(session)

    # TO PUT FOR SAVE EVERY CONVERSATION FROM ALL CONNECTIONS AND REMOVE data= {} and data[request.sid]=[]
    with open('logger.json', 'r') as f:
        data = json.load(f)
        data[request.sid] = []
    # data = {}
    # data[request.sid] = []
    if session['dm'].bot_msgs != None:
        for msg in session['dm'].bot_msgs:
            if msg['type'] == 'message':
                data[request.sid].append(msg['payload']['text'])

    with open('logger.json', 'w') as file:
        json.dump(data, file)

    # session['status'].clear_msgs()
    # session['status'].clear_entities()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


app.register_blueprint(simple_page, url_prefix=base_url)

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=5980)
