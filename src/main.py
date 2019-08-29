import os
import responder

from __init__ import __version__

api = responder.API(
    title="knock-down-with-jeers",
    debug=True,
    cors=True,
    cors_params={
        "allow_origins": ["*"],
        "allow_methods": ["GET", "POST"],
        "allow_headers": ["*"],
    },
    version=__version__,
    static_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
    openapi="3.0.2",
    docs_route="/docs",
    openapi_route="/schema.yml",
    description="This is a game that can fight the your jeers. Words are weapons! !",
    contact={
        "name": "tubone24",
        "url": "https://tubone-project24.xyz",
        "email": "tubo.yyyuuu@gmail.com",
    },
    license={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)


@api.route("/")
def hello_html(req, resp):
    resp.html = api.template("index.html", name="aaa", jeer="bbb", streak=14, total=100)


if __name__ == "__main__":
    api.run()
