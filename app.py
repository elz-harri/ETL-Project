#import necessary modules
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
    #creating a sql query to retrieve the data
    # we will engine.execute instead of using SQLalchemy session
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

#second route 
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

    result = {}
    #creating a sql query to retrieve the data
    #result_details = engine.execute('''select name, born, birthplace, description
    #from author''')
    
    result_details = engine.execute('''select a.name, a.born, a.birtplace,a.description, count(q.author_name) from author a inner join quotes q on q.author_name = a.name
group by a.name''')
    total_authors = result_details.rowcount
    authors = []
    for row in result_details:
        author = {}
        author['name'] = row.name
        author['born'] = row.born
        author['birthplace'] = row.birthplace
        author['description'] = row.description
        #needs to be edited
        author['count'] = row.count(q.author_name)
        #WE NEED TO ADD THE AUTHOR QUOTE COUNT!!!!!!!!!!!!!!!!!!!!!!!!!!!! TO OUR AUTHOR TABLE
        #MARA PLEASE HELP
        # tags_result = engine.execute(
        #     f'select tag  from tags where quote_id= {row.id}')
        # for tagrow in tags_result:
        #     tags.append(tagrow.tag)
        # quote['tags'] = tags
        authors.append(author)
    result['total'] = total_authors    
    result['author'] = authors

    
    return jsonify(result)

#Arun provided coded for top10 tags:
@app.route("/top10tags")
def top10tags():
    result = []
    tags_result_set = engine.execute('''select tag , count(*) as total from tags
    group by tag
    order by total desc
    limit 10''')
    for row in tags_result_set:
        tag = {}
        tag['tag'] = row.tag
        tag['total'] = row.total
        result.append(tag)
    return jsonify(result)



if __name__ == '__main__':
    app.run()