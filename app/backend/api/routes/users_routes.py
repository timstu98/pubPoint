from flask import Blueprint, request, jsonify
from models import db, User, Group, UserGroupQuery
from http import HTTPStatus
from .common import create_success_response, paginate_query, create_error_response, create_error
from uuid import uuid4
import os

# Relative import not necessary apparently.
API_VERSION = os.getenv("API_VERSION", "vX")
api_url_prefix = f"/api/{API_VERSION}"

users_routes = Blueprint("users_routes", __name__)


@users_routes.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    paginated_users, meta, links = paginate_query(users, request.args, "{api_url_prefix}/users")
    return (
        jsonify(
            create_success_response(
                data=paginated_users,
                meta=meta,
                links=links,
                message="Users fetched successfully",
            )
        ),
        HTTPStatus.OK,
    )


@users_routes.route("/users/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id).get_as_dict()
    data = {**user, "links": {"self": f"{api_url_prefix}/users/{user_id}"}}
    return (
        jsonify(
            create_success_response(
                data=data,
                message="User fetched successfully",
            )
        ),
        HTTPStatus.OK,
    )


@users_routes.route("/users", methods=["POST"])
def create_user():
    if not request.is_json:
        return (
            jsonify(
                create_error_response([create_error("INVALID_CONTENT_TYPE", "Content-Type must be application/json"), {"header": "Content-Type"}])
            ),
            HTTPStatus.BAD_REQUEST,
        )

    data = request.get_json()
    # If additional key-values are given, simply ignore these.
    required_fields = ["address", "first_name", "second_name"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return (
            jsonify(
                create_error_response(
                    [
                        create_error(
                            "MISSING_REQUIRED_FIELDS",
                            f"Missing required fields: {', '.join(missing_fields)}",
                            {"pointer": f"/data/attributes/{missing_fields[0]}"},
                        )
                    ]
                )
            ),
            HTTPStatus.BAD_REQUEST,
        )

    try:
        new_user = User(id=str(uuid4().hex), address=data["address"], first_name=data["first_name"], second_name=data["second_name"])
        db.session.add(new_user)
        db.session.commit()
        data = {
            "id": new_user.id,
            "type": "user",
            "attributes": {"address": new_user.address, "first_name": new_user.first_name, "second_name": new_user.second_name},
            "links": {"self": f"{api_url_prefix}/users/{new_user.id}"},
        }
        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="User created successfully",
                )
            ),
            HTTPStatus.CREATED,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST


@users_routes.route("/users/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return (
            jsonify(create_error_response([create_error("RESOURCE_NOT_FOUND", f"User with id {user_id} not found", {"pointer": "/data/id"})])),
            HTTPStatus.NOT_FOUND,
        )

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(create_success_response(message="User deleted successfull")), HTTPStatus.NO_CONTENT

    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response({create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})})), HTTPStatus.BAD_REQUEST


@users_routes.route("/users/<string:user_id>", methods=["PATCH"])
def patch_user(user_id):
    user_query = User.query.get_or_404(user_id)
    data = request.get_json()

    # If no correct fields are given may still return a success -> TODO(@TS): Check what .commit() does for unchanged object

    if "address" in data:
        user_query.address = data["address"]
    if "first_name" in data:
        user_query.first_name = data["first_name"]
    if "second_name" in data:
        user_query.second_name = data["second_name"]

    try:
        db.session.commit()
        data = {**user_query.get_as_dict(), "links": {"self": f"{api_url_prefix}/users/{user_query.id}"}}

        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="User updated successfully",
                )
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST


@users_routes.route("/users/<string:user_id>", methods=["PUT"])
def put_user(user_id):
    user_query = User.query.get_or_404(user_id)
    data = request.get_json()

    required_fields = ["address", "first_name", "second_name"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return (
            jsonify(
                create_error_response(
                    [
                        create_error(
                            "MISSING_REQUIRED_FIELDS",
                            f"Missing required fields: {', '.join(missing_fields)}",
                            {"pointer": f"/data/attributes/{missing_fields[0]}"},
                        )
                    ]
                )
            ),
            HTTPStatus.BAD_REQUEST,
        )

    user_query.address = data["address"]
    user_query.first_name = data["first_name"]
    user_query.second_name = data["second_name"]

    try:
        db.session.commit()
        data = {**user_query.get_as_dict(), "links": {"self": f"{api_url_prefix}/users/{user_query.id}"}}
        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="User updated successfully",
                )
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST


@users_routes.route("/users/<string:user_id>/groups", methods=["GET"])
def get_user_groups(user_id):
    # Verify group exists
    user = User.query.get_or_404(user_id)

    # Get users through relationship
    groups_query = Group.query.join(UserGroupQuery).filter(UserGroupQuery.user_id == user_id)

    # Paginate users
    paginated_groups, meta, links = paginate_query(groups_query, request.args, f"{api_url_prefix}/groups/{user_id}/users")

    return (
        jsonify(
            create_success_response(
                data=user.get_as_dict(),
                meta=meta,
                links=links,
                message=f"User {user_id} with groups fetched successfully",
                included=paginated_groups,
            )
        ),
        HTTPStatus.OK,
    )
