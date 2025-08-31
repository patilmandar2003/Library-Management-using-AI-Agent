import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

connection = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_USER_PASSWORD"),
    database="LIBRARY_DB"
)

