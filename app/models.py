#!/usr/bin/python3
"""
Module: message_schema.py
==========================

This module defines the database schema for the `Message` table in a Flask application using SQLAlchemy. 
The `Message` table is designed to store user messages along with their metadata, such as name, email, 
and the timestamp of when the message was created.

Classes:
--------
- Message: Represents the database table schema for storing user messages.

Functions:
----------
None

External Libraries:
--------------------
- flask.url_for: Provides the URL generation function for Flask (imported but not used in this module).
- SQLAlchemy (db): Manages the database connection and ORM capabilities.
- datetime.datetime: Used to handle date and time for the `created_at` column.

Database Schema:
----------------
Table Name: messages
Columns:
    - id (Integer, Primary Key): Unique identifier for each message.
    - name (String, Not Null): The name of the user who sent the message.
    - email (String, Not Null, Unique): The email address of the user.
    - message (Text, Not Null): The content of the user's message.
    - created_at (DateTime, Default=datetime.utcnow): Timestamp indicating when the message was created.

Usage:
------
This module defines the `Message` class, which can be used to interact with the `messages` table in the database. 
The class supports standard SQLAlchemy operations, such as querying, inserting, and deleting rows.
"""

from flask import url_for
from . import db
from datetime import datetime


class Message(db.Model):
    """
    A SQLAlchemy model representing the `messages` table in the database.

    Attributes:
    -----------
    id (int): 
        Unique identifier for each message. Serves as the primary key.

    name (str): 
        The name of the user who sent the message. Cannot be null.

    email (str): 
        The email address of the user. Must be unique and cannot be null.

    message (str): 
        The content of the user's message. Cannot be null.

    created_at (datetime): 
        Timestamp indicating when the message was created. Defaults to the current UTC time.
    """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
