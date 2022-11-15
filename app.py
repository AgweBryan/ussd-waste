
import logging 
from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



# logging.basicConfig(filename='record.log', level=logging.DEBUG)
app = Flask(__name__)

# Secret key
app.config['Secret_key'] = 'my long secret key'


# db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/health_waste'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ihdvpjwyzvkpqs:1ce0475bfe3c0ed9a9b3f8d18c43453f4e6dded42ec39190e4b265f79b9d00a4@ec2-52-4-104-184.compute-1.amazonaws.com:5432/db0fv80slqe443'
#secret key
app.config['Secret_key'] = "my long secret key veryy"
#initialize db
db = SQLAlchemy(app)
#model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(200), unique=True, nullable=True)
    pin = db.Column(db.String(200), nullable=True)
    userType = db.Column(db.String(200), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, name=None, phone=None, date_added=None, userType=None, pin=None):
        self.name = name
        self.phone = phone
        self.date_added = date_added
        self.pin = pin
        self.userType = userType

    def __repr__(self):
        return f'<User {self.name!r}>'
    # create a string
    # def __repr__(self):
    #     return '<User %r>' % self


'''
# class User:
  

#     def __init__(self, id, name, pin, phone_number, userType) -> None:
#         self.id = id
#         self.pin  = pin
#         self.name = name
#         self.phone_number = phone_number
#         self.userType = userType


#     def toTuple(self):
#         userCred = []
#         userCred.append(self.id)
#         userCred.append(self.name)
#         userCred.append(self.pin)
#         userCred.append(self.phone_number)
#         userCred.append(self.userType)
#         return userCred

#     def fromTuple(tuple):
#         return User(id=tuple[0], name=tuple[1], pin=tuple[2], phone_number=tuple[2], userType=tuple[2])

#     def __repr__(self):
#         return f'<User {self.name}>'


# Database functions begin 

 # Connect to db 'health_waste
def connectToDb():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="health_waste"
    )

# Insert a user in the users table
def insert_user(user):
    mydb = connectToDb()

    mycursor = mydb.cursor()

    sql = "INSERT INTO users (id, name, pin, phone_number, userType) VALUES (%s, %s, %s, %s, %s)"
    # val = ("John", "Highway 21")
    print(user.toTuple())
    mycursor.execute(sql, user.toTuple())

    mydb.commit()

    print(mycursor.lastrowid, "record inserted.")

    

# Find a user in the user table
def find_user(userId):
    mydb = connectToDb()
    mycursor = mydb.cursor()

    sql = "SELECT * FROM users WHERE id = %s"
    id = userId.split()

    mycursor.execute(sql, id)

    myresult = mycursor.fetchall() # Returns a list of users that match

    for x in myresult:
        print("The user exists: ", x)

    if len(myresult) > 0:
        return User.fromTuple(myresult[0])
    else:
        return False


# Database functions end
'''


@app.route('/')
def hellow_world():
    value1 = '1'
    value2 = '2'
    sum = int(value1) + int(value2)
    return 'first page'


@app.route('/ussd', methods = ['POST'])
def ussd():
    # Read the variables sent via POST from our API
    session_id = request.values.get('sessionId')
    service_code = request.values.get('serviceCode')
    phone_number = request.args.get('phoneNumber')
    text = request.args.get('text') # The first begins with CON and the last with END
    # fetch user
    user = User.query.filter_by(phone=phone_number).first()

    print(user)
    print(phone_number)

    x = text.split('*')
    y = len(x)

    print('The Value of x: ', x)


    if user:
        if text == '' or x[y-1] == '99':
            # Main menu
            response = 'CON Welcome back ' + user.name + '! How can we assist you\n\n'
            response += '1. Request pickup\n'
            response += '2. Record transaction\n'
            response += '3. Check SOSOCASH balance\n'
            response += '4. Withdraw funds\n'
            response += '5. Submit insurance claim\n'
            response += '6. Change PIN\n'
         

        elif text == '1':
            # User selected request pickup
            response = 'Enter Area'

        elif y == 2 and x[0] == '1':
            response = 'Enter waste type'
        
        elif y == 3 and x[0] == '1':
            response = 'Enter Approximate quantity in kgs'
        elif y == 4 and x[0] == '1':
            response = 'Thank you. We are processing your request\n\n'
            response += '99. Main menu'
               
    else:
        if text == '':
            response = 'CON Welcome to SOSOCARE\n\n'
            response += '1. Register\n'
            response += '2. Terms and Conditions'
        elif text == '1':
            # if user does not exist, register user
            response = 'CON Register on SOSOCARE.\n Select user type\n\n'
            response += '1. Waste Collector\n'
            response += '2. Waste Collection agent\n'
            response += '3. Organization\n\n'
            response += '99. Main menu'

        elif text == '2':
            response = 'Thank you for choosing SOSOCARE insurance. Accept ECO medical plan terms and conditions Available through our whatsapp number +xxxxxxxx, agree that SOSOCARE can share your data with Medical service providers\n\n'
            response += '0. Next'

        elif text == '2*0' or (x[y-1] == '0' and x[0] == '2'):
            response = 'END And confirm you are between 18 and 65 years old. For enquiries kindly call +xxxxxxxxx\n\n'
            response += '#. Previous'

        elif text == '2*0*#' or (x[y-1] == '#' and x[0] == '2'):
            response = 'Thank you for choosing SOSOCARE insurance. Accept ECO medical plan terms and conditions Available through our whatsapp number +xxxxxxxx, agree that SOSOCARE can share your data with Medical service providers\n\n'
            response += '0. Next'
        
        # Waste collector registration starts
        elif text == '1*1':
            response = 'Enter Name & Surname'
        elif y == 3 and re.search('1\*1\*[a-zA-Z]', text):
            # text == '1*1*username'
            response = 'Enter Bank Account Number'
        elif y == 4 and len(x[y-1]) == 9 and x[1] == '1':
            # text == '1*1*username*bankAccount'
            bank_account_number = x[y-1]
            print('The user bankAccount', bank_account_number)
            response = 'Create SOSOCARE Account PIN'
        elif y == 5 and len(x[y-1]) == 4 and x[1] == '1':
            # text == '1*1*username*bankAccount*pin'
            username = x[y-3]
            userpin = x[y-1]
            current_user = User(name=username, phone=phone_number, pin=userpin, userType='waste collector')
            # add user to database
            # insert_user(current_user)
            db.session.add(current_user)
            db.session.commit()
            response = 'END Thank you. We are verifying your information\n\n'
            response += '99. Main menu'
        # Waste collector registration ends

        # Waste collector agent registration starts
        elif text == '1*2':
            response = 'Enter Name & Surname2'
        elif y == 3 and re.search('1\*2\*[a-zA-Z]', text) and x[1] == '2':
            # text == '1*1*username'
            response = 'Enter Bank Account Number'
        elif y == 4 and len(x[y-1]) == 9 and x[1] == '2':
            # text == '1*1*username*bankAccount'
            response = 'Create SOSOCARE Account PIN'
        elif y == 5 and len(x[y-1]) == 4 and x[1] == '2':
            # text == '1*1*username*bankAccount*pin'
            username = x[y-3]
            userpin = x[y-1]
            current_user = User(name=username, phone=phone_number, pin=userpin, userType='waste collector agent')
            # add user to database
            # insert_user(current_user)
            db.session.add(current_user)
            db.session.commit()
            response = 'END Thank you. We are verifying your information\n\n'
            response += '99. Main menu'

        # Waste collector agent registration ends

        # Organization registration starts

        elif text == '1*3':
            response = 'Enter Organization name'
        elif y == 3 and re.search('1\*3\*[a-zA-Z]', text) and x[1] == '3':
            # text == '1*1*organizationName'
            response = 'Enter address'
        elif y == 4 and x[1] == '3':
            # text == '1*1*organizationName*address'
            response = 'Create SOSOCARE Account PIN'
        elif y == 5 and len(x[y-1]) == 4 and x[1] == '3':
            # text == '1*1*organizationname*address*pin'
            username = x[y-3]
            userpin = x[y-1]
            current_user = User(name=username, phone=phone_number, pin=userpin, userType='Organization')
            # add user to database
            # insert_user(current_user)
            db.session.add(current_user)
            db.session.commit()
            response = 'END Thank you. We are verifying your information\n\n'
            response += '99. Main menu'    

        # Organization registration ends



    return response
    # return 'ussd path'
    




if __name__ == '__main__':
    app.run(debug=True)