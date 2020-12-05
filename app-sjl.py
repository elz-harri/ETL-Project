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


#setup engine for postgres dialect+driver://username:password@host:port/database
connection_string ='postgres://lohpprsybclozn:74f7430754ab578b43b5c46f7acf3dbe200492f88ba0b036850f970eac0b1f46@ec2-54-85-13-135.compute-1.amazonaws.com:5432/da547o0397662v'
engine = create_engine(f'{connection_string}')


# #reflect using automap base
# Base = automap_base()
# #table reflect
# Base.prepare(engine, reflect=True)

# #reference the tables in heroku
# author = Base.classes.author
# # tag = Base.classes.tags
# quotes = Base.classes.quotes


#setup flask app
app = Flask(__name__)


# Flask Routes and welcome text
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

    return


#run app
if __name__ == '__main__':
    app.run()