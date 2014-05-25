from tornado import web, websocket, ioloop, httpclient
import random, string, json

#Let us know we've restarted:
print('Restarted!')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits): #Generates a random ID
    return ''.join(random.choice(chars) for _ in range(size))


#Food Categories:
foodtypes = [{"n":"American","id":"american"},{"n":"American: Southern","id":"american-southern"},{"n":"Asian","id":"asian"},{"n":"French","id":"french"},{"n":"Indian","id":"indian"},{"n":"Italian","id":"italian"},{"n":"Mexican","id":"mexican"},{"n":"Other","id":"n-a"}]
foodlist = ['american', 'american-southern', 'asian', 'french', 'indian', 'italian', 'mexican', 'n-a']

#Games Data:
games = {}



class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('views/home.html', title="Emo Ice Cream Deluxe")

class PlayHandler(web.RequestHandler):
    def get(self):
        self.render('views/play.html', title = "Pick Category", foods = foodtypes )

class GameHandler(web.RequestHandler):
    def get(self):
        cat = self.get_argument('c', None, True)
        if cat == None or cat not in foodlist:
            self.write('Oops! Invalid Category')
            self.finish()
            return

        if cat not in games:
            client = httpclient.HTTPClient()
            data = client.fetch('https://api.pearson.com/kitchen-manager/v1/recipes?limit=100&cuisine='+cat)
            myjson = json.loads(data.body.decode())
            print(myjson)
            games[cat] = {"rooms":[], "recipes": myjson['results']}
            print(games)

        self.render('views/game.html', title = "Play Game", cid = cat)


class SocketHandler(websocket.WebSocketHandler):
    def makeRound(self):
        details=self.get_argument("c") #Get Card ID
        rec = games[details]['recipes']
        print(len(rec))
        trep = random.randint(0, len(rec) - 1)
        totaling = rec[trep]['ingredients']
        ing2 = rec[random.randint(0, len(rec) - 1)]['ingredients']
        ing3 = rec[random.randint(0, len(rec) - 1)]['ingredients']

        for i in ing2:
            if i not in totaling:
                totaling.append(i)

        for i in ing3:
            if i not in totaling:
                totaling.append(i)

        return {'recipe':rec[trep], 'inglist':totaling}


    def open(self):
        details=self.get_argument("c") #Get Card ID
        print("open",details)

        joined = False
        i = 0
        for game in games[details]["rooms"]:
            if "player1" not in game['players']:
                print('here 1')
                game['players']["player1"] = {"socket": self, "score": 0, "right": [], "wrong": []}
                self.write_message('{"event":"youjoin", "data":{"playernum": 1, "gamenum": '+str(i)+'}}')

                joined = True
            elif "player2" not in game['players']:
                print('here 2')
                game['players']["player2"] = {"socket": self, "score": 0, "right": [], "wrong": []}
                self.write_message('{"event":"youjoin", "data":{"playernum": 2, "gamenum": '+str(i)+'}}')

                joined = True
            else:
                print('here 3')
            i = i + 1

            if joined:
                break

        print(games[details]["rooms"])
        if joined == False or i == 0: #Create the first game or a new game.
            print('here 4')
            games[details]["rooms"].append({"players":{"player1":{"socket": self, "score": 0, "right":[], "wrong": ""}}})
            self.write_message('{"event":"youjoin", "data":{"playernum": 1, "gamenum": '+str(i)+'}}')


    def on_message(self, message):
        print('GOT MESSAGE', message)
        details=self.get_argument("c")
        msgjson = json.loads(message)

        if msgjson['event'] == 'userinfo':
            playerinfo = games[details]['rooms'][msgjson['gamenum']]['players']["player"+str(msgjson['playernum'])]
            playerinfo['username'] = msgjson['data']['username']
            game = games[details]['rooms'][msgjson['gamenum']]
            if msgjson['playernum'] == 1:
                #Start Game
                if "player2" in game['players']:
                    oppinfo =  game['players']["player2"]
                else:
                    return
            else:
                if "player1" in game['players']:
                    oppinfo =  game['players']["player1"]
                else:
                    return


            self.write_message('{"event":"oppinfo", "data":{"username": "'+oppinfo['username']+'" }}')
            oppinfo['socket'].write_message('{"event":"oppinfo", "data":{"username": "'+playerinfo['username']+'" }}')
            print('Sent!')

            round = self.makeRound()
            game['currentround'] = round

            self.write_message('{"event":"startround", "data" : {"roundnum": 0, "set": '+json.dumps(round)+'}}')
            oppinfo['socket'].write_message('{"event":"startgame", "data" : {"roundnum": 0, "set": '+json.dumps(round)+'}}')
            

        elif msgjson['event'] == '':
            pass

    def on_close(self):
        details=self.get_argument("c")
        for game in games[details]['rooms']:
            if 'player1' in game['players']:
                if game['players']['player1']['socket'] == self:
                    print('player1 left')
                    del game['players']['player1']
                    if 'player2' in game['players']:
                        game['players']['player2']['socket'].write_message('{event:"oppleft"}')
                    pass

            if 'player2' in game['players']:
                if game['players']['player2']['socket'] == self:
                    print('player2 left')
                    del game['players']['player2']
                    if 'player1' in game['players']:
                        game['players']['player1']['socket'].write_message('{"event":"oppleft"}')
                    pass

        print("WebSocket closed")




application = web.Application([
    (r"/", IndexHandler),
    (r'/public/(.*)', web.StaticFileHandler, {'path': "public"}),
    (r'/play', PlayHandler),
    (r'/game', GameHandler),
    (r'/ws/([^/]+)', SocketHandler),
    (r'/ws', SocketHandler)
], debug=True)


if __name__ == "__main__":
    application.listen(9008)
    ioloop.IOLoop.instance().start()