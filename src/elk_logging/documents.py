from elasticsearch_dsl.connections import connections


connections.create_connection()
from .institution import *
from .person import *