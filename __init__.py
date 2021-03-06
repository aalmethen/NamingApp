#new name site
import os
from forms import  AddForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ['DATABASE_URL']
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#os.environ['DATABASE_URL']
db = SQLAlchemy(app)
Migrate(app,db)

def getApp():
    return app

################################
##### Models creation ##########
################################
class N2(db.Model):

    __tablename__ = 'names'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return self.name

################################
@app.route('/',methods=['POST','GET'])
def index():

    form = AddForm()

    if form.validate_on_submit():

        name = form.name.data

        new_Name = N2(name)
        db.session.add(new_Name)
        db.session.commit()

        return redirect(url_for('list'))

    return render_template('home.html', form = form)


@app.route('/list')
def list():

    NList=N2.query.limit(5).all()
    text = arabic_reshaper.reshape(str(N2.query.all()))
    text = get_display(text)
    # Generate a word cloud image
    wordcloud = WordCloud(background_color='White',font_path="static/arial.ttf").generate(text)
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")


    wordcloud.to_file('static/testing.jpg')

    return render_template('list.html', NList=NList)

###########################################################################
if __name__ == '__main__':
    app.run(debug=True)
