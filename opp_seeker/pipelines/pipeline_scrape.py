from opp_seeker.database.database_connection import Database_connection
from opp_seeker.logger import Logger
from opp_seeker.scrappers.id_extractor import ID_Extractor
from opp_seeker.scrappers.job_collector import Job_Collector



logger = Logger().get_logger()





class Pipline_scrapping  :
    def __init__(self):
        pass


    def execute_Linkdein_ids_collection(self,batch_size):
        logger.debug("Initializing the Id Extractor ")
        jobs_id_extractor = ID_Extractor()
        jobs_id_extractor.extract_job_ids_Linkdein(batch_size)

    def execute_Linkdein_Data_pipeline(self,batch_size):
        logger.debug("Initializing the DatabaseConnetion ")
        database_connection = Database_connection()

        logger.debug("Initializing the Job Collector")
        job_collector = Job_Collector(database_connection)
        length = job_collector.extract_jobs_data()

        logger.info(f"Pipline Executed successfully :: {length} Jobs ")


def main():
    pip = Pipline_scrapping()


if __name__ == "__main__" :
    main()