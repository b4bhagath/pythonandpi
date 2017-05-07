import os
from firebase import firebase
import requests
from twilio.rest import Client
from config import twilio_acc_id, twilio_acc_auth_token, twilio_number

firebase = firebase.FirebaseApplication('https://pieandpython.firebaseio.com/')

# updates firebase to the new state
def change_occupied_state(state):
	if state == 0:
		#toilet is now unoccupied
		firebase.put('/', 'occupied', 'false')
		#send text to next person in the queue
		get_next_in_queue()
	else:
		#toilet is now occupied 
		firebase.put('/', 'occupied', 'true')

# sends text to next in queue
def send_text(number, name):
	# Your Account Sid and Auth Token from twilio.com/user/account
	client = Client(twilio_acc_id, twilio_acc_auth_token)
	message = client.messages.create(body=name + " the toilet is now open!",
	    to= number,    # Replace with your phone number
	    from_=twilio_number) # Replace with your Twilio number
	print "text sent"


# gets next in queue
def get_next_in_queue():
	url = 'https://pieandpython.firebaseio.com/' +'queue.json?orderBy="$key"&limitToFirst=1&print=pretty'
	data = requests.get(url)
	json_object = data.json()
	person = None
	number = None

	# get lastest entry
	for key in json_object: 
		person = json_object[key]
	
	# check if anyone is in queue
	if person == None:
		print "no one in queue"
	else:
		name = person['name']
		number = os.getenv(name)
		# send text
		send_text(number, name)
		# delete entry
		firebase.delete('/queue', key)
