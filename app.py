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
    name = db.Column(db.String(120), unique=False)
    wordgamestate = db.Column(db.String(120), unique=False)
    score = db.Column(db.Integer, unique=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

##@app.route('/favicon.ico')
##def favicon():
##    return flask.redirect(flask.url_for('static', filename='favicon.ico', code=301))
##    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

# Save e-mail to database and send to success page
@app.route('/', methods=['POST'], endpoint='prereg')
def prereg():
    name = None
    if request.method == 'POST':
        name = request.form['name']
        if not (db.session.query(l4l_games).filter(l4l_games.name == name).count()):
            reg = l4l_games(name)
            db.session.add(reg)
            db.session.commit()
        game = l4l_games.query.filter_by(name=name).first()
        return render_template('playonline.html', Player1=name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.score)


##@app.route('/playonline', methods=['GET', 'POST'])
##def playonline():
##    
##    if request.method == 'GET':
##        game.wordgamestate = request.form['theletter']
##        db.session.commit()
##    return render_template('playonline.html', theword=game.wordgamestate, gameid=game.gameid, Player1=game.name)

app.route('/playmove', methods=['GET', 'POST'])
def playmove():
    game = db.session.query(l4l_games).filter(gameid==gameid).first()
    if request.method == 'POST':
        currentword = request.data
        game.wordgamestate = currentword
        db.session.commit()
        return render_template('playonline.html', Player1=name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.score)

app.route('/keepscore', methods=['GET', 'POST'])
def keepscore():
    game = db.session.query(l4l_games).filter(gameid==gameid).first()
    if request.method == 'POST':
        P1score = request.data
        game.score = P1score
        db.session.commit()
        return render_template('playonline.html', Player1=name, gameid=game.gameid,  theword=game.wordgamestate, P1score=game.score)


if __name__ == '__main__':
    app.debug = True
    app.run()
