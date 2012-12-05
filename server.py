"""

============================================================================

A minimal Twisted static & websocket server  copyright Jonathan Dobson, 2012
----------------------------------------------------------------------------
                                                                LICENSE: MIT

============================================================================

"""

# standard lib
import os
import sys
import json
import random

# 3rd party
from twisted.python import log
from autobahn.websocket import (
    WebSocketServerFactory,
    WebSocketServerProtocol,
    listenWS
)

# internal
from client import ClientState


# / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
#
# THE PROTOCOL (i.e. client) FOR THE WEBSOCKET SERVER
#
# / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /


class MyWebSocketServerProtocol(WebSocketServerProtocol):

    def onOpen(self):

        """

        Register each client as it comes in (self == client) to the
        web socket server.

        """

        self.factory.register(self)

    def onMessage(self, msg, binary):

        """

        All websocket messages should be valid JSON. We pass the message and
        the client that sent the message (self) to the web socket server.

        """

        if not binary:

            try:
                msg = json.loads(msg)
            except:
                msg = {}

            print ("Got message {} from {}".format(msg, self.peerstr))
            self.factory.receive(msg, self)

    def connectionLost(self, reason):

        """

        Unregister each client (self) as it disconnects.

        """

        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


# / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
#
# WEB SOCKET SERVER COMPONENT
#
# / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /


class MyWebSocketServer(WebSocketServerFactory):

    protocol = MyWebSocketServerProtocol

    def __init__(self, url):

        WebSocketServerFactory.__init__(self, url)

        self.clients = []
        self.client_state = {}
        self.tick()

    def tick(self):

        """

        The server tick time. Housekeeping can be done here.
        NOTE: This is initially kicked off by self.__init__

        """

        print ("Server ticks.")
        reactor.callLater(1, self.tick)

        if random.choice([0, 0, 1]):
            self.broadcast(json.dumps({"number": random.randint(1, 10)}))

    def register(self, client):

        """

        Register a client, associating some state.

        """
        if not client in self.clients:

            print "registered client " + client.peerstr
            self.clients.append(client)
            self.client_state[client] = ClientState()

    def unregister(self, client):

        """

        Remove a client from the registry.

        """

        if client in self.clients:

            print "unregistered client " + client.peerstr
            self.clients.remove(client)
            del self.client_state[client]

    def send(self, msg, client):

        """

        Send a message to a particular client.

        :msg should be a dict
        :client should be a WebSocketServerProtocol instance

        """

        if client in self.clients:

            print ("Replying to {} with {}...".format(client.peerstr, msg))
            client.sendMessage(json.dumps(msg))  # TODO: superize this so that
                                            # the client's sendMessage method
                                            # handles the json serializing

    def receive(self, msg, client):

        """

        Websocket messages from clients come in here, along with the client.

        :msg should be a dict
        :client should be a WebSocketServerProtocol instance

        """

        if client not in self.clients:
            return

        if not isinstance(msg, dict):
            return

        if msg.get("msgId", None) == None:
            return

        if msg.get("commandText", None) == None:
            return

        self.client_state[client].foo = 1
        msg = dict(
            msgId=msg.get("msgId"),
            lines=["Hello.", "World."]
        )

        self.reply(msg, client)

    def broadcast(self, msg):

        """

        Broadcasts a message to all connected websockets.

        :msg should be valid json

        """

        print ("broadcasting message '{}'...".format(msg))
        for c in self.clients:

            print ("broadcasting to " + c.peerstr)
            c.sendMessage(msg)


# / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
#
# STATIC SITE COMPONENT
#
# / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /


from twisted.web import resource


class Home(resource.Resource):

    isLeaf = False

    def getChild(self, name, request):

        if name == '':
            return self  # I assume by returning self I am returning
                         # self.render_GET

        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):

        html = "<b>Ruh-roh.</b>"
        try:
            app_html = os.path.join(self.root_dir, self.app, 'app.html')
            with open(app_html, 'r') as f:
                html = f.read()
        except:
            log.err()
            pass

        return html

# / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
#
# MAIN SCRIPT
#
# / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /


def setup_websocket_component(port=6789):

    """

    Setup and start the websocket portion of the server.

    """

    log.startLogging(sys.stdout)

    address = "ws://localhost:" + str(port)
    server = MyWebSocketServer(address)

    listenWS(server)


from twisted.internet import reactor


def setup_static_component(port=8000, root=None, app="some-app", css="css",
    js="js", images="images", fonts="fonts"):

    """

    Setup and start the static portion of the server.

    """

    from twisted.web import server, static

    if not root:
        root = os.getcwd()

    site_root = Home()
    site_root.root_dir = root
    site_root.app = app

    if not root:
        root = os.getcwd()

    # Add static directories
    site_root.putChild('css',    static.File(os.path.join(root, app, css)))
    site_root.putChild('js',     static.File(os.path.join(root, app, js)))
    site_root.putChild('images', static.File(os.path.join(root, app, images)))
    site_root.putChild('fonts',  static.File(os.path.join(root, app, fonts)))

    site = server.Site(site_root)
    reactor.listenTCP(port, site)


def run():

    reactor.run()  # blocks

if __name__ == '__main__':

    # 1
    setup_websocket_component(port=6789)

    # 2
    setup_static_component(
        port=8000,
        app='test-app'
    )

    # 3
    run()
