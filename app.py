
import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import datetime
from flask import Response
from flask_migrate import Migrate
load_dotenv()





# logging.basicConfig(filename='record.log', level=logging.DEBUG)
app = Flask(__name__)

# Secret key
app.config['Secret_key'] = 'my long secret key'


# db
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') 
if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

print(SQLALCHEMY_DATABASE_URI)
# 'postgresql://ihdvpjwyzvkpqs:1ce0475bfe3c0ed9a9b3f8d18c43453f4e6dded42ec39190e4b265f79b9d00a4@ec2-52-4-104-184.compute-1.amazonaws.com:5432/db0fv80slqe443'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
#secret key
app.config['Secret_key'] = "my long secret key veryy"
#initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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



@app.route('/')
def hellow_world():
    value1 = '1'
    value2 = '2'
    sum = int(value1) + int(value2)
    return 'first page'


@app.route('/ussd', methods = ['POST', 'GET'])
def ussd():
    # Read the variables sent via POST from our API
    session_id   = request.values.get("sessionId", None)
    serviceCode  = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text         = request.values.get("text", "default") # The first begins with CON and the last with END
    # fetch user
    user = User.query.filter_by(phone=phone_number).first()
    print('The value of user is: ', user)
   
    x = str(text).split('*')

    y = len(x)

    response = ''

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

         

        elif y == 1 and x[0] == '1':
            print('The value of x when pickup is')
            # User selected request pickup
            response = 'CON Enter Area'

        elif y == 2 and x[0] == '1':
            response = 'CON Enter waste type'
        
        elif y == 3 and x[0] == '1':
            response = 'CON Enter Approximate quantity in kgs'
        elif y == 4 and x[0] == '1':
            response = 'CON Thank you. We are processing your request\n\n'
            response += '99. Main menu'

        elif y == 1 and x[0] == '2':
            # User selected Record transaction
            response = 'CON Enter collector ID:'
        elif y == 2 and x[0] == '2':
            response = 'CON Select waste type\n\n'
            response += '1. PET\n'
            response += '2. Rubber\n'
            response += '3. Metal\n\n'
            response += '99. Main menu'
        elif y == 3 and x[0] == '2' and x[y-1] == '1':
            response = 'CON Enter Quantity'
        elif y == 4 and x[0] == '2' and x[y-2] == '1':
            response = 'CON You\'re trading <qty> kg PET valued at Naira <pet_price*qty>\n\n' # TODO: GET QTY
            response += '1. Proceed\n\n'
            response += '99. Main menu'
        elif y == 5 and x[0] == '2' and x[y-3] == '1':
            response = 'CON Enter PIN'
        elif y == 6 and x[0] == '2':
            # Check user pin here
            current_pin = user.pin
            print('This is the user pin 2: ', current_pin)
            if x[y-1] == current_pin:
                response = 'CON Thank you. We are verifying your information\n\n'
                response += '99. Main menu'

        elif y == 3 and x[0] == '2' and x[y-1] == '2':
            response = 'CON Enter Quantity'
        elif y == 4 and x[0] == '2' and x[y-2] == '2':
            response = 'CON You\'re trading <qty> kg RUBBER valued at Naira <rubber_price*qty>\n\n' # TODO: GET QTY
        elif y == 5 and x[0] == '2' and x[y-3] == '2':
            response = 'CON Enter PIN'
        elif  y == 6 and x[0] == '2':
            # Check user pin here
            current_pin = user.pin
            print('This is the user pin 2: ', current_pin)
            if x[y-1] == current_pin:
                response = 'CON Thank you. We are verifying your information\n\n'
                response += '99. Main menu'

        elif y == 3 and x[0] == '2' and x[y-1] == '3':
            response = 'CON Enter Quantity'
        elif y == 4 and x[0] == '2' and x[y-2] == '3':
            response = 'CON You\'re trading <qty> kg METAL valued at Naira <metal_price*qty>\n\n' # TODO: GET QTY
        elif y == 5 and x[0] == '2' and x[y-3] == '3':
            response = 'CON Enter PIN'
        elif  y == 6 and x[0] == '2':
            # Check user pin here
            current_pin = user.pin
            print('This is the user pin 2: ', current_pin)
            if x[y-1] == current_pin:
                response = 'CON Thank you. We are verifying your information\n\n'
                response += '99. Main menu'

        elif y == 1 and x[0] == '3':
            # User selected check balance
            response = 'CON Enter PIN'
        elif y == 2 and x[0] == '3':
            # Check pin here
            current_pin = user.pin
            if x[y-1] == current_pin:
                response = 'CON Your SOSOCash '+user.pin+' balance is <account_balance> You\'re currently on ECO PLAN\n\n'
                response += '1. View Policy benefits\n\n'
                response += '99. Main menu'
        elif y == 3 and x[0] == '3':
            # response = 'CON Hi Nonso, You have the following benefits\n\n'
            response = 'CON Hi ' + user.name + ', You have the following benefits\n\n'
            response += '1. Hospital Admission Accommodation\n'
            response += '2. Emergency Intensive Care Treatment\n'
            response += '3. Minor Surgeries\n'
            response += '4. SCAN: MRI And CT Scan\n\n'
            response += '99. Main menu'

        elif y == 1 and x[0] == '4':
            # User selected Withdraw funds
            response = 'CON Enter Agent Code'
        elif y == 2 and x[0] == '4':
            response = 'CON Enter Amount'
        elif y == 3 and x[0] == '4':
            response = 'CON Enter PIN**'
        elif y == 4 and x[0] == '4':
            # Check user pin here
            current_pin = user.pin
            print('This is the user pin 2: ', current_pin)
            if x[y-1] == current_pin:
                response = 'CON You have withdrawn <amount> from agenet <agent_id>. Your SOSOCash balance is <account_balance>\n\n'
                response = '99. Main menu'
        
        elif y == 1 and x[0] == '5':
            # User selected Submit Claim
            response = 'CON Redeem ECO PLAN Policy\n\n'
            response += '1. Proceed\n\n'
            response += '99. Main menu'
        elif y == 2 and x[0] == '5' and x[y-1] == '1':
            response = 'CON Thank you. We are processing your request. Call 000000000 for more info.\n\n99. Main Menu'
        
        elif y == 1 and x[0] == '6':
            # User selected Change PIN
            response = 'CON Enter Current PIN'
        elif y == 2 and x[0] == '6':
            # Check pin here
            current_pin = user.pin
            if x[y-1] == current_pin:
                # After check update pin
                response = 'CON Enter New PIN'
        elif y == 3 and x[0] == '6':
            # Check new pin here
            print('This is the new pin', x[y-1])
            print('This is the old pin', user.pin)
            print('The type of the pin variable is: ', type(user.pin))
            # Update user pin here
            response = 'CON ' + user.name + ', your new pin has been recorded\n\n'
            response += '99. Main menu'


               
    else:
        # Block for user registration
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
            response = 'CON Thank you for choosing SOSOCARE insurance. Accept ECO medical plan terms and conditions Available through our whatsapp number +xxxxxxxx, agree that SOSOCARE can share your data with Medical service providers\n\n'
            response += '0. Next'

        elif text == '2*0' or (x[y-1] == '0' and x[0] == '2'):
            response = 'CON And confirm you are between 18 and 65 years old. For enquiries kindly call +xxxxxxxxx\n\n'
            response += '#. Previous'

        elif text == '2*0*#' or (x[y-1] == '#' and x[0] == '2'):
            response = 'CON Thank you for choosing SOSOCARE insurance. Accept ECO medical plan terms and conditions Available through our whatsapp number +xxxxxxxx, agree that SOSOCARE can share your data with Medical service providers\n\n'
            response += '0. Next'
        
        # Waste collector registration starts
        elif text == '1*1':
            response = 'CON Enter Name & Surname'
        elif y == 3 and re.search('1\*1\*[a-zA-Z]', text):
            # text == '1*1*username'
            response = 'CON Enter Bank Account Number'
        elif y == 4 and x[1] == '1':
            # text == '1*1*username*bankAccount'
            bank_account_number = x[y-1]
            response = 'CON Create SOSOCARE Account PIN'
        elif y == 5 and len(x[y-1]) == 4 and x[1] == '1':
            # text == '1*1*username*bankAccount*pin'
            username = x[y-3]
            userpin = x[y-1]
            current_user = User(name=username, phone=phone_number, pin=userpin, userType='waste collector')
            # add user to database
            # insert_user(current_user)
            db.session.add(current_user)
            db.session.commit()
            response = 'CON END Thank you. We are verifying your information\n\n'
            response += '99. Main menu'
        # Waste collector registration ends

        # Waste collector agent registration starts
        elif text == '1*2':
            response = 'CON Enter Name & Surname2'
        elif y == 3 and re.search('1\*2\*[a-zA-Z]', text) and x[1] == '2':
            # text == '1*1*username'
            response = 'CON Enter Bank Account Number'
        elif y == 4  and x[1] == '2':
            # text == '1*1*username*bankAccount'
            response = 'CON Create SOSOCARE Account PIN'
        elif y == 5 and len(x[y-1]) == 4 and x[1] == '2':
            # text == '1*1*username*bankAccount*pin'
            username = x[y-3]
            userpin = x[y-1]
            current_user = User(name=username, phone=phone_number, pin=userpin, userType='waste collector agent')
            # add user to database
            # insert_user(current_user)
            db.session.add(current_user)
            db.session.commit()
            response = 'CON END Thank you. We are verifying your information\n\n'
            response += '99. Main menu'

        # Waste collector agent registration ends

        # Organization registration starts

        elif text == '1*3':
            response = 'CON Enter Organization name'
        elif y == 3 and re.search('1\*3\*[a-zA-Z]', text) and x[1] == '3':
            # text == '1*1*organizationName'
            response = 'CON Enter address'
        elif y == 4 and x[1] == '3':
            # text == '1*1*organizationName*address'
            response = 'CON Create SOSOCARE Account PIN'
        elif y == 5 and len(x[y-1]) == 4 and x[1] == '3':
            # text == '1*1*organizationname*address*pin'
            username = x[y-3]
            userpin = x[y-1]
            current_user = User(name=username, phone=phone_number, pin=userpin, userType='Organization')
            # add user to database
            # insert_user(current_user)
            db.session.add(current_user)
            db.session.commit()
            response = 'CON Thank you. We are verifying your information\n\n'
            response += '99. Main menu'    

        # Organization registration ends


    return Response(response, content_type='text/plain')
    # return response
    # return 'ussd path'
    




if __name__ == '__main__':
    app.run(debug=True)