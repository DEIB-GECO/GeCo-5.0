import logging
import uuid
from typing import Any, Awaitable, Callable, Dict, Iterable, List, Optional, Text

from rasa.core.channels.channel import InputChannel, OutputChannel, UserMessage
import rasa.shared.utils.io
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from socketio import AsyncServer

import json

tracker= False
user_ID=""

logger = logging.getLogger(__name__)

def write_json(data2,filename):
    with open(filename,"w") as f:
        json.dump(data2,f, indent=4)

class SocketBlueprint(Blueprint):
    def __init__(self, sio: AsyncServer, socketio_path, *args, **kwargs):
        self.sio = sio
        self.socketio_path = socketio_path
        #super().static('../../frontend/dist/static','../frontend/dist')
        super().__init__(*args, **kwargs)


    def register(self, app, options) -> None:
        self.sio.attach(app, self.socketio_path)
        super().register(app, options)


class SocketIOOutput(OutputChannel):
    @classmethod
    def name(cls) -> Text:
        return "socketio"

    def __init__(self, sio: AsyncServer, bot_message_evt: Text) -> None:
        self.sio = sio
        self.bot_message_evt = bot_message_evt


    """Creato da me"""
    async def _send_message(self, socket_id: Text, response: Any) -> None:
        global user_ID

        X = response['text']
        await self.sio.emit('json_response', {"type" : "message", "payload" : {"sender": "bot","text": X}},room=socket_id)

        if(tracker==True):
            with open("sessions/"+user_ID+".json") as json_file:
                data2=json.load(json_file)
                temp=data2['names']
                y={"sender":"bot", 'message':X}
                temp.append(y)

            write_json(data2,"sessions/"+user_ID+".json")


    async def _send_message2(self, socket_id: Text, response: Any) -> None:
        """Sends a message to the recipient using the bot event."""

        await self.sio.emit(self.bot_message_evt, response, room=socket_id)

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Send a message through this channel."""
        if(isinstance(text,dict) == False and isinstance(text,list)==False):
            for message_part in text.strip().split("\n\n"):
                await self._send_message(recipient_id, {"text": message_part})

        else:
            await self.sio.emit('json_response',text,room=recipient_id)


    async def send_image_url(
        self, recipient_id: Text, image: Text, **kwargs: Any
    ) -> None:
        """Sends an image to the output"""

        message = {"attachment": {"type": "image", "payload": {"src": image}}}
        await self._send_message(recipient_id, message)

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        """Sends buttons to the output."""

        # split text and create a message for each text fragment
        # the `or` makes sure there is at least one message we can attach the quick
        # replies to
        message_parts = text.strip().split("\n\n") or [text]
        messages = [{"text": message, "quick_replies": []} for message in message_parts]

        # attach all buttons to the last text fragment
        for button in buttons:
            messages[-1]["quick_replies"].append(
                {
                    "content_type": "text",
                    "title": button["title"],
                    "payload": button["payload"],
                }
            )

        for message in messages:
            await self._send_message(recipient_id, message)

    async def send_elements(
        self, recipient_id: Text, elements: Iterable[Dict[Text, Any]], **kwargs: Any
    ) -> None:
        """Sends elements to the output."""

        for element in elements:
            message = {
                "attachment": {
                    "type": "template",
                    "payload": {"template_type": "generic", "elements": element},
                }
            }

            await self._send_message(recipient_id, message)

    async def send_custom_json(
        self, recipient_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Sends custom json to the output"""

        json_message.setdefault("room", recipient_id)

        await self.sio.emit(self.bot_message_evt, **json_message)

    async def send_attachment(
        self, recipient_id: Text, attachment: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Sends an attachment to the user."""
        await self._send_message(recipient_id, {"attachment": attachment})


class SocketIOInput(InputChannel):
    """A socket.io input channel."""

    @classmethod
    def name(cls) -> Text:
        #logger.debug(Text)
        return "socketio"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
        credentials = credentials or {}
        return cls(
            credentials.get("user_message_evt", "user_uttered"),
            credentials.get("bot_message_evt", "bot_uttered"),
            credentials.get("namespace"),
            credentials.get("session_persistence", True),
            credentials.get("socketio_path", "/socket.io"),
        )

    def __init__(
        self,
        user_message_evt: Text = "user_uttered",
        bot_message_evt: Text = "bot_uttered",
        namespace: Optional[Text] = None,
        session_persistence: bool = True,
        socketio_path: Optional[Text] = "/socket.io",
    ):
        self.bot_message_evt = bot_message_evt
        self.session_persistence = session_persistence
        self.user_message_evt = user_message_evt
        self.namespace = namespace
        self.socketio_path = socketio_path
        self.sio = None

    def get_output_channel(self) -> Optional["OutputChannel"]:
        if self.sio is None:
            rasa.shared.utils.io.raise_warning(
                "SocketIO output channel cannot be recreated. "
                "This is expected behavior when using multiple Sanic "
                "workers or multiple Rasa Open Source instances. "
                "Please use a different channel for external events in these "
                "scenarios."
            )
            return
        return SocketIOOutput(self.sio, self.bot_message_evt)

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[Any]]
    ) -> Blueprint:
        # Workaround so that socketio works with requests from other origins.
        # https://github.com/miguelgrinberg/python-socketio/issues/205#issuecomment-493769183
        sio = AsyncServer(async_mode="sanic", cors_allowed_origins=[])
        socketio_webhook = SocketBlueprint(
            sio, self.socketio_path, "socketio_webhook", __name__
        )

        # make sio object static to use in get_output_channel
        self.sio = sio

        """fatta da me"""
        @socketio_webhook.route("/", methods=["GET"])
        async def health(_: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @sio.on("connect", namespace=self.namespace)
        async def connect(sid: Text, data: Dict) -> None:
            #logger.debug(f"User {sid} connected to socketIO endpoint.")
            #logger.debug("mi sono connesso")
            #logger.debug(data)
            global user_ID

            #else:
             #   user_ID=sid
              #  logger.debug(user_ID)
            logger.debug(f"sid {sid}, {id(sid)}")
            #if data is None:
            #    data = {}
         #        logger.debug("data is None")
         #    logger.debug(data)
         #    if("HTTP_COOKIE" in data and data["HTTP_COOKIE"] is not None):
         #        logger.debug(f"one")
         #        for x in data["HTTP_COOKIE"].split():
         #            logger.debug(x)
         #            if("io=" in x):
         #                data["session_id"]= x.split("=")[1]
         #                logger.debug(data["session_id"])
         #                sid="pippo" #data["session_id"]
         #                logger.debug(f"sid new? {sid}, {id(sid)}")
         #
         #    logger.debug(f"sid new? {sid}, {id(sid)}")
         #    logger.debug(f"sid new? {sid}")
         #
         # #   if("io="+user_ID == data["HTTP_COOKIE"] ):
         # #       logger.debug("Hello old cookie")
         # #       sid=user_ID
         # #       data["session_id"] = user_ID
         #
         #
         #    if "session_id" not in data or data["session_id"] is None:
         #    #    logger.debug(data["HTTP_COOKIE"])
         #        data["session_id"] = uuid.uuid4().hex
         #        logger.debug("data['session_id']")
         #        logger.debug(data["session_id"])
         #
         #    #logger.debug("session")
         #     #   logger.debug(data["HTTP_COOKIE"])
         #
         #        #logger.debug(data["session_id"])
         #    if self.session_persistence:
         #        sio.enter_room(sid, data["session_id"])
         #
         #    await sio.emit("session_confirm", data["session_id"], room=sid)
            #logger.debug(f"User {sid} session requested to socketIO endpoint.")

            if (tracker == True):
                data = {}
                data['names'] = []
                data['names'].append({
                    'sender': 'bot',
                    'message': 'What data are you looking for?',
                })

                with open("sessions/" +sid+".json", "w") as f:
                    json.dump(data, f)

            await self.sio.emit('json_response', {"type": "message", "payload": {"sender": "bot", "text": "Hi, there! I'm here to help you for the extraction and the analysis of genomic data."}}, room=sid)
            await self.sio.emit('json_response', {"type": "message", "payload": {"sender": "bot", "text": "What data are you looking for?"}}, room=sid)
            await self.sio.emit('json_response', {"type": "available_choices","payload": {"showSearchBar": False,"showDetails": False,"caption":'Data available',"showHelpIcon": False, "elements": [{'name': 'Annotations', 'value':'Annotations'},{'name': 'Experiments', 'value':'Experiments'}]}}, room=sid)
            await self.sio.emit('json_response', {"type": "workflow","payload": {"state": "Data Selection"}}, room=sid)

        @sio.on("disconnect", namespace=self.namespace)
        async def disconnect(sid: Text) -> None:
            logger.debug(f"User {sid} disconnected from socketIO endpoint.")

        @sio.on("reconnect", namespace=self.namespace)
        async def reconnect(sid: Text) -> None:
            print("i'm back online")
            logger.debug(" i'm back")

        @sio.on("session_request", namespace=self.namespace)
        async def session_request(sid: Text, data: Optional[Dict]):
            logger.debug("Ho ricevuto richiesta di sessione")
            logger.debug("data vale: ")
            logger.debug(data)
            logger.debug("il sid vale: ")
            logger.debug(sid)

            for x in data["session_id"].split():
                logger.debug(x)
                if ("session=" in x):
                    data["session_id"] = x.split("=")[1]

            logger.debug(data["session_id"])

            if data is None:
                data = {}
            if "session_id" not in data or data["session_id"] is None:
                data["session_id"] = uuid.uuid4().hex
                logger.debug("ciao")
            if self.session_persistence:
                sio.enter_room(sid, data["session_id"])

            logger.debug("data session2 vale: ")
            logger.debug(data)

            await sio.emit("session_confirm", data["session_id"], room=sid)
            logger.debug(f"User {sid} session requested to socketIO endpoint.")

        @sio.on(self.user_message_evt, namespace=self.namespace)
        async def handle_message(sid: Text, data: Dict) -> Any:
            output_channel = SocketIOOutput(sio, self.bot_message_evt)
            if self.session_persistence:
                if not data.get("session_id"):
                    rasa.shared.utils.io.raise_warning(
                        "A message without a valid session_id "
                        "was received. This message will be "
                        "ignored. Make sure to set a proper "
                        "session id using the "
                        "`session_request` socketIO event."
                    )
                    return
                sender_id = data["session_id"]
            else:
                sender_id = sid

            message = UserMessage(
                data["message"], output_channel, sender_id, input_channel=self.name()
            )
            await on_new_message(message)

        @sio.on('Prova', namespace='/test')
        async def test_ack_message(message):
            #user_ID = int(message['message_id'])
            logger.debug("Ho ricevuto ack")
            logger.debug(message)

        """fatta da me da é questo che funziona veramente"""
        @sio.on('my_event', namespace=self.namespace)
        async def handle_message(sid: Text, data: Dict) -> Any:
            output_channel = SocketIOOutput(sio, self.bot_message_evt)
            logger.debug("arriva il sid")
            logger.debug(sid)
            logger.debug("arriva il data")
            logger.debug(data)
            logger.debug("arriva il data session id")
            logger.debug(data["session_id"])

            #for x in data["session_id"].split():
            #    logger.debug(x)
            #    if ("session=" in x):
            #        data["session_id"] = x.split("=")[1]

            for x in data["session_id"].split():
                logger.debug(x)
                if ("session=" in x):
                    data["session_id"] = x.split("=")[1]

            if self.session_persistence:
                if not data.get("session_id"):
                    rasa.shared.utils.io.raise_warning(
                        "A message without a valid session_id "
                        "was received. This message will be "
                        "ignored. Make sure to set a proper "
                        "session id using the "
                        "`session_request` socketIO event."
                    )
                    return
                sender_id = data["session_id"]
            else:
                sender_id = sid


            #global user_ID

            message = UserMessage(
                data["data"], output_channel, sender_id, input_channel=self.name()
            )
            #('data[data]',data["data"])
            with open('data.txt', 'a') as outfile:
                json.dump( data["data"]+'\n',outfile)

            if (tracker == True):
                with open("sessions/"+user_ID+".json") as json_file:
                    data2 = json.load(json_file)
                    temp = data2['names']
                    y = {"sender": user_ID, 'message': data["data"]}
                    temp.append(y)

                write_json(data2,"sessions/"+user_ID+".json")

            await on_new_message(message)

        return socketio_webhook
