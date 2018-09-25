#import statements go here 
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"
    
#create class to represent WTForm that inherits flask form

class ArtistForm(FlaskForm):
    artist_name = StringField('What is the artist name?', validators=[Required()])
    num_results = IntegerField('How many results do you want?', validators=[Required()])
    email = IntegerField('What is your email?', validators=[Email(), Required()])
    submit = SubmitField('Submit')

@app.route('/itunes-form')
def itunes_form():
    #what code goes here?
    simpleForm = ArtistForm()
    return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
    #what code goes here?
    # HINT : create itunes-results.html to represent the results and return it
    form = ArtistForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.artist_name.data
        num = form.num_results.data
        if num > 200:
        	num = 200
        email = form.email.data
        humes = requests.get('https://itunes.apple.com/search?', params={'term':name, 'limit':num}).text

        res = json.loads(humes)
        return render_template(itunes-result.html, result_html = res)
        # text = '<h1> Here are ' + num_results + ' based on your search of ' + name +'</h1><br><br>'
        # #number_results = res['resultCount']

        # for x in res['results']:
        # 	title = x['trackName']
        # 	description = x['description']
        # 	string = 'Title: {} <br><br> Description: {}'.format(title, description)
        # 	text += string
        # return text
    flash('All fields are required!')
    return redirect(url_for('itunes_form')) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
