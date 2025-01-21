from flask import Blueprint, request, jsonify
from models import db, UserGroupQuery
from http import HTTPStatus
from .common import create_success_response, paginate_query, create_error_response, create_error
from uuid import uuid4

# Relative import not necessary apparently.

user_group_queries_routes = Blueprint("user_group_queries_routes", __name__)


@user_group_queries_routes.route("/user-group-queries", methods=["GET"])
def get_user_group_queries():
    user_group_queries_query = UserGroupQuery.query.all()
    paginated_users, meta, links = paginate_query(user_group_queries_query, request.args, "/v1/api/user-group-queries")
    return (
        jsonify(
            create_success_response(
                data=paginated_users,
                meta=meta,
                links=links,
                message="UserGroupQuerys fetched successfully",
            )
        ),
        HTTPStatus.OK,
    )


@user_group_queries_routes.route("/user-group-queries/<string:user_group_query_id>", methods=["GET"])
def get_user_group_query(user_group_query_id):
    user_group_query = UserGroupQuery.query.get_or_404(user_group_query_id).get_as_dict()
    data = {**user_group_query, "links": {"self": f"/v1/api/user-group-queries/{user_group_query_id}"}}
    return (
        jsonify(
            create_success_response(
                data=data,
                message="UserGroupQuery fetched successfully",
            )
        ),
        HTTPStatus.OK,
    )


@user_group_queries_routes.route("/user-group-queries", methods=["POST"])
def create_user_group_query():
    if not request.is_json:
        return (
            jsonify(
                create_error_response([create_error("INVALID_CONTENT_TYPE", "Content-Type must be application/json"), {"header": "Content-Type"}])
            ),
            HTTPStatus.BAD_REQUEST,
        )

    data = request.get_json()
    # If additional key-values are given, simply ignore these.
    required_fields = ["user_id", "group_id"]
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
        new_user_group_query = UserGroupQuery(id=str(uuid4().hex), user_id=data["user_id"], group_id=data["group_id"])
        db.session.add(new_user_group_query)
        db.session.commit()
        data = {
            "id": new_user_group_query.id,
            "type": "user",
            "attributes": {"user_id": new_user_group_query.user_id, "group_id": new_user_group_query.group_id},
            "links": {"self": f"v1/api/user-group-queries/{new_user_group_query.id}"},
        }
        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="UserGroupQuery created successfully",
                )
            ),
            HTTPStatus.CREATED,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST


@user_group_queries_routes.route("/user-group-queries/<string:user_group_query_id>", methods=["DELETE"])
def delete_user_group_query(user_group_query_id):
    user_group_query = UserGroupQuery.query.get(user_group_query_id)

    if not user_group_query:
        return (
            jsonify(
                create_error_response(
                    [create_error("RESOURCE_NOT_FOUND", f"UserGroupQuery with id {user_group_query_id} not found", {"pointer": "/data/id"})]
                )
            ),
            HTTPStatus.NOT_FOUND,
        )

    try:
        db.session.delete(user_group_query)
        db.session.commit()
        return jsonify(create_success_response(message="UserGroupQuery deleted successfull")), HTTPStatus.NO_CONTENT

    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response({create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})})), HTTPStatus.BAD_REQUEST


@user_group_queries_routes.route("/user-group-queries/<string:user_group_query_id>", methods=["PATCH"])
def patch_user_group_query(user_group_query_id):
    user_group_queries_query = UserGroupQuery.query.get_or_404(user_group_query_id)
    data = request.get_json()

    # If no correct fields are given may still return a success -> TODO(@TS): Check what .commit() does for unchanged object

    if "user_id" in data:
        user_group_queries_query.user_id = data["user_id"]
    if "group_id" in data:
        user_group_queries_query.group_id = data["group_id"]

    try:
        db.session.commit()
        data = {**user_group_queries_query.get_as_dict(), "links": {"self": f"/v1/api/user-group-queries/{user_group_queries_query.id}"}}

        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="UserGroupQuery updated successfully",
                )
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST


@user_group_queries_routes.route("/user-group-queries/<string:user_group_query_id>", methods=["PUT"])
def put_user_group_query(user_group_query_id):
    user_group_queries_query = UserGroupQuery.query.get_or_404(user_group_query_id)
    data = request.get_json()

    required_fields = ["user_id", "group_id"]
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

    user_group_queries_query.user_id = data["user_id"]
    user_group_queries_query.group_id = data["group_id"]

    try:
        db.session.commit()
        data = {**user_group_queries_query.get_as_dict(), "links": {"self": f"/v1/api/user-group-queries/{user_group_queries_query.id}"}}
        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="UserGroupQuery updated successfully",
                )
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST
