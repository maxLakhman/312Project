from flask import Blueprint, jsonify, make_response, redirect, request, url_for, current_app
from pymongo import MongoClient
from routes.auth import user_collection
from roures.tables import table_collection
import uuid



