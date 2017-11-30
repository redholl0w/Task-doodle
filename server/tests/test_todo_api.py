import requests
import os
import pytest

os.environ['no_proxy'] = '127.0.0.1,localhost'

os.system('rm todo.db')

url = 'http://127.0.0.1:5000/todos/'


##################################################################################################
#                                        SUCCESS TEST                                            #
##################################################################################################

def test_get_init():
    r = requests.get(url)
    assert(r.json() == [])


def test_put():
    payload = {'name': 'Todo test 1', 'desc': 'This is a Todo list test'}
    r = requests.put(url, json=payload)
    assert(r.json() == 'Ok' and r.status_code == 200)


def test_get():
    r = requests.get(url)
    assert(r.json() == [{'name': 'Todo test 1', 'desc': 'This is a Todo list test'}])


def test_post():
    payload = {'old_name': 'Todo test 1', 'new_name': 'Still todo test 1'}
    r = requests.post(url, json=payload)
    assert (r.json() == 'Ok' and r.status_code == 200)


def test_get_update_name():
    r = requests.get(url)
    assert (r.json() == [{'name': 'Still todo test 1', 'desc': 'This is a Todo list test'}] or
            r.json() == [{'desc': 'This is a Todo list test', 'name': 'Still todo test 1'}])


def test_delete():
    payload = {'name': 'Still todo test 1'}
    r = requests.delete(url, json=payload)
    assert (r.json() == 'Ok' and r.status_code == 200)


def test_get_after_delete():
    r = requests.get(url)
    assert(r.json() == [])

##################################################################################################
#                                   EXPECTED FAILURE TEST                                        #
##################################################################################################


