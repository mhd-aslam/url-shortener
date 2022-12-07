from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
from werkzeug.utils import secure_filename
import os.path
import json

app = Flask(__name__)
app.secret_key = '8h2tf629h20242gv2h2u2u'

@app.route('/')
def home():
	return render_template('home.html', codes=session.keys())

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
			f.save('./static/user_files/' + full_name)
			urls[request.form['code']] = {'file': full_name}

		with open('./links/urls.json', 'w') as urls_file:
			json.dump(urls, urls_file)
			session[request.form['code']] = True

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
				else:
					return redirect(url_for('static', filename='user_files/' + urls[code]['file']))	

	return abort(404)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('error_404.html'), 404


@app.route('/api')
def session_api():
	return jsonify(list(session.keys()))