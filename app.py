from flask import Flask, request, render_template, url_for, redirect, jsonify
import soundcloud
import vlc
import requests
import json
import time
import os
import xml.etree.ElementTree as ET

client = soundcloud.Client(client_id='xxx', client_secret='xxx', username='xxx', password='xxx')

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
	return render_template('index.html')


@app.route("/play", methods=['GET', 'POST'])
def play():
	if request.method == 'POST':
		url = request.form['url']
		track = client.get('/resolve', url=url)
		stream_url = client.get(track.stream_url, allow_redirects=False)
		player = vlc.MediaPlayer(stream_url.location)
		player.play();

	return redirect(url_for('hello'))

@app.route('/play_stream', methods=['POST'])
def play_stream():
	if request.method == 'POST':
		url = request.json['url']
		stream_url = client.get(url, allow_redirects=False)
		player = vlc.MediaPlayer(stream_url.location)
		player.play();
	return jsonify({'are you ready to rock?' : 'fuck yeah!'})

@app.route("/get_tracks")
def get_tracks():
	# if current file exists and is less than a day old
	if os.path.isfile('list.txt') and os.path.getmtime('list.txt') > (time.time() - 86400):
		with open('list.txt') as data:
			return jsonify(json.load(data))

	# otherwise regenerate the file
	else:
		followers = client.get('/me/followings')
		users = [follow.id for follow in followers]
		user_tracks = [client.get('/tracks/', user_id=user, limit=30, embeddable_by='me') for user in users]
		tracks = []
		for user in user_tracks:
			for track in user:
				if hasattr(track, 'stream_url'):
					tracks.append(dict(id=track.id, duration=track.duration, title=track.title, stream_url=track.stream_url,user=track.user['username']))
		with open('list.txt', 'w') as outfile:
			json.dump({'tracks' : tracks}, outfile)
		return jsonify({ 'tracks' : tracks })

@app.route('/radio6')
def radio6():
	xml = requests.get('http://bbc.co.uk/radio/listen/live/r6.asx')
	tree = ET.fromstring(xml.content)
	stream = tree.find('Entry').find('ref').attrib['href']
	player = vlc.MediaPlayer(stream)
	player.play();
	return redirect(url_for('hello'))

@app.route('/stop')
def stop():
	# player = g.get('player')
	# player.stop()
	return redirect(url_for('hello'))

if __name__ == "__main__":
	app.debug = True
	app.run()
