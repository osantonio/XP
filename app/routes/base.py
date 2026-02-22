from quart import Blueprint, render_template

base_bp = Blueprint("base", __name__)


@base_bp.route("/")
async def index():
    return await render_template("index.html")

