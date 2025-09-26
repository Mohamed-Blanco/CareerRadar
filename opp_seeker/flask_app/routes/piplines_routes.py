from flask import Blueprint, jsonify

from opp_seeker.database.database_connection import Database_connection
from opp_seeker.logger import Logger
from opp_seeker.pipelines.pipeline_data import Pipline
import threading

from opp_seeker.pipelines.pipeline_scrape import Pipline_scrapping

logger = Logger().get_logger()


piplines_bluprint = Blueprint('pipelines',__name__)
database_connection = Database_connection()
pipline = Pipline(database_connection)
piplinescrap = Pipline_scrapping()

@piplines_bluprint .route('/fetch', methods=['POST'])
def fetch_process_pipline():
    threading.Thread(target=piplinescrap.execute_data_fetching_processing).start()
    return jsonify({"message": "Pipeline executed successfully"}), 200


@piplines_bluprint .route('/ids/<batch_size>', methods=['POST'])
def fetch_ids_pipline(batch_size=99999999):
    threading.Thread(target=piplinescrap.execute_Linkdein_ids_collection, args=(int(batch_size),)).start()
    return jsonify({"message": "Pipeline executed successfully"}), 200


@piplines_bluprint.route('/data/<batch_size>', methods=['POST'])
def fetch_data_pipline(batch_size=99999999):
    threading.Thread(target=piplinescrap.execute_Linkdein_Data_pipeline, args=(int(batch_size),)).start()
    return jsonify({"message": "Pipeline executed successfully"}), 200

@piplines_bluprint.route('/full/<batch_size>', methods=['POST'])
def full_data_pipline(batch_size=99999999):
    threading.Thread(target=pipline.execute_pipeline, args=(int(batch_size),)).start()
    return jsonify({"message": "Pipeline executed successfully"}), 200



