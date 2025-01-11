from flask import Flask
from flask import render_template
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
    return "printable"
if __name__ == '__main__':
    app.run(debug=False)