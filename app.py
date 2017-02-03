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
    gameid = db.Column(db.String(120), primary_key=True, default=uuid.uuid4)
    P1name = db.Column(db.String(120), unique=False)
    P2name = db.Column(db.String(120), unique=False)
    wordgamestate = db.Column(db.String(120), unique=False)
    P1score = db.Column(db.Integer, unique=False)
    P2score = db.Column(db.Integer, unique=False)

    def __init__(self, P1name):
        self.P1name = P1name

    def __repr__(self):
        return '<Name %r>' % self.P1name

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

##@app.route('/favicon.ico')
##def favicon():
##    return flask.redirect(flask.url_for('static', filename='favicon.ico', code=301))
##    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

# Save e-mail to database and send to success page
@app.route('/', methods=['GET', 'POST'])
def newgame():
    if request.method == 'POST':
        P1name = request.form['name']
        reg = l4l_games(P1name)
        db.session.add(reg)
        db.session.commit()
        game = l4l_games.query.filter_by(P1name=P1name).first()
        return render_template('playonline.html', Player1=game.P1name, Player2=game.P2name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.P1score, P2score=game.P2score)

@app.route('/', methods=['GET', 'POST'])
def joingame():
    if request.method == 'POST':
        P2name = request.form['name']
        gameid = request.form['gameid']
        game = db.session.query(l4l_games).filter(gameid==gameid).first()
        game.P2name = P2name 
        return render_template('playonline.html', Player1=game.P1name, Player2=game.P2name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.P1score, P2score=game.P2score)


@app.route('/playmove', methods=['GET', 'POST'])
def playmove():
    if request.method == 'POST':
        currentword = request.json['moveData']
        gameid = request.json['gameData']
        game = db.session.query(l4l_games).filter(gameid==gameid).first()
        game.wordgamestate = currentword
        db.session.commit()
        return render_template('playonline.html', Player1=game.P1name, Player2=game.P2name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.P1score, P2score=game.P2score)

@app.route('/keepscore', methods=['GET', 'POST'])
def keepscore():
    if request.method == 'POST':
        gameid = request.json['gameData']
        score = request.json['scoreData']
        game = db.session.query(l4l_games).filter(gameid==gameid).first()
        if request.json['Player'] == "P1":
            game.P1score = score
        elif request.json['Player'] == "P2":
            game.P2score = score
        db.session.commit()
        return render_template('playonline.html', Player1=game.P1name, Player2=game.P2name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.P1score, P2score=game.P2score)

@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    game = db.session.query(l4l_games).filter(gameid==gameid).first()
    return render_template('playonline.html', Player1=game.P1name, Player2=game.P2name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.P1score, P2score=game.P2score)

if __name__ == '__main__':
    app.debug = True
    app.run()
