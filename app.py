from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import datetime

app = Flask(__name__)
api = Api(app)


todo_list = {
    "todo1": {
        "title": "test a",
        "creation_date": "12/31/10",
        "last_update": "1/1/11",
        "due_date": "1/1/11",
        "completed": True,
        "completed_on": "1/1/11"
    },
    "todo2": {
        "title": "teszt2",
        "creation_date": "1/2/13",
        "last_update": "1/3/13",
        "due_date": "1/4/13",
        "completed": False,
        "completed_on": ""
    }
}


parser = reqparse.RequestParser()
# parser.add_argument("id", type=int)
parser.add_argument("title", type=str)
# parser.add_argument("creation_date", type=int)
# parser.add_argument("last_update", type=int)
parser.add_argument("due_date", type=str)
parser.add_argument("completed", type=bool)
# parser.add_argument("completed_on", type=int)


class TodoList(Resource):
    def get(self):
        # if todo_list == []:
        #     return "WTF is this?"
        return todo_list

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(todo_list.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        todo_list[todo_id] = {
            "title": args["title"],
            "due_date": args["due_date"],
            "completed": args["completed"],
            "completed_on": str(datetime.datetime.now()),
            "creation_date": str(datetime.datetime.now()),
            "last_update": str(datetime.datetime.now())
        }
        return todo_list[todo_id], 201


class TodoItem(Resource):
    def get(self, todo_id):
        return todo_list[todo_id]

    def put(self, todo_id):
        args = parser.parse_args()
        if args["title"]:
            todo_list[todo_id].update({"title": args["title"]})
        if args["title"]:
            todo_list[todo_id].update({"title": args["title"]})
        if args["last_update"]:
            todo_list[todo_id].update({"last_update": args["last_update"]})
        return 201

    def delete(self, todo_id):
        del todo_list[todo_id]
        return "", 204


api.add_resource(TodoList, "/todos")
api.add_resource(TodoItem, "/todos/<todo_id>")

if __name__ == "__main__":
    app.run(debug=True)

# generix todo class; check local dic to see if another num is there, figure out what num you can assign to it; if asks for an id, get only works with current ids
