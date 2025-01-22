#!/usr/bin/python3
""" User class """
import hashlib, os
from passlib.hash import sha512_crypt as sha
from datetime import datetime
from dotenv import load_dotenv
from .database import db

# Load environment variables
load_dotenv("./.env")
class user:
    """
    Represents a user in the system, managing authentication, user details, and associated devices.

    Attributes:
    -----------
    - db (db): Database connection object.
    - username (str): The username of the user.
    - secret (str): The password of the user.
    - authenticated (bool): Indicates whether the user is authenticated.
    - first (str): The user's first name (set after authentication).
    - last (str): The user's last name (set after authentication).
    - email (str): The user's email address (set after authentication).
    - phone (str): The user's phone number (set after authentication).
    - last_login (str): The user's last login timestamp (set after authentication).
    - api (str): The user's API key (set after authentication).
    - device_list (list): List of devices associated with the user (set after authentication).
    """
    def __init__(self, username, password):
        """
        Initializes a new user instance and attempts to authenticate the user.

        Parameters:
        -----------
        - username (str): The username of the user.
        - password (str): The password of the user.

        Side Effects:
        -------------
        - Authenticates the user and fetches user details and associated devices.
        """
        self.db = db('ibrahim', 'localhost', 'Django@2024', 'django')
        self.username = username 
        self.secret = password
        self.authenticated = False
        self.auth()
        self.get_details()
        self.get_devices()

    def auth (self):
        """
        Authenticates the user by verifying the provided password.

        Returns:
        --------
        - bool: True if authentication succeeds, otherwise False.

        Side Effects:
        -------------
        - Updates the user's last login time if authentication is successful.

        Exceptions:
        -----------
        - Prints an error message if the query execution fails.
        """
        try:
            query = 'select password from users where username = "{0}"'.format(self.username)
            print(query)
            self.db.cursor.execute(query)
            output = self.db.cursor.fetchall()
            print(output[0][0])
            if sha.verify(self.secret, output[0][0]):
                self.authenticated = True
                
                query = 'update users set last_login = now() where username = "{0}";'.format(self.username)
                self.db.cursor.execute(query)
                self.db.db.commit()

                return True
            else:
                self.authenticated = False
                return False

        except Exception as e:
            print("[ERROR!]")
            print(e)

    def get_details (self):
        """
        Fetches and stores the user's details if authenticated.

        Returns:
        --------
        - bool: True if details are successfully fetched, otherwise False.

        Exceptions:
        -----------
        - Prints an error message if the query execution fails.
        """
        try:
            if self.authenticated:
                query = 'select * from users where username = "{0}"'.format(self.username)
                self.db.cursor.execute(query)
                output = self.db.cursor.fetchall()
                output = output[0]
                self.first = output[2]
                self.last = output[3]
                self.email = output[4]
                self.phone = output[5]
                self.last_login = output[6].strftime("%d-%b-%Y (%H:%M:%S.%f)")
                self.api = output[7]
                return True

            else:
                print("User not logged in!")
                return False

        except Exception as e:
            print("ERROR!")
            print(e)
    
    def get_devices(self):
        """
        Fetches and stores the list of devices associated with the user if authenticated.

        Returns:
        --------
        - list: A list of device IDs associated with the user.
        - bool: False if the user is not authenticated.

        Exceptions:
        -----------
        - Prints an error message if the query execution fails.
        """
        try:
            if self.authenticated:
                query = 'select deviceID from Node where username = "{0}"'.format(self.username)
                self.db.cursor.execute(query)
                output = self.db.cursor.fetchall()
                dummy = []
                for dev in output:
                    dummy.append(dev[0])
                self.device_list = dummy
                return dummy
            else:
                return False

        except Exception as e:
            print("[Error!]")
            print (e)

    def dev_info(self, deviceID):
        """
        Fetches detailed information for a specific device.

        Parameters:
        -----------
        - deviceID (str): The unique identifier of the device.

        Returns:
        --------
        - tuple: The device details as a tuple.
        - bool: False if the user is not authenticated.

        Exceptions:
        -----------
        - Prints an error message if the query execution fails.
        """
        try:
            
            if self.authenticated:
                self.db.db.commit()
                query = 'select * from Node where deviceID="{0}";'.format(deviceID)
                self.db.cursor.execute(query)
                output = self.db.cursor.fetchall()
                print(output)
                return output[0]
            else:
                return False

        except Exception as e:
            print('[ERROR!]')
            print(e)
    
    def field_values(self, fieldname):
        """
        Fetches the latest 10 values from a specific field sorted by time.

        Parameters:
        -----------
        - fieldname (str): The name of the database table.

        Returns:
        --------
        - list: A list of the latest 10 field values.
        - bool: False if the user is not authenticated.

        Exceptions:
        -----------
        - Prints an error message if the query execution fails.
        """
        try:
            if self.authenticated:
                query = 'select * from (select * from {0} order by date_time desc limit 10) dummy order by date_time asc;'.format(fieldname)
                self.db.cursor.execute(query)
                output = self.db.cursor.fetchall()
                return output
            else:
                return False
        except Exception as e:
            print('[ERROR!]')
            print(e)

    def device_values(self, fieldname, deviceID):
        """
        Fetches the latest 10 values for a specific device from a specific field.

        Parameters:
        -----------
        - fieldname (str): The name of the database table.
        - deviceID (str): The unique identifier of the device.

        Returns:
        --------
        - list: A list of the latest 10 device-specific field values.
        - bool: False if the user is not authenticated.

        Exceptions:
        -----------
        - Prints an error message if the query execution fails.
        """
        try:
            if self.authenticated:
                query = 'select * from (select * from (select * from {0} where deviceID = "{1}") var1 order by date_time desc limit 10) dummy order by date_time asc;'.format(fieldname, deviceID)
                self.db.cursor.execute(query)
                output = self.db.cursor.fetchall()
                return output
            else:
                return False

        except Exception as e:
            print('[ERROR!]')
            print(e)
