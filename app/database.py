#!/usr/bin/python3
""" Database class """
import mysql.connector


class db:
    """
    The `db` class is responsible for managing the connection to the MySQL database and executing queries.
    Methods:
    --------
    - __init__(self, user, host, password, database): Initializes the database connection.
    - user(self, username, api): Fetches user information based on the provided username and API key.
    """
    def __init__(self, user, host, password, database):
        """
        Initializes the database connection.
        Parameters:
        -----------
        - user (str): The username for the database.
        - host (str): The host address of the database.
        - password (str): The password for the database.
        - database (str): The name of the database.
        Exceptions:
        -----------
        - Prints an error message if the connection fails.
        """
        try:
            self.db = mysql.connector.connect(user=user, host=host, password=password, database=database,  auth_plugin='mysql_native_password')
            self.cursor = self.db.cursor()
            print ('[result] Database connected!')
            
        except Exception as e:
            print ('[error] error connecting database!')
            print(e)

    def user(self, username, api):
        """
        Fetches user information based on the provided username and API key.
        Parameters:
        -----------
        - username (str): The username to search for.
        - api (str): The API key associated with the user.
        Returns:
        --------
        - Executes a query to fetch user details from the database.
        Exceptions:
        -----------
        - Prints an error message if the query execution fails.
        """
        try:
            query = "select * from users where username='{}' and api_key='{}'".format(username, api)
            self.cursor.execute(query)
            output = self.cursor.fetchall()
            return output[0]
        except Exception as e:
            print('[error] ' + e)

    def get_apikeys(self):
        """
        Retrieves all API keys from the users table.

        Returns:
        --------
        - list: A list of all API keys stored in the database.

        Exceptions:
        -----------
        - Raises an exception if the query execution fails.
        """
        query = 'select api_key from users'
        self.cursor.execute(query)
        output = self.cursor.fetchall()
        dummy = []
        for api in output:
            dummy.append(api[0])
        return dummy

    def add_user(self, username, password, first_name, last_name, email, phone_number, api_key):
        """
        Adds a new user to the database with the provided details.

        Parameters:
        -----------
        - username (str): The username of the user.
        - password (str): The password of the user.
        - first_name (str): The first name of the user.
        - last_name (str): The last name of the user.
        - email (str): The email address of the user.
        - phone_number (str): The phone number of the user.
        - api_key (str): The API key to associate with the user.

        Returns:
        --------
        - str: "success" if the user is added successfully.

        Exceptions:
        -----------
        - Prints an error message if the query execution fails.
        """
        try:
            query = "insert into users (username, password, first_name, last_name, email, phone_number, last_login, api_key) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', now(), '{6}');".format(username, password, first_name, last_name, email, phone_number, api_key)
            # print(query)
            self.cursor.execute(query)
            self.db.commit()
            return "success"
        except Exception as e:
            print( e)
    
    def update_values(self, apikey, fieldname, deviceID, temp, humidity, moisture, light):
        """
        Updates sensor values in the database for a specific device, and logs the data.

        Parameters:
        -----------
        - apikey (str): The API key of the user making the request.
        - fieldname (str): The database table name to insert the values.
        - deviceID (str): The unique identifier of the device.
        - temp (float): The temperature value to be updated.
        - humidity (float): The humidity value to be updated.
        - moisture (float): The soil moisture value to be updated.
        - light (float): The light intensity value to be updated.

        Returns:
        --------
        - bool: True if the update was successful, otherwise False.

        Exceptions:
        -----------
        - Prints an error message if the query execution fails.
        """
        try:
            self.cursor.execute("select api_key from users;")
            output = self.cursor.fetchall()
            dummy = []
            for i in output:
                dummy.append(i[0])
            if apikey in dummy:
                
                query = 'insert into {0} (deviceID, temperature, humidity, moisture, light, date_time) values("{1}", {2}, {3}, {4}, {5}, now());'.format(fieldname, deviceID, temp, humidity, moisture, light)
                self.cursor.execute(query)
                self.db.commit()

                query = 'update Node set temperature={0}, humidity={1}, moisture = {2}, light={3} where deviceID="{4}";'.format(temp, humidity, moisture, light, deviceID)
                self.cursor.execute(query)
                self.db.commit()

                return True

            else:
                print("not available")

        except Exception as e:
            print("[ERROR!]")
            print(e)
