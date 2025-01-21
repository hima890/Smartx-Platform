"""
routes.py

This file defines the routing logic for the Flask application. It includes endpoints
for rendering HTML templates, handling user authentication, managing API requests,
and interacting with the database. The routes cover functionalities like user login,
dashboard rendering, profile management, and various API operations.
"""

import json
import base64
import os
import binascii
from flask import Blueprint, render_template, jsonify, redirect, request
from .users import user
from .database import db
from .models import Message
from dotenv import load_dotenv
from random import choice
from datetime import datetime
from . import db as handler
from . import limiter

# Load environment variables
load_dotenv("./.env")

main = Blueprint('main', __name__)
# Login setup
logged_in = {}
api_loggers = {}

# Database connection
mydb = db(
    os.environ.get('DBUSER'),
    os.environ.get('DBHOST'),
    os.environ.get('DBPASSWORD'),
    os.environ.get('DBNAME')
)

@limiter.limit("50 per minute")
@main.route('/')
def home():
    """Render the home page."""
    return render_template('index.html', title='HOME')


@limiter.limit("50 per minute")
@main.route('/aboutus')
def about():
    """Render the 'About Us' page."""
    return render_template('aboutus.html')


@limiter.limit("50 per minute")
@main.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    POST: Authenticate the user and start a session.
    GET: Render the login page.
    """
    error = ""
    if request.method == 'POST':
        user_instance = user(request.form['username'], request.form['password'])
        if user_instance.authenticated:
            user_instance.session_id = str(binascii.b2a_hex(os.urandom(15)))
            logged_in[user_instance.username] = {"object": user_instance}
            return redirect(f'/overview/{request.form["username"]}/{user_instance.session_id}')
        else:
            error = "Invalid Username or Password"
    return render_template('Login.htm', error=error)


@limiter.limit("50 per minute")
@main.route('/device1/<string:username>/<string:session>', methods=["GET", "POST"])
def Dashoboard():
    """
    Render the dashboard for a specific device.
    The dashboard includes user and device details.
    """
    user = {
        "username": "Aman Singh",
        "image": "static/images/amanSingh.jpg"
    }

    devices = [
        {"Dashboard": "device1", "deviceID": "Device1"}
    ]
    return render_template('device_dashboard.htm', title='Dashboard', user=user, devices=devices)


@limiter.limit("50 per minute")
@main.route('/overview/<string:username>/<string:session>', methods=['GET', 'POST'])
def overview(username, session):
    """
    Render the user overview page.
    Validates session before granting access.
    """
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username": username,
            "image": "/static/images/amanSingh.jpg",
            "api": logged_in[username]["object"].api,
            "session": session
        }

        devices = [
            {"Dashboard": "device1", "deviceID": "Device1"}
        ]
        return render_template('overview.htm', title='Overview', user=user, devices=devices)
    else:
        return redirect('/login')


@limiter.limit("50 per minute")
@main.route('/apisettings/<string:username>/<string:session>', methods=['GET', 'POST'])
def apisettings(username, session):
    """
    Render the API settings page.
    Validates session before granting access.
    """
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username": username,
            "image": "/static/images/amanSingh.jpg",
            "api": logged_in[username]["object"].api,
            "session": session
        }

        devices = [
            {"Dashboard": "device1", "deviceID": "Device1"}
        ]
        return render_template('api_settings.htm', title='API-Settings', user=user, devices=devices)
    else:
        return redirect('/login')


@limiter.limit("50 per minute")
@main.route('/profile/<string:username>/<string:session>', methods=['GET', 'POST'])
def profile(username, session):
    """
    Render the user profile page.
    Validates session before granting access.
    """
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username": username,
            "image": "/static/images/amanSingh.jpg",
            "api": logged_in[username]["object"].api,
            "session": session,
            "firstname": logged_in[username]["object"].first,
            "lastname": logged_in[username]["object"].last,
            "email": logged_in[username]["object"].email,
            "phone": logged_in[username]["object"].phone,
            "lastlogin": logged_in[username]["object"].last_login,
        }

        devices = [
            {"Dashboard": "device1", "deviceID": "ARMS12012"}
        ]
        return render_template('profile.htm', title='Profile', user=user, devices=devices)
    else:
        return redirect('/login')


@limiter.limit("50 per minute")
@main.route('/logout/<string:username>/<string:session>', methods=['GET', 'POST'])
def logout(username, session):
    """
    Handle user logout.
    Terminates the user's session.
    """
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        logged_in.pop(username)
        return redirect('/')
    else:
        return redirect('/login')


@limiter.limit("50 per minute")
@main.route("/api/<string:apikey>/test", methods=["GET", "POST"])
def apitest(apikey):
    """
    Test the connection to the API server.
    Returns a simple JSON response.
    """
    return {"data": "Working fine. Connected to the API server."}



@limiter.limit("50 per minute")
@main.route("/api/<string:apikey>/listdevices", methods=['GET', 'POST'])
def listdevices(apikey):
    """
    List all devices associated with a valid API key.

    Args:
        apikey (str): The user's API key for authentication.

    Methods:
        GET, POST

    Returns:
        JSON response containing a list of devices or an error message.
    """
    global api_loggers
    global mydb
    if not(apikey in api_loggers):
        try:
            query = "select username from users where api_key = '{}'".format(apikey)
            mydb.cursor.execute(query)
            username = mydb.cursor.fetchall()
            username = username[0][0]
            apiuser = person.user(username, "dummy")
            apiuser.authenticated = True
            devices_list = apiuser.get_devices()
            api_loggers[apikey] = {"object" : apiuser}
            return jsonify(devices_list)
        except Exception as e:
            print (e)
            return jsonify({"data":"Oops Looks like api is not correct"})
    
    else:
        data = api_loggers[apikey]["object"].get_devices()
        return jsonify (data)

@limiter.limit("50 per minute")
@main.route('/api/<string:apikey>/deviceinfo/<string:deviceID>', methods=['GET', 'POST'])
def device_info(apikey, deviceID):
    """
    Retrieve information about a specific device.

    Args:
        apikey (str): The user's API key for authentication.
        deviceID (str): The unique ID of the device.

    Methods:
        GET, POST

    Returns:
        JSON response with the device's information or an error message.
    """
    global api_loggers
    global mydb
    if not(apikey in api_loggers):
        try:
            query = "select username from users where api_key = '{}'".format(apikey)
            mydb.cursor.execute(query)
            username = mydb.cursor.fetchall()
            username = username[0][0]
            apiuser = user.user(username, "dummy")
            apiuser.authenticated = True
            devices_list = apiuser.get_devices()
            api_loggers[apikey] = {"object" : apiuser}
            return jsonify(devices_list)
        except Exception as e:
            print (e)
            return jsonify({"data":"Oops Looks like api is not correct"})
    
    else:
        data = api_loggers[apikey]["object"].get_devices()
        return jsonify (data)


randlist = [i for i in range(0, 100)]

@limiter.limit("50 per minute")
@main.route('/api/<string:apikey>/fieldstat/<string:fieldname>', methods=['GET', 'POST'])
def fieldstat (apikey, fieldname):
    """
    Get statistics for a specific field across all devices.

    Args:
        apikey (str): The user's API key for authentication.
        fieldname (str): The field to retrieve statistics for.

    Methods:
        GET, POST

    Returns:
        JSON response with field statistics or an error message.
    """
    global api_loggers
    global mydb
    if not(apikey in api_loggers):
        try:
            query = "select username from users where api_key = '{}'".format(apikey)
            mydb.cursor.execute(query)
            username = mydb.cursor.fetchall()
            username = username[0][0]
            apiuser = user.user(username, "dummy")
            apiuser.authenticated = True
            data = apiuser.field_values(fieldname)
            api_loggers[apikey] = {"object" : apiuser}
            return jsonify(data)
        except Exception as e:
            print (e)
            return jsonify({"data":"Oops Looks like api is not correct"})
    
    else:
        data = api_loggers[apikey]["object"].field_values(fieldname)
        return jsonify (data)


@limiter.limit("50 per minute")
@main.route('/api/<string:apikey>/devicestat/<string:fieldname>/<string:deviceID>', methods=['GET', 'POST'])
def devicestat (apikey, fieldname, deviceID):
    """
    Get statistics for a specific field on a specific device.

    Args:
        apikey (str): The user's API key for authentication.
        fieldname (str): The field to retrieve statistics for.
        deviceID (str): The unique ID of the device.

    Methods:
        GET, POST

    Returns:
        JSON response with the device's field statistics or an error message.
    """
    global api_loggers
    global mydb
    if not(apikey in api_loggers):
        try:
            query = "select username from users where api_key = '{}'".format(apikey)
            mydb.cursor.execute(query)
            username = mydb.cursor.fetchall()
            username = username[0][0]
            apiuser = user.user(username, "dummy")
            apiuser.authenticated = True
            data = apiuser.device_values(fieldname, deviceID)
            api_loggers[apikey] = {"object" : apiuser}
            return jsonify(data)
        except Exception as e:
            print (e)
            return jsonify({"data":"Oops Looks like api is not correct"})
    
    else:
        data = api_loggers[apikey]["object"].device_values(fieldname, deviceID)
        return jsonify (data)


@limiter.limit("50 per minute")
@main.route('/api/<string:apikey>/update/<string:data>', methods=['GET','POST'])
def update_values(apikey, data):
    """
    Update values for a specific device.

    Args:
        apikey (str): The user's API key for authentication.
        data (str): Encoded data containing field name, device ID, temperature, humidity, moisture, and light values.

    Methods:
        GET, POST

    Returns:
        String indicating success or an error message.
    """
    global mydb
    try:
        data = decode(data)
        output = mydb.get_apikeys()
        if apikey in output:
            if (len(data) == 6) and (type(data) is list):
                fieldname = data[0]
                deviceID = data[1]
                temp = data[2]
                humidity = data[3]
                moisture = data[4]
                light = data[5]
                mydb.update_values(apikey, fieldname, deviceID, temp, humidity, moisture, light)
                return ("Values Updated")
            else:
                return "Data Decoding Error!"
        else:
            return "Api key invalid"

    except Exception as e:
        print (e)
        return jsonify({"data":"Oops Looks like api is not correct"})


@limiter.limit("50 per minute")
@main.route("/api/<string:apikey>/temperature", methods=["GET", "POST"])
def get_temperature(apikey):
    """
    Retrieve a random temperature value with a timestamp.

    Args:
        apikey (str): The user's API key for authentication.

    Methods:
        GET, POST

    Returns:
        JSON response with the current timestamp and a random temperature value.
    """
    randData = choice(randlist)
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    response = [time, randData]
    return jsonify(response)

@limiter.limit("50 per minute")
@main.route("/api/<string:apikey>/moisture", methods=["GET", "POST"])
def get_moisture(apikey):
    """
    Retrieve a random moisture value with a timestamp.

    Args:
        apikey (str): The user's API key for authentication.

    Methods:
        GET, POST

    Returns:
        JSON response with the current timestamp and a random moisture value.
    """
    randData = choice(randlist)
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    response = [time, randData]
    return jsonify(response)

@limiter.limit("50 per minute")
@main.route("/api/<string:apikey>/humidity", methods=["GET", "POST"])
def get_humidity(apikey):
    """
    Retrieve a random humidity value with a timestamp.

    Args:
        apikey (str): The user's API key for authentication.

    Methods:
        GET, POST

    Returns:
        JSON response with the current timestamp and a random humidity value.
    """
    randData = choice(randlist)
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    response = [time, randData]
    return jsonify(response)

@limiter.limit("50 per minute")
@main.route("/api/<string:apikey>/light", methods=["GET", "POST"])
def get_light(apikey):
    """
    Retrieve a random light intensity value with a timestamp.

    Args:
        apikey (str): The user's API key for authentication.

    Methods:
        GET, POST

    Returns:
        JSON response with the current timestamp and a random light intensity value.
    """
    randData = choice(randlist)
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    response = [time, randData]
    return jsonify(response)


def encode(data):
    """
    Encode data into a Base64 string.

    Args:
        data (dict): The data to be encoded.

    Returns:
        str: The Base64 encoded string.
    """
    data = json.dumps(data)
    message_bytes = data.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def decode(base64_message):
    """
    Decode a Base64 string into a dictionary.

    Args:
        base64_message (str): The Base64 string to decode.

    Returns:
        dict: The decoded data.
    """
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return json.loads(message)
