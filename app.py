from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Hello(Resource):
    def get(self):
        return {"hello": "no"}


api.add_resource(Hello.get, "/")

if __name__ == "__main__":
    app.run(debug=True)

# generix todo class; check local dic to see if another num is there, figure out what num you can assign to it; if asks for an id, get only works with current ids
