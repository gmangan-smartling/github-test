import sys
import os
import logging
import requests
import json
import time

access_token = None
refresh_token = None
refresh_time = None

def authenticate():
	global access_token
	global refresh_token
	global refresh_time

	if access_token is None: 
		with open('creds.json') as f:
			data = json.load(f)
		#print "first time"
		USER_IDENTIFIER = data["userIdentifier"]
		#PROJECT_ID = data["projectId"]
		USER_SECRET = data["userSecret"]
		# call auth function and return access token
		r = requests.post('https://api.smartling.com/auth-api/v2/authenticate', json = {"userIdentifier":USER_IDENTIFIER,"userSecret":USER_SECRET})
		access_token = r.json()['response']['data']['accessToken']
		refresh_token = r.json()['response']['data']['refreshToken']
		expires_in = r.json()['response']['data']['expiresIn']

		refresh_time = time.time() + expires_in - 20
	if time.time() > refresh_time:
		r = requests.post('https://api.smartling.com/auth-api/v2/authenticate/refresh', json = {"refreshToken":refresh_token})
		access_token = r.json()['response']['data']['accessToken']
		refresh_token = r.json()['response']['data']['refreshToken']
		expires_in = r.json()['response']['data']['expiresIn']
		refresh_time = time.time() + expires_in - 3000

	return access_token
