from flask_restful import Resource
from . import Models as model
from flask import request, abort
   # import session, Task, Todo
import sqlalchemy


class Todo(Resource):

    def get(self):
        q = model.session.query(model.Todo)
        ret = []
        for r in q:
            ret.append({'name': r.name, 'desc': r.desc})
        return ret

    def put(self):
        try:
            td = model.Todo(name=request.args.get('name'), desc=request.args.get('desc'))
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
        print(js['name'])
        todo = model.session.query(model.Todo).filter_by(name=request.args.get('old_name')).first()
        if todo is None:
            abort(404)
        todo.name = request.args.get('new_name')
        todo.desc = request.args.get('new_desc', todo.desc)
        model.session.commit()
        return 'Ok', 200

    def delete(self):
        model.session.query(model.Todo).filter(model.Todo.name == request.args.get('name')).\
            delete(synchronize_session=False)
        model.session.commit()
        return 'Ok', 200


class Task(Resource):

    def get(self):
        q = model.session.query(model.Task)

        ret = []
        for r in q:
            todo = model.session.query(model.Todo).filter_by(id=r.todo_id).first()
            ret.append({'name': r.name, 'desc': r.desc, 'done': r.done, 'todo': todo.name})
        return ret

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
        todo = model.session.query(model.Todo).filter_by(name=todo_name).first()
        if todo is None:
            abort(404)
        task = model.Task(name=request.args.get('name'), desc=request.args.get('desc'), done=False, todo_id=todo.id)
        model.session.add(task)
        model.session.commit()
        return 'Ok', 200

    def post(self, todo_name):
        todo = model.session.query(model.Todo).filter_by(name=todo_name).first()
        if todo is None:
            abort(404)
        task = model.session.query(model.Task).filter_by(todo_id=todo.id, name=request.args.get('name')).first()
        task.done = not task.done
        model.session.commit()
        return 'Ok', 200

    def delete(self, todo_name):
        todo = model.session.query(model.Todo).filter_by(name=todo_name).first()
        if todo is None:
            abort(404)
        model.session.query(model.Task).filter(model.Task.name == request.args.get('name'),
                                               model.Task.todo_id == todo.id).delete(synchronize_session=False)
        model.session.commit()
        return 'Ok', 200
