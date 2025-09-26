
from psycopg2 import OperationalError
from psycopg2._psycopg import InterfaceError
from opp_seeker.logger import Logger
logger = Logger().get_logger()
from opp_seeker.database.database_connection import Database_connection
import psycopg2
from psycopg2.extras import execute_values
import os
import json
from opp_seeker.utils import Utils
from opp_seeker.general_params import BASE_DIR

class Data_handler:
    def __init__(self,database_connection : Database_connection):
        self.db = database_connection
        self.utils = Utils()

    def Clean_outdated_jobs(self):
        logger.info("Cleaning outdated jobs")
        query = """"""
        conn = self.db.get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(query, ())
                conn.commit()
                jobs = cursor.fetchall()
                logger.debug(f" Cleaned Jobs Successfully  : {len(jobs)}")
                return jobs
        except psycopg2.OperationalError as e:
            logger.error(f"Error: {e}")
            conn.rollback()
        finally:
            self.db.release_connection(conn)

    def get_jobs_data(self):
        ## Please Add Last date Proccessed
        ## To not duplicate processing data_warehouse
        logger.info("Getting jobs data_warehouse")
        query = """SELECT * FROM job_records WHERE date_enregistrement > %s ORDER BY id   """  ## Here is were you prepare you query
        
        conn = self.db.get_connection()  #Get fresh connection here

        file = os.path.join(BASE_DIR, 'configuration.json')
        with open(file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        ## i added this so i will not get the data for an already scraped ID OK ?
        date = config.get("last_date_processed")


        try:
            with conn.cursor() as cursor:
                cursor.execute(query,(date,))
                conn.commit()
                jobs = cursor.fetchall()
                logger.debug(f" Jobs to process : {len(jobs)}")
                return jobs
        except psycopg2.OperationalError as e:
            logger.error(f"Error: {e}")
            conn.rollback()  # Rollback on error
        finally:
            self.db.release_connection(conn)

    def store_bulk_data(self, data):
        if not data:
            logger.error("Bulk insert failed: 'null'")
            return

        query = """INSERT INTO job_metadata 
        (id_original_job, location, title, description, months_of_experience, sector_travail,
         entreprise, skills, date_processement, date_posted,job_logo, total_skills)  
        VALUES %s"""

        conn = self.db.get_connection()  #  Get fresh connection here
        try:
            with conn.cursor() as cursor:
                execute_values(cursor, query, data)
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Bulk insert failed: {e}")
        finally:
            self.db.release_connection(conn)

    def get_scrapped_jobs_data(self):
        file = os.path.join(os.path.dirname(__file__), '..', 'data_warehouse', 'raw', 'jobs_data.json')

        logger.info("Getting data_warehouse from json files")

        with open(file, 'r', encoding='utf-8') as f:
            js_data = json.load(f)

        with open(file, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

        return js_data

    def get_job_ids(self):
        file = os.path.join(BASE_DIR, 'configuration.json')
        with open(file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        ## i added this so i will not get the data for an already scraped ID OK ?
        date = config.get("last_date_scrapped")
        ids = []

        conn = self.db.get_connection()  # Get fresh connection here

        try:
            query = """SELECT l.linkdein_id , l.found_by_keyword FROM linkdein_job_ids l WHERE l.date_creation > %s """
            with conn.cursor() as cursor:
                cursor.execute(query, (date,))
                conn.commit()
                ids = cursor.fetchall()

            # conn.cursor.execute(query)

            return ids
        except Exception as e:
            conn.rollback()
            logger.error(f"Error when trying to get ids {e}")

        self.db.release_connection(conn)
        return ids


    def store_bluk_ids(self, job_batch):
        """
        Store a batch of job IDs in the database, ensuring proper connection handling.

        Args:
            job_batch: List of tuples containing (linkedin_id, date_creation, found_by_keyword)

        Returns:
            int: Number of records inserted, or 0 if an error occurred
        """
        if not job_batch:
            logger.error("Bulk insert failed: empty job batch provided")
            return 0

        conn = None
        try:
            # Get a new connection from the pool
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                # First drop the temporary table if it exists from a previous failed operation
                cursor.execute("DROP TABLE IF EXISTS data_source")
                conn.commit()

                # Create the temporary table
                cursor.execute("""
                    CREATE TEMPORARY TABLE data_source (
                        linkdein_id varchar(200),
                        date_creation DATE,
                        found_by_keyword varchar(500) 
                    )
                """)
                conn.commit()

                # Populate temp table
                execute_values(cursor,
                               "INSERT INTO data_source (linkdein_id, date_creation, found_by_keyword) VALUES %s",
                               job_batch)
                conn.commit()

                # Insert into main table, skipping duplicates
                cursor.execute("""
                    INSERT INTO linkdein_job_ids (linkdein_id, date_creation, found_by_keyword)
                    SELECT s.linkdein_id, s.date_creation, s.found_by_keyword 
                    FROM data_source s
                    LEFT JOIN linkdein_job_ids t ON s.linkdein_id = t.linkdein_id
                    WHERE t.linkdein_id IS NULL
                    RETURNING linkdein_id
                """)

                # Get count of inserted records
                result = cursor.fetchall()
                inserted_count = len(result) if result else 0
                conn.commit()

                # Explicitly drop the temporary table
                cursor.execute("DROP TABLE IF EXISTS data_source")
                conn.commit()

                logger.info(f"Successfully inserted {inserted_count} new job IDs")
                return inserted_count

        except Exception as e:
            logger.error(f"Bulk insert failed: {str(e)}")
            # Print stack trace for debugging
            import traceback
            logger.debug(f"Exception traceback: {traceback.format_exc()}")

            if conn:
                try:
                    # Attempt to rollback and clean up
                    conn.rollback()
                    with conn.cursor() as cursor:
                        cursor.execute("DROP TABLE IF EXISTS data_source")
                        conn.commit()
                except Exception as cleanup_error:
                    logger.error(f"Error during cleanup after failed insert: {str(cleanup_error)}")

            return 0
        finally:
            # Make sure we release the connection back to the pool
            if conn:
                try:
                    self.db.release_connection(conn)
                except Exception as e:
                    logger.error(f"Error releasing connection: {str(e)}")



    def delete_all_scrapped_ids(self):
        conn = self.db.get_connection()  #Get fresh connection here

        try:
            query = """DELETE FROM linkdein_job_ids l"""
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()

            # conn.cursor.execute(query)
            logger.debug("All scrapped job ids are deleted ")
        except Exception as e:
            conn.rollback()
            logger.error(f"Error when trying to delete ids ids {e}")
        finally:
            self.db.release_connection(conn)





def main():

    database_connection = Database_connection()
    df = Data_handler(database_connection)
    ids = [40,41,43,60]

if __name__ == "__main__" :
    main()