# -*- coding: utf-8 -*-
_author_ = 'Peter "Marenthyu" Fredebold'

import random
import traceback
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class Test():
    list = []
    names = ['Liebling','Profi','Gorilla','Bananenschlecker','Computer','Tastatur','Maus','Katze','Headset','Hund','Wikipedia','Dr. Franz','Dr. K-Mann','Dr. Schiwago','Dr. med. J. Busch-Lichtner','Liebe','Hass','Wut','Ding','Heimatlosigkeit','Freude','Gartenzwerg','Der Deutsche','Ammi','Coder','Andi Gewehre','Marei Juana','Ann Zeige','Andi Macht','Matt McBrötchen','Bodo Lette','Lätta','Lexy Kon','Jack','Anna','Schneewettchen','Frank Reich','Lapü Topp','Ben U. T. Z. Mich','Hinrich Tung','PythonIstKacke','YOLOMAN','ihatecaps','Tim Eisenhart','Lach Meister','Bambusratte','Addi Dass','Windoofs','Applios','Linne X.','Rainer hin und von zu Fall','Christian Harten','Jacqueline-Schayenne-Chantralle','DAU Jones','Anonymous','Bruce Will S.','Hannibal Starkarm McSteel']

class MyServerProtocol(WebSocketServerProtocol):

    name = 'Lol, wähl ma was.'
    color = 'ff1234'
    afk = False

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        try:
            random.seed()
        except:
            print('1 Fehler')
        try:
            self.name = Test.names[random.randint(0,len(Test.names))]
            print('Name: '+ self.name)
            self.color = self.rgbToHex(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            print ('Color: ' + self.color)

        except:
            print('2')
        Test.list.append(self)



    def onOpen(self):
        print("WebSocket connection open.")
        self.sendMessage(('NAME:'+self.name).encode('utf8'), False)
        for x in Test.list:
            x.sendMessage(self.name + ' has joined.')

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
             print("Text message received: {0}".format(payload.decode('utf8')))


        if payload.decode('utf8').startswith('/'):
            command = payload.decode('utf8')[1:len(payload.decode('utf8'))]
            if command.startswith('help'):
                self.sendMessage('Available commands:\n/help - Displays this message\n/list - shows online and afk people\n/afk - sets your afk status\n/name NEWNAME - sets your name\n/color RED GREEN BLUE - sets your color'.encode('utf8'), False)
                return
            if command.startswith('name'):
                if len(command) > 5:
                    newname = command[5:len(command)]
                    self.name = newname
                    self.sendMessage(('NAME:' + newname).encode('utf8'), False)
                    return
                self.sendMessage(('Your name is '+self.name).encode('utf8'), False)
                return
            if command.startswith('list'):
                print('list command received.')
                i = 0
                reply = 'There are currently the following people online:\n'
                for x in Test.list:
                    i += 1
                    if x.afk is True:
                        reply = reply + x.name + ' (AFK), '
                    else:
                        reply = reply + x.name + ', '
                reply = reply + '\nwhich is ' + str(i) + ' People.'
                self.sendMessage(reply.encode('utf8'), False)
                print('Reply is: ' + reply)
                return
            if command.startswith('afk'):
                if len(command)>4:
                    extra = command[4:len(command)]
                    if extra == 'paused':
                        self.afk = True
                        for x in Test.list:
                            x.sendMessage(self.name + ' is now AFK. (app paused)'.encode('utf8'), False)
                        return
                    if extra == 'resume':
                        self.afk = False
                        for x in Test.list:
                            x.sendMessage(self.name + ' is no longer AFK. (app resumed)'.encode('utf8'), False)
                        return
                if self.afk is True:
                    self.afk = False
                    for x in Test.list:
                            x.sendMessage(self.name + ' is no longer AFK.'.encode('utf8'), False)
                    return
                else:
                    self.afk = True
                    for x in Test.list:
                            x.sendMessage(self.name + ' is now AFK.'.encode('utf8'), False)
                    return
            if command.startswith('color'):
                if len(command)>6:
                    red = command[6:command.find(' ', 6)]
                    green = command[7+len(red):command.find(' ', 7+len(red))]
                    blue = command[8+len(red)+len(green):len(command)]
                    if int(red) > 255:
                        return
                    if int(blue) > 255:
                        return
                    if int(green) > 255:
                        return
                    self.color = self.rgbToHex(int(red), int(green), int(blue))
                    self.sendMessage('[color='+self.color+']Your new Color has been set.[/color]'.encode('utf8'), False)
                return

        # no command, send message to all clients
        for x in Test.list:
            x.sendMessage(('[color=' + self.color + ']' + self.name + ':[/color] ' + payload.decode('utf8')).encode('utf8'), isBinary)

    def onClose(self, wasClean, code, reason):
        try:
            for x in Test.list:
                x.sendMessage(self.name + ' has disconnected.'.encode('utf8'), False)
            Test.list.remove(self)
        except:
            traceback.print_exc()
        print("WebSocket connection closed: {0}".format(reason))

    def rgbToHex(self, red, green, blue):
        redh = 0
        red1 = ''
        red2 = ''
        while red >= 16:
            redh += 1
            red -= 16
        if red == 10:
            red2 = 'a'
        else:
            if red == 11:
                red2 = 'b'
            else:
                if red == 12:
                    red2 = 'c'
                else:
                    if red == 13:
                        red2 = 'd'
                    else:
                        if red == 14:
                            red2 = 'e'
                        else:
                            if red == 15:
                                red2 = 'f'
                            else:
                                red2 = str(red)
        if redh == 10:
            red1 = 'a'
        else:
            if redh == 11:
                red1 = 'b'
            else:
                if redh == 12:
                    red1 = 'c'
                else:
                    if redh == 13:
                        red1 = 'd'
                    else:
                        if redh == 14:
                            red1 = 'e'
                        else:
                            if redh == 15:
                                red1 = 'f'
                            else:
                                red1 = str(redh)
        blueh = 0
        blue1 = ''
        blue2 = ''
        while blue >= 16:
            blueh += 1
            blue -= 16
        if blue == 10:
            blue2 = 'a'
        else:
            if blue == 11:
                blue2 = 'b'
            else:
                if blue == 12:
                    blue2 = 'c'
                else:
                    if blue == 13:
                        blue2 = 'd'
                    else:
                        if blue == 14:
                            blue2 = 'e'
                        else:
                            if blue == 15:
                                blue2 = 'f'
                            else:
                                blue2 = str(blue)
        if blueh == 10:
            blue1 = 'a'
        else:
            if blueh == 11:
                blue1 = 'b'
            else:
                if blueh == 12:
                    blue1 = 'c'
                else:
                    if blueh == 13:
                        blue1 = 'd'
                    else:
                        if blueh == 14:
                            blue1 = 'e'
                        else:
                            if blueh == 15:
                                blue1 = 'f'
                            else:
                                blue1 = str(blueh)
        greenh = 0
        green1 = ''
        green2 = ''
        while green >= 16:
            greenh += 1
            green -= 16
        if green == 10:
            green2 = 'a'
        else:
            if green == 11:
                green2 = 'b'
            else:
                if green == 12:
                    green2 = 'c'
                else:
                    if green == 13:
                        green2 = 'd'
                    else:
                        if green == 14:
                            green2 = 'e'
                        else:
                            if green == 15:
                                green2 = 'f'
                            else:
                                green2 = str(green)
        if greenh == 10:
            green1 = 'a'
        else:
            if greenh == 11:
                green1 = 'b'
            else:
                if greenh == 12:
                    green1 = 'c'
                else:
                    if greenh == 13:
                        green1 = 'd'
                    else:
                        if greenh == 14:
                            green1 = 'e'
                        else:
                            if greenh == 15:
                                green1 = 'f'
                            else:
                                green1 = str(greenh)
        print('Converted color: ' + red1 + red2 + green1 + green2 + blue1 + blue2)
        return (red1 + red2 + green1 + green2 + blue1 + blue2)




if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    reload(sys)
    sys.setdefaultencoding('UTF-8')

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000", debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()
