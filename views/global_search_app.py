from flask import Blueprint, request, jsonify

from libs.es import ESearch

search_blue = Blueprint("search_blue", __name__)


@search_blue.route("/search/", methods=["GET"])
def search_view():
    keyword = request.args.get("keyword", "")
    search = ESearch('eduindex')
    return jsonify(search.query(keyword))
