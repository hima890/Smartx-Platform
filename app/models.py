#!/usr/bin/python3
""" Message Table Schema """
from flask import url_for
from . import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    message = db.Column(db.Text(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
