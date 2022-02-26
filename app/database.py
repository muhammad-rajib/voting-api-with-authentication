# import psycopg2
# from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


# database_url = 'postgresql://username:password@hostname:port/database-name'
database_url = (f"postgresql://"
                f"{settings.database_username}"
                f":{settings.database_password}"
                f"@{settings.database_hostname}"
                f":{settings.database_port}"
                f"/{settings.database_name}")


engine = create_engine(database_url)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# connect postgres using psycopg2 connector driver
"""
while True:
    try:
        conn = psycopg2.connect(
            host='',
            database='',
            user='',
            password='',
            cursor_factory=RealDictCursor 
        )
        cursor = conn.cursor()
        print('Database connection was succesfull!')
        break
    except Exception as error:
        print('Connecting to database failed')
        print('Error: ', error)
"""