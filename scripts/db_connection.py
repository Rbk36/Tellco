import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class db_connection:
    def __init__(self):
       # Set up the database connection parameters and initialize the engine
        self.connection_params = {
            "dbname": os.getenv("DBNAME"),
            "user": os.getenv("DBUSER"),
            "password": os.getenv("DBPASSWORD"),
            "host": os.getenv("DBHOST"),
            "port": os.getenv("DBPORT"),
        }
        try:
            self.engine = self.initialize_engine()
            print("Database connection engine created successfully.")
        except Exception as error:
            print(f"Error creating database connection engine: {error}")
            self.engine = None

    def initialize_engine(self):
        """Construct and return an SQLAlchemy engine."""
        database_uri = (
            f"postgresql+psycopg2://"
            f"{self.connection_params['user']}:{self.connection_params['password']}@"
            f"{self.connection_params['host']}:{self.connection_params['port']}/"
            f"{self.connection_params['dbname']}"
        )
        try:
            engine = create_engine(database_uri)
            return engine
        except Exception as error:
            print(f"Error creating SQLAlchemy engine: {error}")
            return None

    def get_engine(self):
        """Retrieve the SQLAlchemy engine."""
        if self.engine:
            return self.engine
        else:
            raise ConnectionError("SQLAlchemy engine is not available.")

    def fetch_all_query(self):
        """Return SQL query to retrieve all records from the xdr_data table."""
        try:
            query = "SELECT * FROM public.xdr_data;"
            return query
        except Exception as error:
            print(f"Error fetching query: {error}")
            return None

    def fetch_aggregate_query(self, aggregate_column, alias, function):
       
        try:
            query = f"""
            SELECT {aggregate_column} AS {alias}, {function}(*) 
            FROM public.xdr_data
            WHERE {aggregate_column} IS NOT NULL
            GROUP BY {aggregate_column}
            ORDER BY {function}({aggregate_column}) DESC;
            """
            return query
        except Exception as error:
            print(f"Error fetching query: {error}")
            return None