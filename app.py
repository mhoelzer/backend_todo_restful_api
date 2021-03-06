from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

import datetime

app = Flask(__name__)
api = Api(app)

todo_list = {}

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, default="You forgot a title :(")
parser.add_argument("due_date", type=str, default="Not today, Satan")
parser.add_argument("completed", type=bool, default=False)

todo_id = 0
current_datetime = datetime.datetime.now()


def nonexistant_todo(todo_id):
    """if a todo doesn't exist, just abort but don't flip out too much"""
    if todo_id not in todo_list:
        abort(404, message=f"{todo_id} doesn't exist")


class TodoList(Resource):
    """this is the big list with all the todos b/c strength in numbers"""
    def get(self):
        """show all the todos you have"""
        return todo_list

    def post(self):
        """create a todo"""
        global todo_id
        todo_id = int(todo_id) + 1
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
    """this is for individual todos"""
    def get(self, todo_id):
        """get a specific todo based on id b/c they want to feel special"""
        nonexistant_todo(todo_id)
        return todo_list[todo_id]

    def put(self, todo_id):
        """update a todo"""
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
        """delete a todo b/c it isn't worth the effort anymore"""
        nonexistant_todo(todo_id)
        del todo_list[todo_id]
        return 204


api.add_resource(TodoList, "/todos")
api.add_resource(TodoItem, "/todos/<todo_id>")

if __name__ == "__main__":
    app.run(debug=True)
