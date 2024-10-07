import psycopg2

class Postgres_database():
    def __init__(self):
        self.connection= None
        self.cursor=None

##Database Connection
    def connect_database(self):
        """Establish a connection to the PostgreSQL database."""
        # PostgreSQL connection details
        db_host = 'localhost'
        db_name = 'movie_db'
        db_user = 'postgres'
        db_password = 'hello'

        try:
            # Connect to PostgreSQL database
            self.connection = psycopg2.connect(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_password
            )
            print("Database connection established.")
            self.cursor = self.connection.cursor()
            self.create_table()
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            self.connection = None
    
    def create_table(self):
        """Create the movies table if it doesn't exist."""
        if self.connection:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS moviescraped (
                    id SERIAL PRIMARY KEY,
                    movie_name VARCHAR(255),
                    tomatometer INTEGER,
                    popcornmeter INTEGER,
                    storyline TEXT,
                    rating VARCHAR(50),
                    genres VARCHAR(255),
                    review_1 TEXT,
                    review_2 TEXT,
                    review_3 TEXT,
                    review_4 TEXT,
                    review_5 TEXT,
                    status VARCHAR(50) NOT NULL
                )
                """
            )
            self.connection.commit()
        else:
            print("No connection available to create the table.")
    

    def insert_movie_data(self, movie_name, tomatometer_score, popcornmeter_score, storyline, rating, genres, reviews, status):
        """Insert movie data into the database."""
        if self.connection:
            try:
                # Prepare the SQL statement
                insert_query = """
                INSERT INTO moviescraped (
                    movie_name,
                    tomatometer,
                    popcornmeter, 
                    storyline, 
                    rating, 
                    genres, 
                    review_1, 
                    review_2, 
                    review_3, 
                    review_4, 
                    review_5, 
                    status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                # Prepare the data to be inserted
                review_data = [reviews[i] if i < len(reviews) else None for i in range(5)]
                review_data = (movie_name, tomatometer_score, popcornmeter_score, storyline, rating, genres) + tuple(review_data) + (status,)

                # Execute the insert query
                self.cursor.execute(insert_query, review_data)
                self.connection.commit()
                print(f"Data inserted for movie: {movie_name} with status: {status}")
            except psycopg2.Error as e:
                print(f"Error inserting data for '{movie_name}': {e}")
                self.connection.rollback()

            except Exception as e:
                print(f"Unexpected error: {e}")
                self.connection.rollback()
                
        else:
            print("No database connection available.")

    def close_database(self):
        if self.connection:
            self.connection.close