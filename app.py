import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#setup engine from hawaii sqlite in resources folder
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect using automap base
Base = automap_base()
#table reflect
Base.prepare(engine, reflect=True)

#reference the two tables in Base
#Measurement = Base.classes.measurement
#Station = Base.classes.station


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