from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

import datetime

app = Flask(__name__)
api = Api(app)


# todo_practice_list = {
#     "todo1": {
#         "title": "test a",
#         "creation_date": "12/31/2010",
#         "last_update": "1/1/2011",
#         "due_date": "1/1/2011",
#         "completed": True,
#         "completed_on": "1/1/2011"
#     },
#     "todo2": {
#         "title": "teszt2",
#         "creation_date": "1/2/2013",
#         "last_update": "1/3/2013",
#         "due_date": "1/4/2013",
#         "completed": False,
#         "completed_on": ""
#     }
# }

todo_list = {}

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, default="You forgot a title :(")
parser.add_argument("due_date", type=str, default="Not today, Satan")
parser.add_argument("completed", type=bool, default=False)

todo_id = 0
current_datetime = datetime.datetime.now()


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in todo_list:
        abort(404, message=f"{todo_id} doesn't exist")


class TodoList(Resource):
    def get(self):
        if not todo_list:
            return "WTF is this? Add some friggin' todos"
        return todo_list

    def post(self):
        global todo_id
        todo_id += 1
        todo_id = str(todo_id)
        args = parser.parse_args()
        todo_list[todo_id] = {
            "title": args["title"],
            "due_date": args["due_date"],
            "completed": args["completed"],
            "completed_on": str(current_datetime),
            "creation_date": str(current_datetime),
            "last_update": str(current_datetime)
        }
        return todo_id, 201


class TodoItem(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return todo_list[todo_id]

    def put(self, todo_id):
        args = parser.parse_args()
        if args["title"]:
            todo_list[todo_id].update({"title": args["title"]})
        if args["completed"]:
            todo_list[todo_id].update({"completed": args["completed"]})
            if args["completed"] is True:
                todo_list[todo_id].update(
                    {"completed_on": str(current_datetime)})
            if args["completed"] is not True:
                todo_list[todo_id].update({"completed_on": "Not completed"})
        todo_list[todo_id].update(
            {"last_update": str(current_datetime)})
        return 201

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del todo_list[todo_id]
        return 204


api.add_resource(TodoList, "/todos")
api.add_resource(TodoItem, "/todos/<todo_id>")

if __name__ == "__main__":
    app.run(debug=True)

# generic todo class; check local dic to see if another num is there, figure out what num you can assign to it; if asks for an id, get only works with current ids
