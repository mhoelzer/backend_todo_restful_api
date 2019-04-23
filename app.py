from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class TodoList(Resource):
    def get(self):
        return {"hello": "no"}


class TodoItem(Resource):
    def get(self):
        pass


class TodoUpdate(Resource):
    def put(self):
        pass


class TodoDelete(Resource):
    def delete(self):
        pass


api.add_resource(TodoList, "/todolist")
api.add_resource(TodoItem, "/todoitem/<int:id>")
api.add_resource(TodoUpdate, "/todoitem/<int:id>/update")
api.add_resource(TodoDelete, "/todoitem/<int:id>/delete")

if __name__ == "__main__":
    app.run(debug=True)

# generix todo class; check local dic to see if another num is there, figure out what num you can assign to it; if asks for an id, get only works with current ids
