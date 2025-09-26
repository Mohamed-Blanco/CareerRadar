from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
import os

from selenium.webdriver.common.by import By

import time
import json
import datetime

from opp_seeker.database.database_connection import Database_connection
from opp_seeker.general_params import BASE_DIR
from opp_seeker.logger import Logger
logger = Logger().get_logger()
from bs4 import BeautifulSoup
from opp_seeker.scrappers.chromedriver_manager import Chromedriver_Manager
from opp_seeker.database.data_handler import Data_handler
import re
from opp_seeker.logger import Logger
logger = Logger().get_logger()

class Job_Collector:

    def __init__(self,database_connetion:Database_connection):
        self.db = database_connetion
        self.batch_size = 2
        self.data_handler = Data_handler(self.db)
        self.max_requests = 20


    def extract_job_title(self,list_soup):
        # Getting title
        title = list_soup.find("h2", class_="top-card-layout__title")
        if title:
            title_text = title.get_text(strip=True)
            logger.debug("title :" + title_text)
            return title_text
        else:
            logger.error("entreprise not found")
            return None


    def extract_entreprise(self,list_soup):
        # Getting entreprise
        entreprise = list_soup.find("a", class_="topcard__org-name-link")

        if entreprise:
            entreprise_text = entreprise.get_text(strip=True)
            logger.debug("entreprise :" + entreprise_text)
            return  entreprise_text
        else:
            logger.error("entreprise not found")
            return None


    def extract_location(self,list_soup):
        # Getting Location
        location = list_soup.find("span", class_="topcard__flavor topcard__flavor--bullet")

        if location:
            location_text = location.get_text(strip=True)
            logger.debug("Location:" + location_text)
            return location_text
        else:
            logger.error("Location not found")
            return None

    def extract_job_logo_url(self,list_soup):
        img_url = list_soup.find("img", class_="artdeco-entity-image")

        if img_url:
            url = img_url.get("data-delayed-url")
            logger.debug("Url Image:" +  url)
            return  url
        else:
            logger.error("Image tag not found")
            return None

    def extract_applicants_number(self,list_soup):
        # Number of candidates applied for this job
        nomberofapplicants = list_soup.find("span", class_="num-applicants__caption")

        print(nomberofapplicants)

        if nomberofapplicants:
            nomberofapplicants_text = nomberofapplicants.get_text(strip=True)
            match = re.search(r'\d+', nomberofapplicants_text)
            number = match.group()
            logger.debug(f"nomberofapplicants:{number}")
            return number
        else:
            return None

    def extract_posted_date(self, list_soup):
        current_date = datetime.datetime.now()
        formatted_date = None

        time_posted = list_soup.find("span", class_="posted-time-ago__text")
        time_posted_text = time_posted.get_text(strip=True)
        time_posted_text = time_posted_text.lower().replace("'", " ").strip()
        logger.debug(f"Date plain text {time_posted_text}")
        # Clean and normalize the text
        time_posted_text = time_posted_text.lower().replace("'", " ").strip()

        # Extract number using regex
        match = re.search(r'\d+', time_posted_text)
        if not match:
            logger.error("Could not extract number from time text")
            return None

        timefrom = int(match.group())

        # Check for different time units
        if any(word in time_posted_text for word in ['day', 'days', 'jours', 'jour']):
            new_date = current_date - datetime.timedelta(days=timefrom)
            formatted_date = new_date.strftime("%d/%m/%Y")
        elif any(word in time_posted_text for word in ['week', 'weeks', 'semaines', 'semaine']):
            new_date = current_date - datetime.timedelta(weeks=timefrom)
            formatted_date = new_date.strftime("%d/%m/%Y")
        elif any(word in time_posted_text for word in ['month', 'months', 'mois']):
            new_date = current_date - datetime.timedelta(days=30 * timefrom)
            formatted_date = new_date.strftime("%d/%m/%Y")
        else:
            logger.info("No recognized time unit found in: " + time_posted_text)
            return None

        # Log the results.json
        logger.debug("Time Posted: " + formatted_date)

        return formatted_date


    def extract_test(self,text):
        current_date = datetime.datetime.now()
        formatted_date = None

        time_posted_text = text
        print("tffooo", time_posted_text)

        # Clean and normalize the text
        time_posted_text = time_posted_text.lower().replace("'", " ").strip()

        # Extract number using regex
        match = re.search(r'\d+', time_posted_text)
        if not match:
            logger.error("Could not extract number from time text")
            return None

        timefrom = int(match.group())

        # Check for different time units
        if any(word in time_posted_text for word in ['day', 'days', 'jours', 'jour']):
            new_date = current_date - datetime.timedelta(days=timefrom)
            formatted_date = new_date.strftime("%d/%m/%Y")
        elif any(word in time_posted_text for word in ['week', 'weeks', 'semaines', 'semaine']):
            new_date = current_date - datetime.timedelta(weeks=timefrom)
            formatted_date = new_date.strftime("%d/%m/%Y")
        else:
            logger.info("No recognized time unit found in: " + time_posted_text)
            return None

        # Log the results.json
        logger.debug("Time Posted: " + formatted_date)

        return formatted_date

    def extract_job_description(self,list_soup):
        try:
            job_description = list_soup.find("div", class_="show-more-less-html__markup")
            job_description_text = job_description.get_text(
                strip=True) if job_description else "Job description not found"
            return job_description_text
        except :
            return None
    def extract_job_link(self,job_id):
        return f"https://www.linkedin.com/jobs/view/{job_id[0]}/?alternateChannel=search&refId=AFYeJOMJHPAGzw3EjH59FQ%3D%3D&trackingId=FcBdDTjfIr%2FJomXXdyVFoA%3D%3D"

    def extract_jobs_data(self):

        job_ids = self.data_handler.get_job_ids()
        if len(job_ids) == 0 :
            logger.debug("There is no jobs to scrape , try running Id_extractor ")
            return

        # print(job_ids)
        jobs_batch = []
        logger.info(f"Number of jobs to extract : {len(job_ids)}")

        chrome = Chromedriver_Manager()
        driver = chrome.get_chrome_driver()
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        driver.set_script_timeout(30)

        w = 0
        for job_id in job_ids:
            w = w + 1

            job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id[0]}?refId=ktoEP6ysZSpHZMZn%2FB4EaA%3D%3D&trackingId=CttRKxcyjxBh5sFFk2ihWA%3D%3D"
            request_number = 0

            while request_number < self.max_requests:
                logger.info(f"Extracting Job {job_id} : {job_url}")
                logger.info(f"Request Number {request_number}")
                request_number = request_number + 1

                try:
                    driver.get(job_url)

                    if driver.current_url.startswith("https://www.linkedin.com/authwall"):
                        logger.error("AuthWall detected")
                        logger.error("AuthWall URL:" + driver.current_url)

                    elif driver.current_url == job_url:
                        response = requests.get(job_url)
                        try:
                            driver.find_element(By.CLASS_NAME, "top-card-layout")
                            html_source = driver.page_source
                            list_soup = BeautifulSoup(html_source, 'html.parser')

                            job_criteria_items = list_soup.find_all('li', class_='description__job-criteria-item')
                            # Extract and print job information
                            # In this code we will loop on the for classes that have the same class name , that contains [Fonctionn, emploi ....]
                            job_info = {}
                            for item in job_criteria_items:
                                key = item.find('h3', class_='description__job-criteria-subheader').text.strip()
                                value = item.find('span', class_='description__job-criteria-text').text.strip()
                                job_info[key] = value

                            try:
                                job_data = {
                                    "title": self.extract_job_title(list_soup),
                                    "entreprise": self.extract_entreprise(list_soup),
                                    "location": self.extract_location(list_soup),
                                    "nomberofapplicants": self.extract_applicants_number(list_soup),
                                    "time": self.extract_posted_date(list_soup),
                                    "description": self.extract_job_description(list_soup),
                                    "Niveau hiérarchique": job_info.get('Seniority level', ""),
                                    "Type d’emploi": job_info.get('Employment type', ""),
                                    "Fonction": job_info.get('Job function', ""),
                                    "Secteurs":job_info.get('Industries', ""),
                                    "joblink": self.extract_job_link(job_id),
                                    "found_by_keyword":job_id[1],
                                    "logo_url":self.extract_job_logo_url(list_soup),
                                }
                            except Exception as e:
                                logger.error(f"Failed to map data_warehouse {e}")

                            jobs_batch.append(job_data)

                            if len(jobs_batch) >= self.batch_size :
                                file = os.path.join(os.path.dirname(__file__), '..', 'data_warehouse', 'raw','jobs_data.json')

                                # ensure file exists
                                if not os.path.exists(file):
                                    all_records = []
                                else:
                                    with open(file, 'r', encoding='utf-8') as f:
                                        try:
                                            all_records = json.load(f)
                                        except json.JSONDecodeError:
                                            all_records = []  # empty file → start with empty list

                                all_records.extend(jobs_batch)

                            break

                        except NoSuchElementException:
                            if response.status_code == 429:
                                logger.error("Too Many Request Detected !")
                                time.sleep(10)

                            logger.error(
                                "Element with class 'top-card-layout' not found. Skipping further actions.")
                    else:
                        logger.error("Page did not load correctly.")
                except:
                    logger.error("The Scrapping Procces Was interupted Check your jobs_data.json!! ")
                    chrome.cleanup_stuck_sessions()
                    continue

        if len(jobs_batch) >= 0 :
            file = os.path.join(os.path.dirname(__file__), '..', 'data_warehouse', 'raw','jobs_data.json')
            with open(file, 'r', encoding='utf-8') as f:
                all_records = json.load(f)

            all_records.extend(jobs_batch)

            with open(file, 'w', encoding='utf-8') as f:
                json.dump(all_records, f, indent=4, ensure_ascii=False)


        logger.debug("Last Batch executed")
        file = os.path.join(BASE_DIR, 'configuration.json')

        with open(file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        config = {
            "last_date_scrapped": str(datetime.datetime.now()),
            "jobs_extracted": len(jobs_batch),
            "last_date_processed": config.get("last_date_processed"),
            "jobs_processed": config.get("jobs_processed"),
        }

        with open(file, 'w') as f:
            json.dump(config,f)

        chrome.cleanup_stuck_sessions()
        return len(all_records)


def main():
    database_connection = Database_connection()
    job_collector = Job_Collector(database_connection)
    job_collector.extract_jobs_data()

if __name__ == "__main__" :
    main()