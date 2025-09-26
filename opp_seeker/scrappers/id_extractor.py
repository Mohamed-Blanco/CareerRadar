
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
import pandas as pd
from selenium.webdriver.common.by import By
import time
import json
import datetime
import re
from opp_seeker.logger import Logger
logger = Logger().get_logger()
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from opp_seeker.scrappers.chromedriver_manager import Chromedriver_Manager
from opp_seeker.scrappers.auth_manager import Auth_Manager
from opp_seeker.database.data_handler import Data_handler
from opp_seeker.database.database_connection import Database_connection
from opp_seeker.general_params import KEYWORDS_PATH

class ID_Extractor :
    def __init__(self):
        self.batch_size = 20
        database_connection = Database_connection()
        self.data_handler = Data_handler(database_connection)
        self.max_requests = 20
        pass

    def extract_job_ids_Linkdein(self , limit:int):
        chrome = Chromedriver_Manager()
        driver = chrome.get_chrome_driver()
        if driver is None:
            return

        auth_manager = Auth_Manager(driver)
        auth_manager.login_linkdein()

        keywords = self.keywords_manager()

        jobs_batch = []
        total_jobs = 0

        for key in keywords :
            logger.info("MANAGING KEYWORDS ")
            key1,key2,key3,key4 = self.sub_keys_from_keyword(key)

            # this is Login url
            compose_url = f"https://www.linkedin.com/jobs/search?keywords={key1}%20{key2}%20{key3}%20{key4}&location=Morocco&position=1&pageNum=0"

            # After we logged in we will be shown an foryou page , we need to search our jobs with specified Url
            # Sleep waiting for login procces
            time.sleep(12)

            driver.get(compose_url)
            logger.debug(f"Navigating into the jobs url wich is equal to {compose_url}")

            i = 0
            n = 0

            while i <= n:
                try :
                    driver.execute_script(
                        "document.querySelector('.scaffold-layout__list ').children[1].scrollTo({ top: 4000, behavior: 'smooth' });")
                    time.sleep(2)
                    driver.execute_script(
                        "document.querySelector('.scaffold-layout__list ').children[1].scrollTo({ top: 4000, behavior: 'smooth' });")
                    logger.info("Trying to get all ids of the Jobs appeared on our page ")
                except :
                    logger.error("Error when trying to get the Ids on the page ")
                # Here we will get all the HTML page DOM
                html_source = driver.page_source
                # parsing the HTML DOM , to make it easier when searching for classes
                list_soup = BeautifulSoup(html_source, 'html.parser')
                dt = datetime.datetime.today()
                job_ids = [(int(div.get('data-job-id')),dt,key) for div in list_soup.find_all('div', {'data-job-id': True})]

                jobs_batch.extend(job_ids)

                logger.info(f"Job Ids : {job_ids}")
                print("batch size = " , len(jobs_batch) , "ids_size = " , len(job_ids) )
                if(len(jobs_batch) >= min(self.batch_size,limit) ):
                    print("sort bulk ")
                    self.data_handler.store_bluk_ids(jobs_batch)
                    total_jobs += len(jobs_batch)
                    jobs_batch = []
                    if total_jobs >= limit:
                        logger.info(f"Total Scrapped job {total_jobs} ")
                        chrome.cleanup_stuck_sessions()
                        return

                        # Here we will increment the number , this represents the number of the next page
                i = i + 1

                try:
                    # Here we will check if the button of the next page is available , for example if we are in page 0 the number will be 1....
                    button = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="Page {i}"]')
                    logger.info(f"The pagination Button found, trying to get the page number {i} ")
                    button.click()
                    n = n + 1
                    time.sleep(6)
                except Exception as e:
                    logger.info(f"Total Scrapped job {total_jobs} ")
                    logger.error(f"Error when going into the second page {e}")


    def extract_jobs_data(self,batch_size):
        job_ids = self.data_handler.get_job_ids(batch_size)

        jobs_batch = []

        logger.info(f"Extracting...... {len(job_ids)} jobs ")

        chrome = Chromedriver_Manager()
        driver = chrome.get_chrome_driver()
        chrome = Chromedriver_Manager()
        driver = chrome.get_chrome_driver()
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        driver.set_script_timeout(30)

        auth_manager = Auth_Manager(driver)
        auth_manager.login_linkdein()

        for job_id in job_ids:

            check = False

            if not check:

                # self.addExtracted_id(job_id)
                logger.info(f"Extracting Job Number : {w} With the Id : {job_id} \n\n\n\n")
                w = w + 1

                job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}?refId=ktoEP6ysZSpHZMZn%2FB4EaA%3D%3D&trackingId=CttRKxcyjxBh5sFFk2ihWA%3D%3D"
                request_number = 0

                while request_number < self.max_requests:

                    logger.info(f"Extracting Job {job_id} : {job_url}")
                    logger.info(f"Request Number {request_number}")
                    request_number = request_number + 1
                    logger.debug("Navigating to:" + job_url)

                    try:
                        driver.get(job_url)

                        if driver.current_url.startswith("https://www.linkedin.com/authwall"):
                            logger.error("AuthWall detected")
                            logger.error("AuthWall URL:" + driver.current_url)

                        elif driver.current_url == job_url:

                            response = requests.get(job_url)

                            try:
                                driver.find_element(By.CLASS_NAME, "top-card-layout")
                                logger.info("Driver Title : " + driver.title)
                                logger.info("Current URL:" + driver.current_url)
                                logger.info("Page loaded successfully")
                                logger.info("Beginning to get Job Information:")
                                html_source = driver.page_source
                                list_soup = BeautifulSoup(html_source, 'html.parser')

                                title = list_soup.find("h2", class_="top-card-layout__title")
                                entreprise = list_soup.find("a", class_="topcard__org-name-link")
                                location = list_soup.find("span", class_="topcard__flavor topcard__flavor--bullet")
                                nomberofapplicants = list_soup.find("figcaption", class_="num-applicants__caption")
                                job_data = {}

                                if title:
                                    title_text = title.get_text(strip=True)
                                    logger.debug("title :" + title_text)
                                    job_data["title"] = title_text
                                else:
                                    logger.error("entreprise not found")
                                    job_data["title"] = None
                                if entreprise:
                                    entreprise_text = entreprise.get_text(strip=True)
                                    logger.debug("entreprise :" + entreprise_text)
                                    job_data["entreprise"] = entreprise_text
                                else:
                                    logger.error("entreprise not found")

                                if location:
                                    location_text = location.get_text(strip=True)
                                    logger.debug("Location:" + location_text)
                                    job_data["location"] = location_text
                                else:
                                    logger.error("Location not found")

                                if nomberofapplicants:

                                    nomberofapplicants_text = nomberofapplicants.get_text(strip=True)
                                    match = re.search(r'\d+', nomberofapplicants_text)
                                    number = match.group()
                                    logger.debug("nomberofapplicants:" + number)
                                    job_data["nomberofapplicants"] = number
                                else:
                                    logger.error("nomberofapplicants not found")

                                time_posted = list_soup.find("span", class_="posted-time-ago__text")
                                time_posted_text = time_posted.get_text(strip=True)
                                print("tffooo", time_posted_text)
                                current_date = datetime.now()

                                try:
                                    # Extract the number from the text
                                    match = re.search(r'\d+', time_posted_text)
                                    if match:
                                        timefrom = int(match.group())
                                    else:
                                        raise ValueError("No number found in time_posted_text")

                                    # Split the text to find the time unit
                                    convertDate = time_posted_text.split(' ')
                                    print("Converted Date = " + time_posted_text)
                                    # Calculate the new date based on the input
                                    if convertDate[-1] in ['day', 'days', 'jours', 'jour']:
                                        new_date = current_date - datetime.timedelta(days=timefrom)
                                    elif convertDate[-1] in ['week', 'weeks', 'semaines', 'semaine']:
                                        new_date = current_date - datetime.timedelta(weeks=timefrom)
                                    else:
                                        raise ValueError("Unrecognized time unit in time_posted_text")

                                    # Log the extracted time and formatted date
                                    logger.debug("Time from text: " + str(timefrom))
                                    formatted_date = new_date.strftime("%d/%m/%Y")
                                    logger.debug("Time Posted: " + formatted_date)

                                    # Store the result in job_data
                                    job_data["time"] = formatted_date

                                except Exception as e:
                                    logger.error("Problem when trying to get date: " + str(e))
                                    job_data["time"] = "Nan"

                                job_description = list_soup.find("div", class_="show-more-less-html__markup")
                                job_description_text = job_description.get_text(
                                    strip=True) if job_description else "Job description not found"
                                job_data["description"] = job_description_text
                                logger.debug("Job Description: " + job_description_text)

                                job_criteria_items = list_soup.find_all('li', class_='description__job-criteria-item')

                                # Extract and print job information
                                # In this code we will loop on the for classes that have the same class name , that contains [Fonctionn, emploi ....]
                                job_info = {}
                                for item in job_criteria_items:
                                    key = item.find('h3', class_='description__job-criteria-subheader').text.strip()
                                    value = item.find('span', class_='description__job-criteria-text').text.strip()
                                    job_info[key] = value

                                logger.debug("Niveau hiérarchique :" + job_info['Seniority level'])
                                job_data["Niveau hiérarchique"] = job_info['Seniority level']

                                logger.debug("Type d’emploi :" + job_info['Employment type'])
                                job_data["Type d’emploi"] = job_info['Employment type']

                                logger.debug("Fonction :" + job_info['Job function'])
                                job_data["Fonction"] = job_info['Job function']

                                try:
                                    logger.debug("Secteur :" + job_info['Industries'])
                                    job_data["Secteurs"] = job_info['Industries']
                                except:
                                    logger.error("Error when getting Secteurs")

                                job_data[
                                    "joblink"] = f"https://www.linkedin.com/jobs/view/{job_id}/?alternateChannel=search&refId=AFYeJOMJHPAGzw3EjH59FQ%3D%3D&trackingId=FcBdDTjfIr%2FJomXXdyVFoA%3D%3D"

                                jobs_batch.append(job_data)

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
                        logger.error("The Scrapping Procces Was interupted Check your results.json!! ")
                        job_df = pd.DataFrame(jobs_batch)
            else:
                logger.warning("Job Number Already  Extracted")

        job_df = pd.DataFrame(jobs_batch)
        logger.info(job_df)

    def turn_str_array(self,x):
        x=x.replace("'"," ")
        x = [(int(y) if y.strip() else None) for y in x[1:-1].split(',')]

        # for i in x :
        #     print(i,"\n")
        return x



    def keywords_manager(self):
        keywords_path = KEYWORDS_PATH

        with open(keywords_path, "r") as file:
            keywords_json = json.load(file)

        keywords = []

        for keyword in keywords_json["keywords"] :
            keywords.append(keyword)

        return keywords


    def sub_keys_from_keyword(self,keyword):
        keyword = keyword.strip()
        split_keywords = keyword.split(' ')

        # This code is there for exrtacting keyword , an also ha,dling empty keywords before inserting in Url
        key1 = split_keywords[0] if len(split_keywords) > 0 else ''
        key2 = split_keywords[1] if len(split_keywords) > 1 else ''
        key3 = split_keywords[2] if len(split_keywords) > 2 else ''
        key4 = split_keywords[3] if len(split_keywords) > 3 else ''

        logger.debug(f"Entred keywords : {key1} + {key2} + {key3} + {key4}  ")

        return key1,key2,key3,key4


def main():
    id = ID_Extractor()
    # test = "['4184136484', '4167114496', '4166280484', '4187404582', '4163088350', '4187291839', '4173977409', '4108130892', '4154598756', '4158534714', '4181089996', '4177275060']"
    # id.turn_str_array(test)
    id.extract_job_ids_Linkdein(5)


if __name__ == "__main__" :
    main()