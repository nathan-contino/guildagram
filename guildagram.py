from flask import Flask, request
from flask_mongoengine import MongoEngine
from flask_api import status
import datetime

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
	'db': 'guildagram',
	'host': 'localhost',
	'port': 27017
}

db = MongoEngine()
db.init_app(app)

MAX_MESSAGES_PER_REQUEST=100

class Message(db.Document):
	receiver = db.StringField()
	sender = db.StringField()
	content = db.StringField()
	when = db.DateTimeField()
	def to_json(self):
		return {
				"receiver": self.name,
				"sender": self.email,
				"content": self.content,
				"when": self.when
				}

def is_valid_user(user):
	if user == None or user == "":
		return False
	return True

def is_valid_message(message):
	if message == None or message == "":
		return False
	return True

def create_result(success, message, code):
	result_body = {}
	result_body["success"] = success
	result_body["message"] = message
	return (result_body, code)

@app.route('/sendMessage', methods=['POST'])
def send_message():
	message = request.json
	send_message_handler(message.get("receiver"), message.get("sender"), message.get("content"))

def send_message_handler(receiver, sender, content):
	if not is_valid_user(receiver):
		return create_result(False, "Receiver is not valid.", status.HTTP_400_BAD_REQUEST)
	if not is_valid_user(sender):
		return create_result(False, "Sender is not valid.", status.HTTP_400_BAD_REQUEST)
	if not is_valid_message(content):
		return create_result(False, "Message text is not valid.", status.HTTP_400_BAD_REQUEST)

	Message(receiver=receiver, sender=sender, content=content, when=datetime.datetime.utcnow()).save()
	return create_result(True, "Message send successful.", status.HTTP_201_CREATED)

@app.route('/getMessages/<receiver>', methods=['GET'], defaults={'sender': None})
@app.route('/getMessages/<receiver>/<sender>', methods=['GET'])
def get_messages(receiver, sender):
	matched_messages = {}
	thirty_days_ago = datetime.datetime.now() - datetime.timedelta(30)

	if not is_valid_user(receiver):
		return create_result(False, "Receiver is not valid.", status.HTTP_400_BAD_REQUEST)

	if sender != None:
		if not is_valid_user(sender):
			return create_result(False, "Sender is not valid.", status.HTTP_400_BAD_REQUEST)
		matched_messages["messages"] = Message.objects(receiver=receiver, sender=sender, when__gte=thirty_days_ago).limit(MAX_MESSAGES_PER_REQUEST)
	else:
		matched_messages["messages"] = Message.objects(receiver=receiver, when__gte=thirty_days_ago).limit(MAX_MESSAGES_PER_REQUEST)

	return (matched_messages, status.HTTP_200_OK)
