from flask import Flask, render_template, request
from flask_assistant import context_manager
import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('order-status1-firebase-adminsdk-ya6e3-7233dbf876.json')
cred1 = credentials.Certificate('order-stat-firebase-adminsdk-mds8n-0c87d6fb61.json')
cred2=credentials.Certificate('order-status-ahntui-firebase-adminsdk-kngrw-3296748b6c.json') 

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://order-status1.firebaseio.com/'
})
app1 = firebase_admin.initialize_app(cred1, {
    'databaseURL': 'https://order-stat.firebaseio.com/'
}, name='app1')
app2 = firebase_admin.initialize_app(cred2, {
    'databaseURL': 'https://order-status-ahntui.firebaseio.com'
}, name='app2')





                                                            
app = Flask(__name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Order-Status-c0ffd279137b.json'

DIALOGFLOW_PROJECT_ID = 'order-status-ahntui'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

@app.route("/")

def home():    
    return render_template("home.html") 
@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg') 
    text_to_be_analyzed = userText

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
   
    response=response.query_result.fulfillment_text
    a=0
    string= userText
    res = [int(i) for i in string.split() if i.isdigit()] 
    orderNo = ' '.join(map(str, res))
    if(len(orderNo))==5 :
        a=1
        ref = db.reference('boxes')
        ref1 = db.reference('boxes', app1)
        ref2 = db.reference('boxes', app2)
        for val in ref2.get().items():
            if(val[1]['orderId']==int(orderNo)):
                response="Product Name : "+val[1]['productName']+" <br/> "+val[1]['Status']+" "+val[1]['Location']
                
        for val in ref.get().items():
            if(val[1]['orderId']==int(orderNo)):
                response=response+" <br/>"+val[1]['Status']+" "+val[1]['Location']
                
        for val in ref1.get().items():
            if(val[1]['orderId']==int(orderNo)):
                response=response+" <br/>"+val[1]['Status']+" "+val[1]['Location']+" <br/>Delivery Date :"+val[1]['deliveryDate']
               
    
    if(len(orderNo)==0):
        response=response
    elif(len(orderNo)!=5):
        response="Please enter a valid order ID"
    
    return str(response) 
if __name__ == "__main__":    
    app.run()