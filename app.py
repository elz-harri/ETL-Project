#import necessary modules
import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import text

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
        f"/authors/&ltauthor_name&gt<br/>"
        f"/tags<br/>"
        f"/tags/<tag><br/>"
        f"/top10tags<br/>"
    )

#################################################
def tags_for_the_quote(quote_id):
    tags = []
    print(f'getting tags for {quote_id}')
    tags_result = engine.execute(
        f'select tag  from tags where quote_id= {quote_id}')
    for tagrow in tags_result:
        tags.append(tagrow.tag)
    return tags
#################################################

def quotes_for_author(author_name):
    result = []
    print(f'getting quotes for {author_name}')
    query = text("select id , quote_text from quotes where author_name ~* :name")
    quotes_result_set = engine.execute(query, {'name': author_name})
    for row in quotes_result_set:
        this_quote = {}
        this_quote['text'] = row.quote_text
        # call tags funtion
        this_quote['tags'] = tags_for_the_quote(row.id)
        result.append(this_quote)
    return result

#################################################

def quotes_for_tag(tag):
    result = []
    print(f'getting quotes for {tag}')

    query = text('''select q.id, q.quote_text
            from quotes q inner join tags t on q.id=t.quote_id
            where t.tag ~* :tag ''')
    quotes_result_set = engine.execute(query, {'tag': tag})
    for row in quotes_result_set:
        this_quote = {}
        this_quote['text'] = row.quote_text
        this_quote['tags'] = tags_for_the_quote(row.id)
        result.append(this_quote)
    return result

#################################################

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
    result_details = engine.execute('''select a.name, a.born, a.birthplace, a.description, count(q.author_name) from author a inner join quotes q on q.author_name = a.name
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
        author['count'] = row.count
        # sel = text(f"select quote_text from quotes where author_name like '%{row.name}'")
        # quote_result = engine.execute(sel).fetchall()
        # quote_result = engine.execute(f"select quote_text from quotes where author_name like '\%%{row.name}\%%'")
        query = text("select * from quotes where author_name ~* :name")
        quotes_result = engine.execute(query, {'name': row.name})
        author_quotes=[]
        for row in quotes_result:            
            author_quotes.append(row.quote_text)
            #  quote['tags'] = tags
        author['quotes'] = (author_quotes)
        authors.append(author)
    result['total'] = total_authors    
    result['author'] = authors
    
    return jsonify(result)


@app.route("/authors/<author_name>")
def oneauthor(author_name):
    result = {}
    query = text(
        "select name , born , description from author where name ~* :name")
    author_result = engine.execute(query, {'name': author_name})
    # if we found the author, return the details, otherwise return Author not found
    if(author_result.rowcount == 1):
        author = author_result.fetchone()
        result['name'] = author.name
        result['description'] = author.description
        # calll the quotes function within the loop
        quotes = quotes_for_author(author_name)
        result['quotes'] = quotes
        result['number_of_quotes'] = len(quotes)
    else:  # author not found
        result['name'] = author_name
        result['description'] = 'Author not found'

    return jsonify(result)

# get tags
@app.route("/tags")
def tags():
    result = {}
    tags_result_set = engine.execute('''select tag , count(*) as total from tags
        group by tag
        order by total desc''')
    result['count'] = tags_result_set.rowcount
    tags = []
    for row in tags_result_set:
        this_tag = {}
        this_tag['name'] = row.tag
        this_tag['number_of_quotes'] = row.total
        this_tag['quotes'] = quotes_for_tag(row.tag)
        tags.append(this_tag)
    result['details'] = tags
    return jsonify(result)

# Get user requested tag
@app.route("/tags/<tag_name>")
def onetag(tag_name):
    result = {}
    result['tag'] = tag_name
    quotes = quotes_for_tag(tag_name)
    result['quotes'] = quotes
    result['count'] = len(quotes)
    return jsonify(result)

    
#Get top10 tags:
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