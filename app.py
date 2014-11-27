from flask import Flask, request, render_template, url_for, redirect, jsonify
import soundcloud
import vlc
import requests
import json
import time
import os
import xml.etree.ElementTree as ET
from connection import ScDetails

details = ScDetails();
client = soundcloud.Client(client_id=details.client_id, client_secret=details.client_secret, username=details.username, password=details.password)


class VlcPlayer:
	def __init__(self):
		self.instance = vlc.Instance()
		self.player = self.instance.media_player_new()
	def play(self, stream_url):
		self.media = self.instance.media_new(stream_url)
		self.player.set_media(self.media)
		self.player.play()
		return self.player

	def stop(self):
		self.player.stop()

	def pause(self):
		self.player.pause()

player = VlcPlayer()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
	return render_template('index.html', home=True)

@app.route("/stream")
def stream():
	return render_template('stream.html', stream=True)

@app.route("/favourites")
def favourites():
	return render_template('favourites.html', favourites=True)

@app.route("/others_favourites")
def others_favourites():
	return render_template('others_favourites.html', otherfavourites=True)

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
		print dir(stream_url.keys())
		player.play(stream_url.location)
	return jsonify({'are you ready to rock?' : 'fuck yeah!'})

@app.route("/get_tracks")
def get_tracks():
	# if current file exists and is less than a day old
	if os.path.isfile('data/list.txt') and os.path.getmtime('data/list.txt') > (time.time() - 86400):
		with open('data/list.txt') as data:
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
					tracks.append(dict(
						id=track.id,
						duration=track.duration,
						title=track.title,
						stream_url=track.stream_url,
						user=track.user['username'],
						date=track.created_at,
						permalink=track.permalink_url
					))
		with open('data/list.txt', 'w') as outfile:
			json.dump({'tracks' : tracks}, outfile)
		return jsonify({ 'tracks' : tracks })

@app.route("/get_favourites")
def get_favourites():
	# if current file exists and is less than a day old
	if os.path.isfile('data/favourites.txt') and os.path.getmtime('data/favourites.txt') > (time.time() - 86400):
		with open('data/favourites.txt') as data:
			return jsonify(json.load(data))

	# otherwise regenerate the file
	else:
		me = client.get('/me/')
		fav_tracks = client.get('/users/' + str(me.id) + '/favorites')
		tracks = []
		for track in fav_tracks:
			if hasattr(track, 'stream_url'):
				tracks.append(dict(
					id=track.id,
					duration=track.duration,
					title=track.title,
					stream_url=track.stream_url,
					user=track.user['username'],
					date=track.created_at,
					permalink=track.permalink_url
				))
		with open('data/favourites.txt', 'w') as outfile:
			json.dump({'tracks' : tracks}, outfile)
		return jsonify({ 'tracks' : tracks })


@app.route("/get_others_favourites")
def get_others_favourites():
	# if current file exists and is less than a day old
	if os.path.isfile('data/others_favourites.txt') and os.path.getmtime('data/others_favourites.txt') > (time.time() - 86400):
		with open('data/others_favourites.txt') as data:
			return jsonify(json.load(data))

	# otherwise regenerate the file
	else:
		followers = client.get('/me/followings')
		users = [dict(id=follow.id, username=follow.username) for follow in followers]
		tracks = []
		for user in users:
			user_tracks = client.get('/users/' + str(user['id']) + '/favorites')
		 	for track in user_tracks:
				if hasattr(track, 'stream_url'):
					tracks.append(dict(
						id=track.id,
						duration=track.duration,
						title=track.title,
						stream_url=track.stream_url,
						user=track.user['username'],
						date=track.created_at,
						permalink=track.permalink_url,
						favourited=user['username']
					))
		with open('data/others_favourites.txt', 'w') as outfile:
			json.dump({'tracks' : tracks}, outfile)
		return jsonify({ 'tracks' : tracks })
		return 'test'

@app.route('/embedcode', methods=['GET', 'POST'])
def embedcode():
	if request.method == 'POST':
		track_url = request.json['url']
		url = request.json['url']
		embed = client.get('/oembed', url=track_url)
		return embed.html.encode('utf8')
	return 'test'

@app.route('/radio6')
def radio6():
	xml = requests.get('http://bbc.co.uk/radio/listen/live/r6.asx')
	tree = ET.fromstring(xml.content)
	stream = tree.find('Entry').find('ref').attrib['href']
	player.play(stream);
	return redirect(url_for('hello'))

@app.route('/stop')
def stop():
	player.stop()
	return jsonify({'response' : 'ssssshhh!'})

if __name__ == "__main__":
	app.debug = True
	app.run()
