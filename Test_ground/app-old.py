import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#setup engine for postgres dialect+driver://username:password@host:port/database
connection_string ='postgres://yonxayzwttwqcf:7b11f9fcfe67b6ad7f2ca38fa2a5cf7e521e5757f44fdd3bd90b9f386e696a2e@ec2-54-85-13-135.compute-1.amazonaws.com:5432/dbne19n4g8dtss'
engine = create_engine(f'{connection_string}')


#reflect using automap base
Base = automap_base()
#table reflect
Base.prepare(engine, reflect=True)
Base.classes.keys()

#reference the tables in heroku
Author_info = Base.classes.author
Tags = Base.classes.tags
Quotes = Base.classes.quotes


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
   
    session = Session(engine)
    #  = session.query(quotes).count()
    # quotes = session.query(quotes.quote_text)
       
    # session.close()
    # return jsonify(quotes=quotes)

#   { total: <total number quotes scraped >,
#     quotes : [{ text: <quote text >,
#                 author name: <author name >,
#                 tags: []},
# 	            ...]}
#stealing codes
  # get total number of quotes scrapped
    # get quote information (text, author name, and tags)
    sel=[Quotes.author_name, Quotes.quote_text, Tags.tag]
    
    quote_info = session.query(*sel).\
            filter(Quotes.id == Tags.quote_id).all()     

    session.close()


        # text, name, and tags (qry) --> [{Text:text}, {Name:name}, {Tags:tags}]
    quote_list=[]
    for name, text, tags in quote_info:
        info_dict = {}
        info_dict["Text"] = text
        info_dict["Author"] = name
        info_dict["Tags"] = tags
        quote_list.append(info_dict)

    quotes_libr = {"total":len(quote_list), "quote":quote_list}


        # Return the JSON representation of your dictionary.
    return (quotes_libr) 

    # return  'you found us'
    


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