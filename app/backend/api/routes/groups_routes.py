from flask import Blueprint, request, jsonify
from models import db, Group, User, UserGroupQuery
from http import HTTPStatus
from .common import create_success_response, paginate_query, create_error_response, create_error
from uuid import uuid4

# from .services.pub_service import get_optimal_pub_for_group

groups_routes = Blueprint("groups_routes", __name__)


@groups_routes.route("/groups", methods=["GET"])
def get_groups():
    groups_query = Group.query.all()
    paginated_groups, meta, links = paginate_query(groups_query, request.args, "/v1/api/groups")
    return (
        jsonify(
            create_success_response(
                data=paginated_groups,
                meta=meta,
                links=links,
                message="Groups fetched successfully",
            )
        ),
        HTTPStatus.OK,
    )


@groups_routes.route("/groups/<string:group_id>", methods=["GET"])
def get_group(group_id):
    group = Group.query.get_or_404(group_id).get_as_dict()
    data = {**group, "links": {"self": f"/v1/api/groups/{group_id}"}}
    return (
        jsonify(
            create_success_response(
                data=data,
                message="Group fetched successfully",
            )
        ),
        HTTPStatus.OK,
    )


@groups_routes.route("/groups", methods=["POST"])
def create_group():
    if not request.is_json:
        return (
            jsonify(
                create_error_response([create_error("INVALID_CONTENT_TYPE", "Content-Type must be application/json"), {"header": "Content-Type"}])
            ),
            HTTPStatus.BAD_REQUEST,
        )

    data = request.get_json()
    # If additional key-values are given, simply ignore these.
    required_fields = ["suggested_pub_id"]
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
        new_group = Group(id=str(uuid4().hex), suggested_pub_id=data["suggested_pub_id"])
        db.session.add(new_group)
        db.session.commit()
        data = {
            "id": new_group.id,
            "type": "group",
            "attributes": {"suggested_pub_id": new_group.suggested_pub_id},
            "links": {"self": f"v1/api/groups/{new_group.id}"},
        }
        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="Group created successfully",
                )
            ),
            HTTPStatus.CREATED,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST


@groups_routes.route("/groups/<string:group_id>", methods=["DELETE"])
def delete_group(group_id):
    group = Group.query.get(group_id)

    if not group:
        return (
            jsonify(create_error_response([create_error("RESOURCE_NOT_FOUND", f"Group with id {group_id} not found", {"pointer": "/data/id"})])),
            HTTPStatus.NOT_FOUND,
        )

    try:
        db.session.delete(group)
        db.session.commit()
        return jsonify(create_success_response(message="Group deleted successfull")), HTTPStatus.NO_CONTENT

    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response({create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})})), HTTPStatus.BAD_REQUEST


@groups_routes.route("/groups/<string:group_id>", methods=["PATCH"])
def patch_group(group_id):
    group_query = Group.query.get_or_404(group_id)
    data = request.get_json()

    # If no correct fields are given may still return a success -> TODO(@TS): Check what .commit() does for unchanged object

    if "suggested_pub_id" in data:
        group_query.suggested_pub_id = data["suggested_pub_id"]

    try:
        db.session.commit()
        data = {**group_query.get_as_dict(), "links": {"self": f"/v1/api/groups/{group_query.id}"}}

        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="Group updated successfully",
                )
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST


@groups_routes.route("/groups/<string:group_id>", methods=["PUT"])
def put_group(group_id):
    group_query = Group.query.get_or_404(group_id)
    data = request.get_json()

    required_fields = ["suggested_pub_id"]
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

    group_query.suggested_pub_id = data["suggested_pub_id"]

    try:
        db.session.commit()
        data = {**group_query.get_as_dict(), "links": {"self": f"/v1/api/groups/{group_query.id}"}}
        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="Group updated successfully",
                )
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST


@groups_routes.route("/groups/<string:group_id>/users", methods=["GET"])
def get_group_users(group_id):
    # Verify group exists
    group = Group.query.get_or_404(group_id)

    # Get users through relationship
    users_query = User.query.join(UserGroupQuery).filter(UserGroupQuery.group_id == group_id)

    # Paginate users
    paginated_users, meta, links = paginate_query(users_query, request.args, f"/v1/api/groups/{group_id}/users")

    return (
        jsonify(
            create_success_response(
                data=group.get_as_dict(),
                meta=meta,
                links=links,
                message=f"Group {group_id} with users fetched successfully",
                included=paginated_users,
            )
        ),
        HTTPStatus.OK,
    )
