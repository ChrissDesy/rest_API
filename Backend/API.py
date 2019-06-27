import mysql.connector as mysql
from flask import Flask, abort, make_response, jsonify, request

api = Flask(__name__)
db = mysql.connect(
    host = "your_host",
    user = "your_username",
    passwd = "your_password",
    database = "your_database_name"
)

#error 404 handle...
@api.errorhandler(404) 
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

#error 400 handle...
@api.errorhandler(400) 
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@api.route('/')
def home():
    return 'You have reached my API'

def view_clients():
    cursor = db.cursor()

    ## defining the Query
    query = "SELECT * FROM clients"

    ## getting records from the table
    cursor.execute(query)

    ## fetching all records from the 'cursor' object
    records = cursor.fetchall()

    if records == []:
        abort(404)

    res = []
    for record in records:
        rec = {
            'id' : record[0],
            'name' : record[1],
            'surname': record[2],
            'id-number': record[3],
            'gender': record[4],
            'birth-date': record[5],
            'telephone': record[6]
        }
        res.append(rec)
        
    return jsonify(res)

@api.route('/add', methods = ['GET', 'POST'])
def add_client():
    fname = request.form['fname']
    sname = request.form['sname']
    idnum = request.form['idnum']
    gender = request.form['gender']
    dob = request.form['dob']
    tel = request.form['tel']    

    cursor = db.cursor()

    #defining the Query...
    query = "INSERT INTO clients (fname, sname, id_num, gender, dob, telephone) VALUES (%s, %s, %s, %s,%s, %s)"
    
    #storing the values in a variable...
    values = (fname, sname, idnum, gender, dob, tel)

    try:
        #executing the query with values...
        cursor.execute(query, values)

        #save changes to db...
        db.commit()

        return make_response(jsonify( { 'status': 'created' } ), 201)

    except Exception as e:
        print('Failed to add client. Error: '+str(e))
        return abort(400)

#define and map routes...
api.add_url_rule('/clients', 'View_Clients', view_clients)


#start the server...
if __name__ == "__main__":
    api.run(debug=True, port=1234)