from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup
from flask import request, make_response
from urllib.request import Request, urlopen
import re
import scraper
import pdf_generator 

#create a Flask application
#the argument to Flask is the name of the application's module
#since we are running our application in a single file, leave it as __name__
app=Flask(__name__, static_folder="static")

#relative path to the root of your application
@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/printable', methods=['GET'])
def printable():
    urlp = request.args.get('textInput')
    json = scraper.scrape(urlp)
    '''pdf = pdf_generator.json_to_pdf(json)

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=recipe.pdf'
'''
    return urlp

def scrape():
    req = Request('https://addapinch.com/the-best-chocolate-cake-recipe-ever/', headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    print(html_page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)