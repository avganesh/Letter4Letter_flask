from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import uuid 

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
heroku = Heroku(app)
db = SQLAlchemy(app)

# Create our database model
class l4l_games(db.Model):
    __tablename__ = "l4l_games"
    #id = db.Column(db.Integer, primary_key=True)
    gameid = db.Column(db.String(120), primary_key=True, unique=True)#, default=uuid.uuid4)
    P1name = db.Column(db.String(120), unique=False, default="")
    P2name = db.Column(db.String(120), unique=False, default="")
    wordgamestate = db.Column(db.String(120), unique=False, default="")
    lastmove = db.Column(db.String(120), unique=False, default="")
    P1score = db.Column(db.Integer, unique=False, default=0)
    P2score = db.Column(db.Integer, unique=False, default=0)

    def __init__(self, gameid):
        self.gameid = gameid

    def __repr__(self):
        return '<gameid %r>' % self.gameid

def isword(word):
    if (len(word)>3 and(word in open('static/UKACD17.TXT').read())):
        response = True
    else:
        response = False
    return str(response)

def scoreupdate(player, gameID):
    game = db.session.query(l4l_games).filter_by(gameid=gameID).first()
    if (player == game.P1name):
        game.P2score = game.P2score + 1
        game.lastmove = player
        message = game.P2name + " wins!! and gets to start this game."
    elif (player == game.P2name): 
        game.P1score = game.P1score + 1
        game.lastmove = player
        message = game.P1name + " wins!! and gets to start this game."
    game.wordgamestate = ""
    db.session.commit()
    game = l4l_games.query.filter_by(gameid=gameID).first()
    return render_template('playonline.html', Player1=game.P1name, Player2=game.P2name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.P1score, P2score=game.P2score, lastmove=game.lastmove, roundnum=0, yourname=name, message=message)
    
# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/splash', methods=['GET', 'POST'])
def splash():
    if request.method == 'GET':
        return render_template('splash.html')

##@app.route('/favicon.ico')
##def favicon():
##    return flask.redirect(flask.url_for('static', filename='favicon.ico', code=301))
##    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

# Save e-mail to database and send to success page
@app.route('/newgame', methods=['GET', 'POST'])
def newgame():
    if request.method == 'POST':
        response = str(uuid.uuid4())
        reg = l4l_games(response)
        db.session.add(reg)
        db.session.commit()
        #game = db.session.query(l4l_games).filter_by(gameid=response).first()
        #game.P1score = 0
        #game.P2score = 0
        #game.wordgamestate = ""
        #game.lastmove = ""
        #db.session.commit()
    return response

@app.route('/joingame', methods=['GET', 'POST'])
def joingame():
    if request.method == 'POST':
        name = request.json['nameData']
        gameid = request.json['gameData']
        player = request.json['playerData']
        message = "Enter a letter to start playing"
        game = db.session.query(l4l_games).filter_by(gameid=gameid).first()
        if player == "P1":
            game.P1name = name
        elif player == "P2":
            game.P2name = name
        db.session.commit()
        game = l4l_games.query.filter_by(gameid=gameid).first()
    return render_template('playonline.html', Player1=game.P1name, Player2=game.P2name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.P1score, P2score=game.P2score, lastmove=game.lastmove, roundnum=0, yourname=name, message=message)


@app.route('/playmove', methods=['GET', 'POST'])
def playmove():
    if request.method == 'POST':
        currentword = request.json['wordData']
        theletter = request.json['letterData']
        gameid = request.json['gameData']
        move = request.json['moveData']
        name = request.json['playerData']
        if move == "left":
            currentword = theletter+currentword
        elif move == "right":
            currentword = currentword+theletter
        game = db.session.query(l4l_games).filter_by(gameid=gameid).first()
        game.wordgamestate = currentword
        game.lastmove = name
        db.session.commit()
        if (isword(currentword)):
            return score_update(name, gameid)
        else:
            game = l4l_games.query.filter_by(gameid=gameid).first()
            message = "Hmm... interesting move "+ name + "... now press refresh to see your opponent's move."  
            return render_template('playonline.html', Player1=game.P1name, Player2=game.P2name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.P1score, P2score=game.P2score, lastmove=game.lastmove, roundnum=len(currentword), yourname=name, message=message)

#@app.route('/keepscore', methods=['GET', 'POST'])
#def keepscore():
#    if request.method == 'POST':
#        gameid = request.json['gameData']
#        score = request.json['scoreData']
#        name = request.json['playerData']
#        game = db.session.query(l4l_games).filter_by(gameid=gameid).first()
#        if request.json['Player'] == "P1":
#            game.P1score = score
#        elif request.json['Player'] == "P2":
#            game.P2score = score
#        db.session.commit()
#        game = l4l_games.query.filter_by(gameid=gameid).first()
#    return render_template('playonline.html', Player1=game.P1name, Player2=game.P2name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.P1score, P2score=game.P2score, lastmove=game.lastmove, roundnum=len(currentword), yourname=name)

@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        gameid = request.json['gameData']
        name = request.json['playerData']
        game = l4l_games.query.filter_by(gameid=gameid).first()
        if (game.lastmove == name):
            message = "Still waiting for opponent's move, press Refresh again after a while..."
        else:
            message = "Enter a letter to play."
    return render_template('playonline.html', Player1=game.P1name, Player2=game.P2name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.P1score, P2score=game.P2score, lastmove=game.lastmove, roundnum=len(game.wordgamestate), yourname=name, message=message)

if __name__ == '__main__':
    app.debug = True
    app.run()
