from flask_restful import Resource
from . import Models as model
from flask import request, abort
   # import session, Task, Todo


class Todo(Resource):

    def get(self):
        q = model.session.query(model.Todo)
        ret = []
        for r in q:
            ret.append({'name': r.name, 'desc': r.desc})
        return ret

    def put(self):
        td = model.Todo(name=request.args.get('name'), desc=request.args.get('desc'))
        model.session.add(td)
        model.session.commit()
        return 'Ok', 200

    def post(self):
        todo = model.session.query(model.Todo).filter_by(name=request.args.get('old_name')).first()
        if todo is None:
            abort(404)
        todo.name = request.args.get('new_name')
        todo.desc = request.args.get('new_desc', todo.desc)
        model.session.commit()
        return 'Ok', 200

class Task(Resource):

    def get(self):
        model
        return None

    def get(self, todo_id):

        return todo_id + request.args.get('username')

    def put(self):
        pass

    def post(self):
        pass