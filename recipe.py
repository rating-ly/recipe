from flask import Flask
from flask import render_template
from flask import request, make_response
import scraper
import json


app=Flask(__name__, static_folder="static")

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/printable', methods=['GET'])
def printable():
    jsdata = {}
    try:
        urlp = request.args.get('textInput')
        js = scraper.scrape(urlp)
        print(type(js))
    except Exception as e:
        print("error: ",e )
    return render_template('printable.html', data=js)


if __name__ == '__main__':
    #app.run(host= '0.0.0.0')
    app.run(host='127.0.0.1',port=4455,debug=True)
