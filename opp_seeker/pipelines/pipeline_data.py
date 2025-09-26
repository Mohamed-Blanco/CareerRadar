from opp_seeker.logger import Logger
from opp_seeker.scrappers.id_extractor import ID_Extractor
from opp_seeker.scrappers.job_collector import Job_Collector
logger = Logger().get_logger()
from opp_seeker.database.database_connection import Database_connection


class Pipline:
    def __init__(self, database_connection: Database_connection):
        self.db = database_connection

    # def execute_pipeline(self):
    #
    #     logger.critical("Initializing the data_warehouse handler ")
    #     data_handler = Data_handler(self.db)
    #
    #     logger.critical("Initializing the data_warehouse fetcher ")
    #     data_fetcher = Data_fetcher(self.db,data_handler)
    #     data_fetcher.collect_jobs_data()
    #
    #     logger.critical("Initializing the data_warehouse processor")
    #     data_processor = Data_processor(data_handler)
    #     length = data_processor.process_job_data()
    #
    #     logger.info(f"Pipline Executed successfully :: {length} Jobs ")

    def execute_pipeline(self, limit):

        logger.critical("Preparing the DATABASE ")
        database = Database_connection()


        logger.critical("Initializing the Id Extractor ")
        jobs_id_extractor = ID_Extractor()
        logger.critical("Starting To Extract Job ids from Linkdein ")
        jobs_id_extractor.extract_job_ids_Linkdein(limit)
        

        logger.critical("Initializing the Data Collector ")
        job_collector = Job_Collector(database)
        logger.critical("Starting To Extract Real Jobs data from Linkdein Using ALL IDS ")
        job_collector.extract_jobs_data()
        

    

    





