from .database import Postgres_database
from .excelfile import ExcelFile
from .rottentomato import Rotten_tomato


class Movie_Scrapping:
    def __init__(self):
        self.database= Postgres_database()
        self.excel=ExcelFile()
        self.rottentomato=Rotten_tomato()
        self.movies = []

    def before_run(self):
        self.movies = self.excel.read_movie_list_from_excel()
        self.database.connect_database()
        self.database.create_table()
        self.rottentomato.open_browser()

        print("Setup done")
    
        for movie in self.movies:
            self.run_item(movie)

    def after_run(self):
        self.database.close_database()
        self.rottentomato.close()
        self.excel.close_excel()

        print("Process complete")

    def before_run_item(self):
        pass

    def run_item(self, movie_name):
        self.rottentomato.search_movie(movie_name)
        movie_url=self.rottentomato.exact_movie_details(movie_name)

        if movie_url is None:
            print(f"No exact match found for movie: {movie_name}")
            return
        
        movie_data_dict = self.rottentomato.extract_movie_details(movie_name,movie_url)
        
        if movie_data_dict is None:
            return

        reviews = movie_data_dict.get('reviews', [])  # Get the reviews list, default to an empty list if not found
        
        self.database.insert_movie_data(
                movie_name = movie_data_dict['movie_name'], 
                tomatometer_score = movie_data_dict['tomatometer_score'], 
                popcornmeter_score = movie_data_dict['popcornmeter_score'], 
                storyline = movie_data_dict['storyline'], 
                rating = movie_data_dict['rating'], 
                genres= movie_data_dict['genres'], 
                reviews = reviews[:5],
                status=movie_data_dict['status']
            )
        
        
    def after_run_item(self):
        pass