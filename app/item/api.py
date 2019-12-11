import os
import json

from flask import request, jsonify
from werkzeug.utils import secure_filename

from app.common.decorator import token_required, validate_schema, validate_json
from app.common.schema import item_schema
from app.item import itembp
from app.models import items
from run import app, db

basedir = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.abspath(os.path.join(basedir, "..", "..", "imagesUpload"))
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def image_upload(new_item, current_user):
    try:
        if request.method == "POST":
            if "file[]" not in request.files:
                return jsonify({"message": "No file is selected1"}), 401
            files = request.files.getlist("file[]")
            file_paths = ""
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(
                        app.config["UPLOAD_FOLDER"], filename + "" + str(current_user.id)
                    )
                    file.save(file_path)
                    file_paths = file_path + "," + file_path
            new_item.image_path = file_paths
    except:
        return jsonify({"message": "files not uploaded"}), 404


@itembp.route("/post", methods = ["POST"])
@token_required
@validate_json
@validate_schema(item_schema)
def add_post(current_user):
    """" function to add the post detail """
    if not current_user:
        return jsonify({"message": "please login first to perform this operation"}), 401
    data = json.loads(request.form["data"])
    new_item = items(
        name = data["name"],
        description = data["description"],
        category = data["category"],
        location = data["location"],
        date = data["date"],
    )
    new_item.user_id = current_user.id
    if "category" in data:
        if data["category"] == "found":
            image_upload(new_item, current_user)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "New Item added"}), 201


@itembp.route("/post", methods = ["GET"])
@token_required
def all_posts(current_user):
    """"function to view all post"""
    if not current_user:
        return jsonify({"message": "please login first to perform this operation"})
    _Items = items.query.all()
    if not _Items:
        return jsonify({"message": "No item exist"})
    data = []
    for item in _Items:
        item_data = item.to_json()
        data.append(item_data)
    return jsonify({"All Item": data}), 200


@itembp.route("/post/<item_id>", methods = ["DELETE"])
@token_required
def delete_post(current_user, item_id):
    """ function to delete a specific post"""
    if not current_user:
        return jsonify({"message": "login first"})
    item = items.query.filter_by(id = item_id).first()
    if not item:
        return jsonify({"message": "item not found"})
    else:
        if item.user_id == current_user.id:
            file_paths = str(item.image_path)
            if file_paths != "":
                _file_paths = file_paths.split(",")
                for path in _file_paths:
                    os.remove(path)
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "item successfully deleted"})
        else:
            return jsonify({"message": "you cannot perform this operation"})


@itembp.route("/post/<name>", methods = ["GET"])
@token_required
def search_post(current_user, name):
    """function to search a post"""
    item = items.query.filter_by(name = name).first()
    if not item:
        return jsonify({"message": "item not found"}), 404
    return jsonify({"item": item.to_json()}), 200


@itembp.route("/post/<id>", methods = ["PUT"])
@token_required
@validate_json
def update_post(current_user, id):
    """function to update post detail by its id"""
    if not current_user:
        return jsonify({"message": "Login first"}), 401
    data = request.get_json()
    item = items.query.filter_by(id = id).first()
    counter = 0
    if not item:
        return jsonify({"message": "Item does not exist"}), 404
    else:
        if item.user_id == current_user.id:
            if "name" in data:
                item.name = data["name"]
                counter += 1
            if "description" in data:
                item.description = data["description"]
                counter += 1
            if "date" in data:
                item.date = data["date"]
                counter += 1
            if "location" in data:
                item.location = data["location"]
                counter += 1
            if "category" in data:
                item.category = data["category"]
                counter += 1
            if counter > 0:
                db.session.commit()
                return jsonify({"message": "Post is updated"}), 200
            else:
                return jsonify({"message": "Post cannot be updated"}), 403
        else:
            return jsonify({"message": "you cannot update this Post"}), 403

