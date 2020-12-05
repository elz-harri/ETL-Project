import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.engine.result import ResultMetaData, RowProxy
from sqlalchemy.engine.interfaces import Dialect, ExecutionContext
from sqlalchemy.sql import ClauseElement
from sqlalchemy.types import TypeEngine
from flask import Flask, jsonify

connection_string ='postgres://yonxayzwttwqcf:7b11f9fcfe67b6ad7f2ca38fa2a5cf7e521e5757f44fdd3bd90b9f386e696a2e@ec2-54-85-13-135.compute-1.amazonaws.com:5432/dbne19n4g8dtss'
engine = create_engine(f'{connection_string}')

<<<<<<< HEAD:app-sjl.py

# #reflect using automap base
# Base = automap_base()
# #table reflect
# Base.prepare(engine, reflect=True)

# #reference the tables in heroku
# author = Base.classes.author
# # tag = Base.classes.tags
# quotes = Base.classes.quotes
=======
#reflect using automap base
# Base = automap_base()
# #table reflect
# Base.prepare(engine, reflect=True)
# Base.classes.keys()

# #reference the tables in heroku
# Author_info = Base.classes.author
# Tags = Base.classes.tags
# Quotes = Base.classes.quotes
>>>>>>> 36598f9ff6b15a4cf42cfeef81987757c91709ed:app.py


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


<<<<<<< HEAD:app-sjl.py
@app.route("/quotes")
def quotes():
    result = {}
    result_set = engine.execute('''select id, author_name, text
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

#   { total: <total number quotes scraped >,
#     quotes : [{ text: <quote text >,
#                 author name: <author name >,
#                 tags: []},
# 	            ...]}
    return  'you found us'
    


@app.route("/authors")
def authors():
#     {total: <total number of authors>,
#      details:[{ name : <author name >,
#             	  description : <author description>,
#             	  born : <date of birth etc. >,
#             	  count : <total number of quotes by this author >,
#             	  quotes : [{ text: <quote text>,
#                     		  tags: []}, 
#                 ...]
#             	},
#      	...]
#      }

    return


@app.route("/<author_name>")
def authorsname(author_name):
#     {name: <Author name>,
#      description: <author description>,
#      born: <date of birth etc>
#      number_of_quotes :  <total quotes by the author>
#      quotes : [{ text: <quote text>,
#     			   tags: []},
#                ...]
#      }
    return


@app.route("/tags")
def tags():
#     { count: <total tags>,
# 	    details:[{ name: < tag>,
#         		   number_of_quotes :  <total quotes this tag appears in >,
#         		   quotes : [{ text: <quote text>, tags: []}, ... ]},
#                  ...]
#      }
    return


@app.route("/<tag>")
def tag(tag):
#     { tag : <tag name>,
# 	    count : <number of quotes this tag appears in >,
# 	    quotes : [{ quote : <quote text >, tags : []}, ...	]
#      }
    return


@app.route("/top10tags")
def top10tags():
#		{ tag: <tag name> ,
#		quote count: < number of quotes this tag appears in >
#		},
#		...
=======

>>>>>>> 36598f9ff6b15a4cf42cfeef81987757c91709ed:app.py

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