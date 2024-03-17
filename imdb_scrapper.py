import requests
from bs4 import BeautifulSoup
import logging
import json
import traceback
import sys

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log message format
    filename='info.log',  # Set the log file name
    filemode='w'  # Set the file mode (w for write, a for append)
)

class WebScrapper :

    
    def __init__(self,genre,keyword) -> None:
        self.keyword = keyword
        self.genre = genre

    
    movieDivClassName = "ipc-metadata-list-summary-item"
    titleClassName = "ipc-title__text"
    yearClassName = "sc-b0691f29-8 ilsLEX dli-title-metadata-item"
    ratingClassName = "ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"
    summaryClassName = "ipc-html-content-inner-div"


    def start_scrapping(self):
        
        url = "https://www.imdb.com/search/title/?"
        headers = {'Accept-Language': 'en-US,en;q=0.8','content-type': 'text/html','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'} # If this is not specified, the default language is Mandarin
        movieData = []
        fileName = f"{self.genre}"
         
        if self.genre :
            url += f"genres={self.genre}&"
        if self.keyword :
            url += f"keywords={self.keyword}"
            fileName += f" {self.keyword}"

        response = requests.get(url,headers=headers)
        
        if response.status_code == 200 :
        
            soup = BeautifulSoup(response.text,"lxml")
            
                
            allMovies = soup.find_all("li",class_= self.movieDivClassName)
            for movie in allMovies :
               
                data = {}
                
                title = movie.find("h3",class_= self.titleClassName)
                if title :
                    data["title"] = title.text
                
                year =  movie.find("span",class_= self.yearClassName)
                if year : 
                    data["year"] = year.text.replace("\u2013","-")
                
                rating = movie.find("span", class_= self.ratingClassName)
                if rating :
                    data["rating"] = rating.text.replace("\u00a0", " ")
                
                summary = movie.find("div",class_= self.summaryClassName)
                if summary :
                    data["summary"] = summary.text


                movieData.append(data)
            
            
            if movieData :

                with open(f"{fileName}.json","w",encoding="utf-8") as f :
                    f.write(json.dumps(movieData))

                print(f"movies are saved in {fileName}.json file")
            else :
                print("No movies found with given genre and keyword")
   
        else :
            logging.error(response.text)

    



if __name__ == "__main__":
    movieGenre = input("enter movie genre : ")
    movieKeyword = input("enter keyword to search (if any ) : ")
    
    if not movieGenre and not movieKeyword :
        print("please provide either genre or keyword")
        sys.exit()
    
    logging.info(f"movie genre : {movieGenre} , search keyword : {movieKeyword}")
    
    print("getting all movies.....")

    try :
        scrapper = WebScrapper(movieGenre,movieKeyword)
        scrapper.start_scrapping()
        
    except Exception as e :
        print("something went wrong ....")
        logging.error(traceback.format_exc())
        