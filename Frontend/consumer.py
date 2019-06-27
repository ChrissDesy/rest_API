import requests as rq
from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return redirect('/viewclients')

@app.route('/viewclients')
def list_clients():

    try:
        clients = rq.get('http://localhost:1234/clients')

        return render_template('clients.html', data=clients.json())

    except:
        return 'Connection To The API Failed. Status 404.', 404

@app.route('/new')
def add_new():
    return render_template('form.html')

@app.route('/save', methods = ['GET', 'POST'])
def save_client():
    details = {
        'fname' : request.form['fname'],
        'sname' : request.form['sname'],
        'idnum' : request.form['idnum'],
        'gender' : request.form['gender'],
        'dob' : request.form['dob'],
        'tel' : request.form['tel']
    }

    status = rq.post('http://localhost:1234/add', data=details)

    flash(str(status.json()))

    return redirect('/viewclients')

if __name__ == "__main__":
    app.run(debug=True, port=5678)