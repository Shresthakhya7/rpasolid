from .moviescraping import Movie_Scrapping

class bot:
    def __init__(self):
        self.scraping=Movie_Scrapping()

    def start(self):
        self.scraping.before_run()
        # self.scraping.run_item()

    def teardown(self):
        self.scraping.after_run()