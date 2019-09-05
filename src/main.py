import os
from statistics import mean
import logging
import responder
import sqlite3
from contextlib import closing
import oseti

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

dbname = 'database.db'


@api.route("/")
def hello_html(_, resp):
    champ = get_jeer_champ()
    logging.info(champ)
    resp.html = api.template("index.html", champ_name=champ[1], champ_jeer=champ[2], streak=champ[4], total=100)


@api.route("/battle")
def battle(req, resp):
    champ = get_jeer_champ()
    champ_name = champ[1]
    champ_jeer = champ[2]
    champ_score = champ[3]
    name = req.params.get("name", "")
    jeer = req.params.get("jeer", "")
    score = analyze(jeer)
    insert_jeer(name, jeer, score)
    if champ_score >= score:
        result = "チャンピオンの勝ち"
    else:
        result = "挑戦者の勝ち"
    resp.html = api.template("battle.html", name=name, jeer=jeer, score=score, champ_name=champ_name, champ_jeer=champ_jeer, champ_score=champ_score, result=result)


def analyze(jeer):
    analyzer = oseti.Analyzer()
    scores = analyzer.analyze(jeer)
    logging.info(scores)
    mean_score = mean(scores)
    return mean_score


def insert_jeer(name, jeer, score):
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        create_table = """
        CREATE TABLE IF NOT EXISTS jeers (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL, jeer VARCHAR, score INTEGER NOT NULL, streak INTEGER);
        """
        c.execute(create_table)
        sql = "INSERT INTO jeers (name, jeer, score, streak) VALUES (?,?,?,?)"
        record = (name, jeer, score, 1)
        c.execute(sql, record)
        conn.commit()


def get_jeer_champ():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        create_table = """
        CREATE TABLE IF NOT EXISTS jeers (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL, jeer VARCHAR, score INTEGER NOT NULL, streak INTEGER);
        """
        c.execute(create_table)
        conn.commit()
        sql = "SELECT * FROM jeers ORDER BY score DESC"
        c.execute(sql)
        champ = c.fetchone()
        conn.commit()
        return champ


if __name__ == "__main__":
    api.run()
