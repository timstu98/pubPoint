from flask import request
import time


def create_success_response(data=None, message=None, links=None, meta=None, included=None):
    response = {}

    response["data"] = data if data else {}
    if links:
        response["links"] = links

    # Metadata section
    response["meta"] = {**(meta if meta else {}), "timestamp": get_time()}
    if message:
        response["meta"]["message"] = message

    if included:
        response["included"] = included

    return response


def get_time():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ")


def create_error(code, detail, source=None):
    error = {"code": code, "detail": detail}
    if source:
        error["source"] = source
    return error


def create_error_response(list_of_errors):
    error_response = {"meta": {"timestamp": get_time()}}
    if len(list_of_errors) == 0:
        print("No error given to error response")
    error_response["errors"] = [error for error in list_of_errors]
    return error_response


# TODO(@TS): It is possible to request a page that does not exist. ie page 9 of users with 10 per_page when there are only 8 users
def paginate_query(query, args, url_stem):
    query_as_list = [item.get_as_dict() for item in query]
    page = int(args.get("page", 1))
    per_page = int(args.get("per_page", 10))
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page  # exclusive
    paginated_items = query_as_list[start_idx:end_idx]
    total_items = len(query_as_list)
    total_pages = (total_items + per_page - 1) // per_page

    links = {
        "self": f"{url_stem}?page={page}&per_page={per_page}",
        "first": f"{url_stem}?page=1&per_page={per_page}",
        "last": f"{url_stem}?page={total_pages}&per_page={per_page}",
    }
    if page > 1:
        links["prev"] = f"{url_stem}?page={page-1}&per_page={per_page}"
    if page < total_pages:
        links["next"] = f"{url_stem}?page={page+1}&per_page={per_page}"

    meta = {
        "pagination": {
            "totalItems": total_items,
            "totalPages": total_pages,
            "currentPage": page,
            "perPage": per_page,
        },
    }

    return paginated_items, meta, links
