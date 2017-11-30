from flask_restful import Resource
from . import Models as model
from flask import request, abort

import sqlalchemy


class Todo(Resource):

    def get(self):
        q = model.session.query(model.Todo)
        ret = []
        for r in q:
            ret.append({'name': r.name, 'desc': r.desc})
        return ret

    def put(self):
        js = request.get_json()

        try:
            td = model.Todo(name=js.get('name'), desc=js.get('desc'))
            model.session.add(td)
            model.session.commit()
            return 'Ok', 200

        except sqlalchemy.exc.IntegrityError:
            model.session.rollback()
            abort(409)
        except sqlalchemy.exc.InvalidRequestError:
            model.session.rollback()

    def post(self):
        js = request.get_json()

        todo = model.session.query(model.Todo).filter_by(name=js['old_name']).first()
        if todo is None:
            abort(404)
        todo.name = js['new_name']
        todo.desc = js.get('new_desc', todo.desc)
        model.session.commit()
        return 'Ok', 200

    def delete(self):
        js = request.get_json()

        model.session.query(model.Todo).filter(model.Todo.name == js.get('name')).\
            delete(synchronize_session=False)
        model.session.commit()
        return 'Ok', 200


class Task(Resource):

    def get(self, todo_name):
        r = model.session.query(model.Todo).filter_by(name=todo_name).first()
        if r is None:
            abort(404)
        q = model.session.query(model.Task).filter_by(todo_id=r.id)
        ret = []
        for res in q:
            ret.append({'name': res.name, 'desc': res.desc, 'done': res.done})
        return ret

    def put(self, todo_name):
        js = request.get_json()
        todo = model.session.query(model.Todo).filter_by(name=todo_name).first()
        if todo is None:
            abort(404)
        task = model.Task(name=js['name'], desc=js.get('desc'), done=False, todo_id=todo.id)
        model.session.add(task)
        model.session.commit()
        return 'Ok', 200

    def post(self, todo_name):
        js = request.get_json()
        todo = model.session.query(model.Todo).filter_by(name=todo_name).first()
        if todo is None:
            abort(404)
        task = model.session.query(model.Task).filter_by(todo_id=todo.id, name=js['name']).first()
        task.done = not task.done
        model.session.commit()
        return 'Ok', 200

    def delete(self, todo_name):
        js = request.get_json()
        todo = model.session.query(model.Todo).filter_by(name=todo_name).first()
        if todo is None:
            abort(404)
        model.session.query(model.Task).filter(model.Task.name == js['name'],
                                               model.Task.todo_id == todo.id).delete(synchronize_session=False)
        model.session.commit()
        return 'Ok', 200
