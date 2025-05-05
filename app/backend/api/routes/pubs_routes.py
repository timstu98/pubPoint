from flask import Blueprint, request, jsonify
from models import db, Pub
from http import HTTPStatus
from .common import create_success_response, paginate_query, create_error_response, create_error
from uuid import uuid4
import os

# Relative import not necessary apparently.
API_VERSION = os.getenv("API_VERSION", "vX")
api_url_prefix = f"/api/{API_VERSION}"

pubs_routes = Blueprint("pubs_routes", __name__)


@pubs_routes.route("/pubs", methods=["GET"])
def get_pubs():
    pubs_query = Pub.query.all()
    paginated_pubs, meta, links = paginate_query(pubs_query, request.args, "{api_url_prefix}/pubs")
    return (
        jsonify(
            create_success_response(
                data=paginated_pubs,
                meta=meta,
                links=links,
                message="Pubs fetched successfully",
            )
        ),
        HTTPStatus.OK,
    )


@pubs_routes.route("/pubs/<string:pub_id>", methods=["GET"])
def get_pub(pub_id):
    pub = Pub.query.get_or_404(pub_id).get_as_dict()
    data = {**pub, "links": {"self": f"{api_url_prefix}/pubs/{pub_id}"}}
    return (
        jsonify(
            create_success_response(
                data=data,
                message="Pub fetched successfully",
            )
        ),
        HTTPStatus.OK,
    )


@pubs_routes.route("/pubs", methods=["POST"])
def create_pub():
    if not request.is_json:
        return (
            jsonify(
                create_error_response([create_error("INVALID_CONTENT_TYPE", "Content-Type must be application/json"), {"header": "Content-Type"}])
            ),
            HTTPStatus.BAD_REQUEST,
        )

    data = request.get_json()
    # If additional key-values are given, simply ignore these.
    required_fields = ["name", "address"]
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
        new_pub = Pub(id=str(uuid4().hex), name=data["name"], address=data["address"])
        db.session.add(new_pub)
        db.session.commit()
        data = {
            "id": new_pub.id,
            "type": "pub",
            "attributes": {"name": new_pub.name, "address": new_pub.address},
            "links": {"self": f"{api_url_prefix}/pubs/{new_pub.id}"},
        }
        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="Pub created successfully",
                )
            ),
            HTTPStatus.CREATED,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST


@pubs_routes.route("/pubs/<string:pub_id>", methods=["DELETE"])
def delete_pub(pub_id):
    pub = Pub.query.get(pub_id)

    if not pub:
        return (
            jsonify(create_error_response([create_error("RESOURCE_NOT_FOUND", f"Pub with id {pub_id} not found", {"pointer": "/data/id"})])),
            HTTPStatus.NOT_FOUND,
        )

    try:
        db.session.delete(pub)
        db.session.commit()
        return jsonify(create_success_response(message="Pub deleted successfull")), HTTPStatus.NO_CONTENT

    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response({create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})})), HTTPStatus.BAD_REQUEST


@pubs_routes.route("/pubs/<string:pub_id>", methods=["PATCH"])
def patch_pub(pub_id):
    pub_query = Pub.query.get_or_404(pub_id)
    data = request.get_json()

    # If no correct fields are given may still return a success -> TODO(@TS): Check what .commit() does for unchanged object

    if "name" in data:
        pub_query.name = data["name"]
    if "address" in data:
        pub_query.address = data["address"]

    try:
        db.session.commit()
        data = {**pub_query.get_as_dict(), "links": {"self": f"{api_url_prefix}/pubs/{pub_query.id}"}}

        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="Pub updated successfully",
                )
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST


@pubs_routes.route("/pubs/<string:pub_id>", methods=["PUT"])
def put_pub(pub_id):
    pub_query = Pub.query.get_or_404(pub_id)
    data = request.get_json()

    required_fields = ["name", "address"]
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

    pub_query.name = data["name"]
    pub_query.address = data["address"]

    try:
        db.session.commit()
        data = {**pub_query.get_as_dict(), "links": {"self": f"{api_url_prefix}/pubs/{pub_query.id}"}}
        return (
            jsonify(
                create_success_response(
                    data=data,
                    message="Pub updated successfully",
                )
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response([create_error("DATABASE_ERROR", str(e), {"pointer": "/data"})])), HTTPStatus.BAD_REQUEST
