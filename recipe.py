from flask import Flask, send_file
from flask import render_template
from flask import request, make_response
import scraper
import json
from xhtml2pdf import pisa
import requests
from io import BytesIO
import os


app=Flask(__name__, static_folder="static")

def convert_url_to_pdf(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch URL: {url}")
        return False
    
    html_content = response.text
    result = open('test.pdf', "w+b")
    pdf = pisa.pisaDocument(BytesIO(html_content.encode('utf-8')), dest=result)
    return pdf

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/printable', methods=['GET'])
def printable():
    jsdata = {}
    try:
        urlp = request.args.get('textInput')
        hpdf = request.args.get('hpdf')
        js = scraper.scrape(urlp)
        template = 'printable.html'
        if hpdf:
            template = 'hpdf.html'
    except Exception as e:
        print("error: ",e )
    return render_template(template, data=js)

@app.route('/pdf', methods=['GET'])
def get_pdf():
    urlp = request.args.get('rurl')
    print(urlp)
    try:
        os.remove('test.pdf')
    except FileNotFoundError:
        print("test.pdf not found")
    convert_url_to_pdf(urlp[:-1]+"&hpdf=true")
    return send_file('test.pdf', mimetype='application/pdf',as_attachment=True, download_name='example.pdf')


if __name__ == '__main__':
    #app.run(host= '0.0.0.0')
    app.run(host='127.0.0.1',port=4455,debug=True)
