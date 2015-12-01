from __future__ import print_function

_author_ = 'Peter "Marenthyu" Fredebold'

import sys
import atexit
import traceback
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
import thread
import time
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

Builder.load_file('main.kv')

class ScrollView(ScrollView):
    pass

class MainScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))

class ChatApp(App):

    name = ""

    refreshstarted = False

    connectedserver = []

    def start(lol):
        try:

            class MyClientProtocol(WebSocketClientProtocol):

                latestmessage = None

                def onConnect(self, response):
                    print("Server connected: {0}".format(response.peer))
                    try:
                        ChatApp().connectedserver[0] = self
                        self.factory.resetDelay()
                    except:
                        ChatApp().connectedserver.append(self)
                        self.factory.resetDelay()

                def onOpen(self):
                    atexit.register(self.sendClose, 1000, "User Exited program.")
                    print("WebSocket connection open.")

                def onMessage(self, payload, isBinary):
                    if isBinary:
                        print("Binary message received: {0} bytes".format(len(payload)))
                    else:
                        print("Text message received: {0}".format(payload.decode('utf8')))
                        self.latestmessage = payload.decode('utf8') + '\n'

                def onClose(self, wasClean, code, reason):
                    print("WebSocket connection closed: {0}".format(reason))



            class MyClientFactory(WebSocketClientFactory, ReconnectingClientFactory):

                protocol = MyClientProtocol

                def clientConnectionFailed(self, connector, reason):
                    print("Client connection failed .. retrying ..")
                    self.retry(connector)

                def clientConnectionLost(self, connector, reason):
                    print("Client connection lost .. retrying ..")
                    self.retry(connector)

            print('Called Start method; Factory & Protocol defined.')

            factory = MyClientFactory(u"ws://marenthyu.de:9000", debug=False)

            print('Set Factory')

            reactor.connectTCP("marenthyu.de", 9000, factory)

            print('connected')

            reactor.run()

            print('run')


        except:
            print('ERROR IN START METHOD')
            traceback.print_exc()

    thread.start_new_thread(start, (1, ))


    def startRefresh(self, output):
        print('Starting refresh!')
        while True:
            try:
                if self.connectedserver[0].latestmessage is not None:
                    self.refresh(output, self.connectedserver[0].latestmessage)
                    self.connectedserver[0].latestmessage = None
            except:
                print('ERROR IN START REFRESH')
                traceback.print_exc()
                return

    def refresh(self, output, message):
        if message.startswith("NAME:"):
            x = int(len(message)-1)
            self.name = message[5:x]
            output.text = 'Your name is now '+ self.name + '\n' + output.text
            output.cursor = (0,0)
            return

        output.text = message+output.text
        output.cursor = (0,0)

    def build(self):
        return sm

    def refocus(self, widget):
        time.sleep(1)
        widget.focus = True

    def sendMessage(self, input, message, output, sv):
        try:
            if not self.refreshstarted:
                thread.start_new_thread(self.startRefresh, (output, ))
                self.refreshstarted = True
            input.text = ""
            if message == "stop":
                self.connectedserver[0].sendClose(1000, "User typed stop")
                time.sleep(1)
                sys.exit(0)


            additive = output.font_size/output.height
            x, y = output.size_hint
            output.size_hint = (x, (y+additive))

            self.connectedserver[0].sendMessage(message.encode('utf8'), False)
            return
        except:
            print('ERROR IN SENDMESSAGE')
            traceback.print_exc()
        sys.exit(0)

    def on_pause(self):
        # self.connectedserver[0].sendClose(1000, "App paused")

        self.connectedserver[0].sendMessage('/afk paused'.encode('utf8'), False)

        time.sleep(1)

        return True

    def on_resume(self):
        try:
            print('resumed; should reconnect asap....')
            self.connectedserver[0].latestmessage = 'Welcome back.\n'
            time.sleep(1)
            self.connectedserver[0].sendMessage('/afk resume'.encode('utf8'), False)

            return True
        except:
            print('ERROR ON RESUME')
            traceback.print_exc()


    def on_stop(self):
        self.connectedserver[0].sendClose(1000, "App closed")
        time.sleep(1)







if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('UTF-8')


    # log.startLogging(sys.stdout)


    ChatApp().run()