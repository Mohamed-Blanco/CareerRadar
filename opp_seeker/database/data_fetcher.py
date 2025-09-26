import json
import datetime
import os 
import psycopg2
from opp_seeker.logger import Logger
logger = Logger().get_logger()
from opp_seeker.database.data_handler import Data_handler
from opp_seeker.database.database_connection import Database_connection

# This class role is to collect the data_warehouse from the scrappers and then insert the data_warehouse into table 'jobs'
# we need to add an traitement to avoid SQL injection

class Data_fetcher :
    def __init__(self,database_connection : Database_connection,data_handler :Data_handler):
        self.db = database_connection
        self.data_handler = data_handler

    def collect_jobs_data(self):
        #connection.open_connection()
        query = """INSERT INTO job_records (title,job_details,date_enregistrement) VALUES (%s,%s,%s)"""  # Here is were you prepare you query
        logger.info("Gathering jobs data_warehouse ")
        jobs = self.data_handler.get_scrapped_jobs_data()
        conn = self.db.get_connection()  # starting a database connection

        for job in jobs :

            title = job['title']
            date_enregistrement = datetime.datetime.now()
            logger.info(title)
            
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (title,json.dumps(job),date_enregistrement))  # Example: Fetching users table
                    conn.commit()

            except psycopg2.DatabaseError as e:
                logger.error(e)
                conn.rollback()

        self.db.release_connection(conn)

            # try:
            #     conn.cursor.execute(query, (title,json.dumps(job),date_enregistrement))
            #     conn.commit()
            # except psycopg2.DatabaseError as e:
            #
            #     conn.rollback()

                # In PostgreSQL, once a transaction fails (e.g., due to a constraint violation),
                # the transaction enters an aborted state. No further commands can be executed in
                # that transaction until you explicitly roll back the transaction or end it. Until then,
                # PostgreSQL ignores all subsequent commands, leading to the error you see





def main():
    database_connection = Database_connection()
    data_hl = Data_handler(database_connection)
    data_collector = Data_fetcher(database_connection,data_hl)
    data_collector.collect_jobs_data()

if __name__ == "__main__":
    main()
