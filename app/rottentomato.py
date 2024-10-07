from RPA.Browser.Selenium import Selenium
import time
from .database import Postgres_database


class Rotten_tomato():
    def __init__(self) -> None:
        self.browser=Selenium()
        self.database=Postgres_database()

    def open_browser(self):
        self.rottentomato_url="https://www.rottentomatoes.com/"
        self.browser.open_chrome_browser(self.rottentomato_url)
        self.browser.maximize_browser_window()

    def search_movie(self,movie_name):
        url = self.rottentomato_url + f'search?search={movie_name}'
        self.browser.go_to(url)
        time.sleep(1)

    def exact_movie_details(self, movie_name):
        movie_tab_xpath="//*[@id='search-results']/nav/ul/li[2]/span"

        try:
            # Wait for the Movies tab to be visible and click it
            if self.browser.is_element_visible(movie_tab_xpath):
                self.browser.click_element(movie_tab_xpath)
                time.sleep(1)  # Wait for the movies section to load
            else:
                print(f"'Movies' tab not found for: {movie_name}")
                return
        except Exception as e:
            print(f"Error clicking on 'Movies' tab: {e}")
            return
        
        movie_results_xpath="//*[@id='search-results']/search-page-result/ul/search-page-media-row/a[2]"
        # movie_years_xpath="//*[@id='search-results']/search-page-result[1]/ul/search-page-media-row[1]//li/div[3]/span[1]"
        # movie_years=self.browser.get_webelements(movie_years_xpath)
        
        try:
            movie_results=self.browser.get_webelements(movie_results_xpath)
            exact_matches=[]

            for movie in movie_results:
                movie_title=self.browser.get_text(movie)
                if movie_name.lower() == movie_title.lower():
                    exact_matches.append(movie)



            if not exact_matches:
                print(f"No movies found: {movie_name}")
                self.database.connect_database()
                self.database.insert_movie_data(movie_name, None, None, None, None, None, [], status='NO exact match found')
                self.database.close_database()
                return

            most_recent_movie = exact_matches[0]  # For example, just select the first match

            # self.browser.wait_until_element_is_visible(movie_results)
            # self.scroll_to_load_movies()
            # Extract details from the selected movie page
            
            movie_url = most_recent_movie.get_attribute('href')
            self.browser.click_element(most_recent_movie)
            return movie_url 

        except Exception as e:
            print(f"Error during movie selection: {e}")
            return

        

    def extract_movie_details(self, movie_name,movie_url):
        tomatometer_score_xpath = "//*[@id='modules-wrap']/div[1]/media-scorecard/rt-button[2]/rt-text"
        popcornmeter_score_xpath = "//*[@id='modules-wrap']/div[1]/media-scorecard/rt-button[5]/rt-text"
        storyline_xpath = "//*[@id='modules-wrap']/div[1]/media-scorecard/div[1]/drawer-more/rt-text"
        rating_xpath = "//*[@id='modules-wrap']/div[1]/media-scorecard/rt-link[2]"
        genres_xpath = "//*[@id='main-page-content']/div/aside/section/div[1]/ul/li[2]"

      
        try:
            # Extract movie details from the page
            tomatometer_score = self.browser.get_text(tomatometer_score_xpath).replace('%', '') or None
            popcornmeter_score = self.browser.get_text(popcornmeter_score_xpath).replace('%', '') or None
            storyline = self.browser.get_text(storyline_xpath) or None
            rating = self.browser.get_text(rating_xpath) or None
            

            # Extract top 5 reviews
            reviews = self.extract_reviews(movie_url) or None
            genres = self.browser.get_text(genres_xpath)
            genres = [genre.strip() for genre in genres.split(',')] if genres else []
            genres = '/'.join(genres) if genres else None

            # Return the scraped movie data as a dictionary
            return{
                'movie_name': movie_name,
                'tomatometer_score': tomatometer_score,
                'popcornmeter_score': popcornmeter_score,
                'storyline': storyline,
                'rating': rating,
                'genres': genres,
                'reviews': reviews,
                'status': 'success'
            }

        except Exception as e:
            print(f"Error while extracting details for '{movie_name}': {e}")


    def extract_reviews(self,movie_url):
        # formatted_movie_name = movie_name.replace(' ', '_').lower()
        critics_review_xpath="//*[@id='reviews']/div/div/div[2]/p[1]"
        top_reviews = []
        try:
            # view_all_reviews_url = self.rottentomato_url + f'm/{formatted_movie_name}/reviews?type=top_critics'
            view_all_reviews_url= movie_url + '/reviews?type=top_critics'
            self.browser.go_to(view_all_reviews_url)
            time.sleep(1)

            # Find the review elements
            review_elements = self.browser.get_webelements(critics_review_xpath)

            # Extract the text of the top 5 reviews
            top_reviews = [review.text.strip() for review in review_elements[:5]]

            print("Top 5 Reviews:\n")
            for index, review in enumerate(top_reviews, 1):
                print(f"Review {index}: {review}\n")

            return top_reviews

        except Exception as e:
            print(f"Error while extracting reviews: {e}")
            return []


    def close(self):
        self.browser.close_browser()