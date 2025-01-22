"""
data_sender.py
===============

This module is responsible for sending encoded data to a local Flask API server at regular intervals. 
The script performs data encoding, forms a URL, sends HTTP requests, and handles server responses.

Functions:
----------
- encode(data): Converts the input data into a JSON string, encodes it using Base64, and returns the encoded message.
- decode(base64_message): Decodes a Base64 encoded message back into the original JSON data.
- main_loop(): Continuously sends encoded data to the server and handles responses.

Dependencies:
-------------
- `json`: Used to convert Python data structures into JSON format.
- `base64`: Provides Base64 encoding and decoding functions.
- `urllib.request`: Used to make HTTP requests.
- `random`: For generating random values.
- `time`: For implementing delays between API requests.

Usage:
------
The script continuously generates a list of simulated data (`mydata`), encodes it into a Base64 JSON string, 
and sends it to a local Flask API running at `http://127.0.0.1:5000/api/abhikuchnhihai/update/`. 
It prints the data, the encoded value, the URL, and the server's response. The process repeats every 2 seconds.

Example:
--------
```python
from data_sender import encode, decode

# Example of encoding data
data = ['Rosegarden', 'ARMS12012', 42, 75, 55, 90]
encoded_message = encode(data)
print(f"Encoded message: {encoded_message}")

# Example of decoding data
decoded_data = decode(encoded_message)
print(f"Decoded data: {decoded_data}")
"""
import json, base64
import urllib.request
from random import choice
import time



def encode(data):
    data = json.dumps(data)
    message_bytes = data.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def decode(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return json.loads(message)


randlist = [i for i in range(0, 100)]
devlist = ['ARMS1112','ARMS12012','ARMS22212']

while 1:
    try:
        mydata = ['Rosegarden', 'ARMS12012', choice(randlist), choice(randlist), choice(randlist), choice(randlist)]
        a = encode(mydata)
        url = 'http://127.0.0.1:5000/api/hima/update/{}'.format(a)
        response = urllib.request.urlopen(url)
        print("[data]: "+ str(mydata))
        print("[Encoded Value]: "+ a)
        print("[url]: "+ url)
        html = response.read()
        print("[output]: " + str(html))
        time.sleep(2)
    except:
        print("Website Not online")
        time.sleep(2)
