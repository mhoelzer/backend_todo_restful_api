from app import app

import json


def test_todolist_get():
    """can we get the list of todos?"""
    with app.test_client() as client:
        result = client.get("/todos")
        assert result.status_code == 200
        data = result.data.decode()
        assert isinstance(data, str)
        jsonified_data = json.loads(data)
        assert "1" not in jsonified_data  # no id of 1
        assert str({}) in str(jsonified_data)  # should be empty


def test_todolist_post():
    """can we add a new todo?"""
    with app.test_client() as client:
        # creating todo
        new_data = {
            "title": "test a",
            "creation_date": "12/31/2010",
            "last_update": "1/1/2011",
            "due_date": "1/1/2011",
            "completed": True,
            "completed_on": "1/1/2011"
        }
        result = client.post("/todos", json=new_data)
        assert result.status_code == 201
        assert result.data.decode()
        assert new_data["title"] != "You forgot a title :("
        assert new_data["completed"] is not False
        # testing for todo
        thats_what_ya_get = app.test_client().get("/todos")
        data = thats_what_ya_get.data.decode()
        jsonified_data = json.loads(data)
        assert thats_what_ya_get.status_code == 200
        assert thats_what_ya_get.data.decode()
        assert jsonified_data["1"]["title"] == "test a"


def test_todoitem_get():
    """can we get a specific todo?"""
    with app.test_client() as client:
        result = client.get("/todos/1")
        assert result.status_code == 200
        data = result.data.decode()
        assert result.data.decode()
        jsonified_data = json.loads(data)
        assert jsonified_data["title"] == "test a"


def test_todoitem_put():
    """can we edit a todo?"""
    with app.test_client() as client:
        # doing update
        data_update = {
            "title": "updated title"
        }
        result = client.put("/todos/1", json=data_update)
        assert result.status_code == 200
        assert result.data.decode()
        # testing for updates
        thats_what_ya_get = client.get("/todos")
        data = thats_what_ya_get.data.decode()
        jsonified_data = json.loads(data)
        assert thats_what_ya_get.status_code == 200
        assert thats_what_ya_get.data.decode()
        assert jsonified_data["1"]["title"] == "updated title"


def test_todoitem_delete():
    """can we delete a todo?"""
    with app.test_client() as client:
        result = client.delete("/todos/1")
        assert result.status_code == 200
        # testing if gone
        result = client.get("/todos/1")
        assert result.status_code == 404
