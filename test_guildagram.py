import os
import tempfile
import random
import pytest

import guildagram

# generate a random suffix so we can use a live MongoDB instance to run these tests
rand_suffix = str(random.randint(0,9000000))

@pytest.fixture
def client():
    guildagram.app.config['TESTING'] = True

def test_get_messages_no_sender_success(client):
    rv = guildagram.get_messages('steve' + rand_suffix, None)
    assert len(rv[0]['messages']) == 0
    assert rv[1] == 200

def test_get_messages_success(client):
    rv = guildagram.get_messages('steve' + rand_suffix, 'earl' + rand_suffix)
    assert len(rv[0]['messages']) == 0
    assert rv[1] == 200

def test_get_messages_no_recipient_failure(client):
    rv = guildagram.get_messages('', None)
    assert rv[0]['success'] == False
    assert 'Receiver is not valid.' in rv[0]['message']
    assert rv[1] == 400

def test_send_message_success_case_end_to_end(client):
    guildagram.send_message_handler('steve' + rand_suffix, 'earl' + rand_suffix, 'hello earl this is steve')
    rv = guildagram.get_messages('steve' + rand_suffix, 'earl' + rand_suffix)
    assert len(rv[0]['messages']) == 1
    assert rv[1] == 200

def test_send_message_failure_invalid_recipient_empty(client):
    rv = guildagram.send_message_handler('steve' + rand_suffix, '', 'hello earl this is steve')
    assert rv[0]['success'] == False
    assert 'Sender is not valid.' in rv[0]['message']
    assert rv[1] == 400

def test_send_message_failure_invalid_sender_empty(client):
    rv = guildagram.send_message_handler('', 'earl' + rand_suffix, 'hello earl this is steve')
    assert rv[0]['success'] == False
    assert 'Receiver is not valid.' in rv[0]['message']
    assert rv[1] == 400

def test_send_message_failure_invalid_message_empty(client):
    rv = guildagram.send_message_handler('steve' + rand_suffix, 'earl' + rand_suffix, '')
    assert rv[0]['success'] == False
    assert 'Message text is not valid.' in rv[0]['message']
    assert rv[1] == 400

def test_get_messages_latest_first(client):
    guildagram.send_message_handler('bob' + rand_suffix, 'joe' + rand_suffix, 'hello joe this is bob')
    guildagram.send_message_handler('bob' + rand_suffix, 'joe' + rand_suffix, 'hello joe this is bob again')
    rv = guildagram.get_messages('bob' + rand_suffix, 'joe' + rand_suffix)
    assert len(rv[0]['messages']) == 2
    assert 'hello joe this is bob again' in rv[0]['messages'][0]['content']
    assert rv[0]['messages'][0]['when'] >= rv[0]['messages'][1]['when']
    assert rv[1] == 200