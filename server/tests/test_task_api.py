import requests
import os
import pytest

os.environ['no_proxy'] = '127.0.0.1,localhost'

os.system('rm todo.db')

todo_url = 'http://127.0.0.1:5000/todos/'
url = 'http://127.0.0.1:5000/todo/{}/task/'

##################################################################################################
#                                        SUCCESS TEST                                            #
##################################################################################################


@pytest.fixture()
def put_Test():
    payload = {'name': 'Todo test', 'desc': 'This is a Todo list test'}
    requests.put(todo_url, json=payload)


def test_get_empty_task(put_Test):
    r = requests.get(url.format('Todo test'))
    assert(r.json() == [] and r.status_code == 200)


def test_put_task():
    payload = {'name': 'Task test'}
    r = requests.put(url.format('Todo test'), json=payload)
    assert (r.json() == 'Ok' and r.status_code == 200)
    r = requests.get(url.format('Todo test'))
    assert (r.json() == [{'name': 'Task test', 'desc': None, 'done': False}])


def test_post_task():
    payload = {'name': 'Task test'}
    r = requests.post(url.format('Todo test'), json=payload)
    assert (r.json() == "Ok" and r.status_code == 200)
    r = requests.get(url.format('Todo test'))
    assert (r.json() == [{'name': 'Task test', 'desc': None, 'done': True}])


def test_lilou_wallace_multi_task():  # 5th element reference
    payload = {'name': 'Task test 1'}
    r = requests.put(url.format('Todo test'), json=payload)
    assert (r.json() == "Ok" and r.status_code == 200)
    r = requests.get(url.format('Todo test'))
    assert (r.json() == [{'name': 'Task test', 'desc': None, 'done': True},
                         {'name': 'Task test 1', 'desc': None, 'done': False}])


def test_delete_task():
    payload = {'name': 'Task test'}
    r = requests.delete(url.format('Todo test'), json=payload)
    assert (r.json() == 'Ok' and r.status_code == 200)
    r = requests.get(url.format('Todo test'))
    assert (r.json() == [{'name': 'Task test 1', 'desc': None, 'done': False}])

##################################################################################################
#                                   EXPECTED FAILURE TEST                                        #
##################################################################################################

@pytest.fixture()
def put_Test1():
    payload = {'name': 'Todo test 1', 'desc': 'This is a Todo list test'}
    requests.put(url, json=payload)


def test_post_no_existing_record():
    payload = {'old_name': 'I don\'t exist', 'new_name': 'I don\'t exist so what ever'}
    r = requests.post(url, json=payload)
    assert (r.status_code == 404)


def test_put_existing_record(put_Test1):
    payload = {'name': 'Todo test 1', 'desc': 'This is a Todo list test'}
    r = requests.put(url, json=payload)
    assert (r.status_code == 409)
