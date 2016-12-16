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
    gameid = db.Column(db.uuid, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), unique=True)
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

# Save e-mail to database and send to success page
@app.route('/', methods=['POST'])
def prereg():
    name = None
    if request.method == 'POST':
        name = request.form['name']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(l4l_games).filter(l4l_games.name == name).count():
            reg = l4l_games(name)
            db.session.add(reg)
            db.session.commit()
            return render_template('index.html')
    return render_template('index.html')

@app.route('/playoffline', methods=['GET'])
def playoffline():
    return render_template('playoffline.html')
    wordgamestate = None
    if request.method == 'GET':
        wordgamestate = ""
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(l4l_games).filter(l4l_games.wordgamestate == wordgamestate and l4l_games.gameid == gameid).count():
            reg = l4l_games(wordgamestate)
            db.session.add(reg)
            db.session.commit()
            return render_template('playoffline.html')
    #return render_template('playoffline.html')

@app.route('/playonline', methods=['GET'])
def playonline():
    wordgamestate = None
    if request.method == 'GET':
        wordgamestate = ""
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(l4l_games).filter(l4l_games.wordgamestate == wordgamestate and l4l_games.gameid == gameid).count():
            reg = l4l_games(wordgamestate)
            db.session.add(reg)
            db.session.commit()
            return render_template('playonline.html')
    return render_template('playonline.html')

@app.route('/playmove', methods=['POST'])
def playmove():
    wordgamestate = None
    if request.method == 'POST':
        wordgamestate = request.form['theletter']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(l4l_games).filter(l4l_games.wordgamestate == wordgamestate and l4l_games.gameid == gameid).count():
            reg = l4l_games(wordgamestate)
            db.session.add(reg)
            db.session.commit()
            return render_template('playonline.html')
        else:
            reg = l4l_games(wordgamestate)
            db.session.add(reg)
            db.session.commit()
            return render_template('playonline.html')
    return render_template('playonline.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
