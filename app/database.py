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
            self.db = mysql.connector.connect(user=user, host=host, password=password, database=database, auth_plugin='mysql_native_password')
            self.cursor = self.db.cursor()
            print('[result] Database connected!')
            
        except Exception as e:
            print('[error] error connecting database!')
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
        except Exception as e:
            print('[error] error executing query!')
            print(e)
