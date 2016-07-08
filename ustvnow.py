import sys, os, re
import urllib, urllib2, socket, cookielib
import json, random
import time, datetime
from time import time
from datetime import datetime, timedelta


mBASE_URL = 'http://m-api.ustvnow.com'
mcBASE_URL = 'http://mc.ustvnow.com'
live_stream_option = '1'
free_package = 'true'
stream_dir = 'Streams'
quality = 3


def get_link(user, password, quality):
	token = login(user, password)
	passkey = get_passkey(token)
	content = get_json('gtv/1/live/channelguide', {'token': token})
	channels = []
	results = content['results'];
	quality = (quality + 1)
	stream_type = 'rtmp'
	for i in results:
		try:
			if i['order'] == 1:
				if quality == 4 and i['scode'] == 'whvl':
					quality = (quality - 1)
				#used for alternate stream options
				src = i['app_name'];
				#used for alternate stream options
				name = i['stream_code']
				stream = get_json('stream/1/live/view', {'token': token, 'key': passkey, 'scode': i['scode']})['stream']
				if live_stream_option == '0':
					url = stream.replace('smil:', 'mp4:').replace('USTVNOW1', 'USTVNOW').replace('USTVNOW', 'USTVNOW' + str(quality))
				else:
					url = stream_type + '://' + str(src) + '.is.ustvnow.com:1935/' + src + '?key=' + passkey + '/mp4:' + i['streamname'] + str(quality)
				if free_package == 'true':
					if name in ['CW','ABC','FOX','PBS','CBS','NBC','MY9']:
						channels.append({ 
							'name': name,    
							'url': url
							 })
				else:
					channels.append({
						'name': name,
						'url': url
						})
		except:
			pass
	return channels



def get_json(path, queries={}):
	content = False
	url = build_json(path, queries)
	response = fetch(url)
	if response:
		content = json.loads(response.read())
	else:
		content = False
	return content    


def build_json(path, queries={}):
	if queries:
		query = urllib.urlencode(queries)
		return '%s/%s?%s' % (mBASE_URL, path, query)
	else:
		return '%s/%s' % (mBASE_URL, path)


def login(user, password):
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
	opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.127 Large Screen Safari/533.4 GoogleTV/162671')]
	urllib2.install_opener(opener)
	url = build_json('gtv/1/live/login', {'username': user, 
										   'password': password, 
										   'device':'gtv', 
										   'redir':'0'})
	response = opener.open(url)
	for cookie in cj:
		if cookie.name == 'token':
			return cookie.value
		else:
			print("Nope! 2")
	return 'False'    


def fetch(url, form_data=False):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	if form_data:
		req = urllib2.Request(url, form_data)
	else:
		req = url
		try:
			response = opener.open(req)
			return response
		except urllib2.URLError, e:
			return False


def get_passkey(token):
	passkey = get_json('gtv/1/live/viewdvrlist', {'token': token})['globalparams']['passkey']
	return passkey			


channels = get_link(user, password, quality)

f = open(stream_dir + '/USTV' + '.txt', 'w')
for channel in channels:
	f.write(channel["name"] + " " + channel["url"] + "\n")
f.close()