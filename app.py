from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os.path
import json

app = Flask(__name__)
app.secret_key = '8h2tf629h20242gv2h2u2u'

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
	if request.method=="POST":
		urls = {}

		if os.path.exists('./links/urls.json'):
			with open('./links/urls.json') as urls_file:
				urls = json.load(urls_file)

		if request.form['code'] in urls.keys():
			flash('Shortname already taken. Please select another one.')
			return redirect(url_for('home'))

		if 'url' in request.form.keys():
			urls[request.form['code']] = {'url': request.form['url']}
		else:
			f = request.files['file']
			full_name = request.form['code'] + secure_filename(f.filename)
			f.save('./images/' + full_name)
			urls[request.form['code']] = {'file': full_name}

		with open('./links/urls.json', 'w') as urls_file:
			json.dump(urls, urls_file)

		return render_template('your_url.html', code=request.form['code'])
	else:
		return redirect(url_for('home'))


@app.route('/<string:code>')
def redirect_to_url(code):
	if os.path.exists('./links/urls.json'):
		with open('./links/urls.json') as urls_file:
			urls = json.load(urls_file)
			if code in urls.keys():
				if 'url' in urls[code].keys():
					return redirect(urls[code]['url'])	


