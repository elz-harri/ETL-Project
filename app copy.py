import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#setup engine for postgres dialect+driver://username:password@host:port/database
connection_string ='postgres://lohpprsybclozn:74f7430754ab578b43b5c46f7acf3dbe200492f88ba0b036850f970eac0b1f46@ec2-54-85-13-135.compute-1.amazonaws.com:5432/da547o0397662v'
engine = create_engine(f'{connection_string}')


#reflect using automap base
Base = automap_base()
#table reflect
Base.prepare(engine, reflect=True)

#reference the tables in scrape_db
author = Base.classes.author
tag = Base.classes.tags
qoutes = Base.classes.quotes


#setup flask app
app = Flask(__name__)


# Flask Routes and welcome text
@app.route("/")
def welcome():
    return (
        f"Welcome to the Quotes Scraper App<br/>"
        f"The List of Available Routes Are:<br/>"
        f"/api/v1.0/quotes<br/>"
        f"/api/v1.0/authors<br/>"
        f"/api/v1.0/authors/author_name<br/>"
        f"/api/v1.0/tags<br/>"
        f"/api/v1.0/tags/<tag><br/>"
        f"/api/v1.0/top10tags<br/>"
    )


@app.route("/api/v1.0/quotes")
def quotes():
#   { total: <total number quotes scraped >,
#     quotes : [{ text: <quote text >,
#                 author name: <author name >,
#                 tags: []},
# 	            ...]}
    print("page_here")

    return


@app.route("/api/v1.0/authors")
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


@app.route("/api/v1.0/authors/<author_name>")
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


@app.route("/api/v1.0/tags")
def tags():
#     { count: <total tags>,
# 	    details:[{ name: < tag>,
#         		   number_of_quotes :  <total quotes this tag appears in >,
#         		   quotes : [{ text: <quote text>, tags: []}, ... ]},
#                  ...]
#      }
    return


@app.route("/api/v1.0/tags/<tag>")
def tag(tag):
#     { tag : <tag name>,
# 	    count : <number of quotes this tag appears in >,
# 	    quotes : [{ quote : <quote text >, tags : []}, ...	]
#      }
    return


@app.route("/api/v1.0/top10tags")
def top10tags():
#		{ tag: <tag name> ,
#		quote count: < number of quotes this tag appears in >
#		},
#		...

    return


#run app
if __name__ == '__main__':
    app.run()