from flask import Flask
from flask import render_template
from flask import request, make_response
import scraper
import htmlgenerator
import json


app=Flask(__name__, static_folder="static")

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/printable', methods=['GET'])

def printable():
    json_string = ""
    try:
        urlp = request.args.get('textInput')
        js = scraper.scrape(urlp)
    except Exception as e:
        print("error: ",e )

    response = None
    try:
        html_content = htmlgenerator.generateHTML(js)
        response = make_response(html_content)
    except Exception as e:
        print("Error rendering PDF: ", e)
        
    return response


if __name__ == '__main__':
    #app.run(host= '0.0.0.0')
    app.run(host='127.0.0.1',port=4455,debug=True)
