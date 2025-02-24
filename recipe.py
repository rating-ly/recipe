from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup
from flask import request, make_response
from urllib.request import Request, urlopen
import re
import scraper
import pdf_generator 
import json


#create a Flask application
#the argument to Flask is the name of the application's module
#since we are running our application in a single file, leave it as __name__
app=Flask(__name__, static_folder="static")

#relative path to the root of your application
@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/printable', methods=['GET'])
'''
works for:
https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/
https://www.allrecipes.com/recipe/10402/the-best-rolled-sugar-cookies/

breaks for:
https://addapinch.com/the-best-chocolate-cake-recipe-ever/
https://www.baking-sense.com/2024/03/08/coconut-layer-cake/

'''
def printable():
    json_string = ""
    try:
        urlp = request.args.get('textInput')
        js = scraper.scrape(urlp)
        json_string = json.dumps(js)
        print(json_string)
    except Exception as e:
        print("error {e}")

    response = None
    try:
        pdf = pdf_generator.json_to_pdf(json_string)
        response = make_response(pdf.output(dest='S').encode('latin-1'))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=recipe.pdf'
    except Exception as e:
        print("Error rendering PDF {e}")
        
    return response


if __name__ == '__main__':
    app.run(host= '0.0.0.0')
    #app.run(host='127.0.0.1',port=4455,debug=True)
