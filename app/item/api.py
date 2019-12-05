import os
import json

from flask import request, jsonify, Blueprint
from werkzeug.utils import secure_filename

from app.common.decorator import token_required
from app.models import items
from run import app, db
from app.item import itembp


UPLOAD_FOLDER = "imagesUpload"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/upload',methods=['POST'])
def image_upload(new_item, current_user):

    try:
        if request.method == "POST":
            if "file[]" not in request.files:
                return jsonify({"message": "No file is selected1"})
            files = request.files.getlist("file[]")
            file_paths = ""
            for file in files:
                # if file.filename == '':
                # return jsonify({'message': 'No file is selected1'})
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(
                        app.config["UPLOAD_FOLDER"], filename + "" + current_user.id
                    )
                    file.save(file_path)
                    file_paths = file_path + "," + file_path
                    # new_item.image_path=file_path
                    # filestr=str(file)
            new_item.image_path = file_paths
            return jsonify({"message": "files uploaded"})
            # return jsonify({'message':'please select image file'})

    except Exception as e:
        return str(e)


@itembp.route("/addPost", methods=["POST"])
@token_required
def add_post(current_user):
    if not current_user:
        return jsonify({"message": "please login first to perform this operation"})
    # data = request.get_json()
    data = json.loads(request.form["data"])
    new_item = items(
        name=data["name"],
        description=data["description"],
        category=data["category"],
        location=data["location"],
        date=data["date"],
    )
    new_item.user_id = current_user.id
    if "category" in data:
        if data["category"] == "found":
            image_upload(new_item, current_user)
            # return 'hello'
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "New item added"})


@itembp.route("/allPosts", methods=["GET"])
@token_required
def all_posts(current_user):
    if not current_user:
        return jsonify({"message": "please login first to perform this operation"})
    _Items = items.query.all()
    if not _Items:
        return jsonify({"message": "No item exist"})
    data = []
    for item in _Items:
        item_data = {}
        item_data["name"] = item.name
        item_data["description"] = item.description
        item_data["category"] = item.category
        item_data["location"] = item.location
        item_data["date"] = item.date
        data.append(item_data)
    return jsonify({"All Item": data})


@itembp.route("/deletePost/<item_id>", methods=["DELETE"])
@token_required
def delete_post(current_user, item_id):
    if not current_user:
        return jsonify({"message": "login first"})
    item = items.query.filter_by(id=item_id).first()
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


@itembp.route("/searchPost/<name>", methods=["GET"])
@token_required
def search_post(current_user, name):

    item = items.query.filter_by(name=name).first()
    if not item:
        return jsonify({"message": "item not found"})
    item_data = {"name": item.name, "description": item.description, "category": item.category,
                 "location": item.location, "date": item.date}
    return jsonify({"item": item_data})


@itembp.route("/updatePost/<id>", methods=["PUT"])
@token_required
def update_post(current_user, id):
    if not current_user:
        return jsonify({"message": "Login first"})
    data = request.get_json()
    item = items.query.filter_by(id=id).first()
    if not item:
        return jsonify({"message": "Item does not exist"})
    else:
        if item.user_id == current_user.id:
            if "name" in data:
                item.name = data["name"]
            if "description" in data:
                item.description = data["description"]
            if "date" in data:
                item.date = data["date"]
            if "location" in data:
                item.location = data["location"]
            if "category" in data:
                item.category = data["category"]
            db.session.commit()
            return jsonify({"message": "Post is updated"})
        else:
            return jsonify({"message": "you cannot update this Post"})
    return jsonify({"message": "Post is not updated ,try again later"}), 400

