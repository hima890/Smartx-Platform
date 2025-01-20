"""
app_runner.py
=============

This script is the entry point for running the Flask application. It imports the `create_app` factory function 
from the application module and starts the Flask development server.

Functionality:
--------------
- Imports the `create_app` function to instantiate and configure the Flask application.
- Runs the Flask app on host `0.0.0.0` and port `5000` when executed directly.

Dependencies:
-------------
- `app.create_app`: The factory function responsible for creating and configuring the Flask application.

Usage:
------
To run the application, execute this script. By default, the application will listen on all available 
network interfaces (`0.0.0.0`) and port `5000`.

Example:
--------
```bash
python app_runner.py
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
