import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

connection_string ='postgres://yonxayzwttwqcf:7b11f9fcfe67b6ad7f2ca38fa2a5cf7e521e5757f44fdd3bd90b9f386e696a2e@ec2-54-85-13-135.compute-1.amazonaws.com:5432/dbne19n4g8dtss'
engine = create_engine(f'{connection_string}')

#reflect using automap base
# Base = automap_base()
# #table reflect
# Base.prepare(engine, reflect=True)
# Base.classes.keys()

# #reference the tables in heroku
# Author_info = Base.classes.author
# Tags = Base.classes.tags
# Quotes = Base.classes.quotes


#setup flask app
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Quotes Scraper App<br/>"
        f"The List of Available Routes Are:<br/>"
        f"/quotes<br/>"
        f"/authors<br/>"
        f"/authors/author_name<br/>"
        f"/tags<br/>"
        f"/tags/<tag><br/>"
        f"/top10tags<br/>"
    )




@app.route("/quotes")
def quotes():
    result = {}
    result_set = engine.execute('''select id, author_name, quote_text
    from quotes q inner join author a on q.author_name = a.name
    order by id''')
    total_quotes = result_set.rowcount
    quotes = []
    for row in result_set:
        quote = {}
        quote['text'] = row.quote_text
        quote['author'] = row.author_name
        tags = []
        tags_result = engine.execute(
            f'select tag  from tags where quote_id= {row.id}')
        for tagrow in tags_result:
            tags.append(tagrow.tag)
        quote['tags'] = tags
        quotes.append(quote)
    result['quotes'] = quotes
    result['total'] = total_quotes
    return jsonify(result)


if __name__ == '__main__':
    app.run()