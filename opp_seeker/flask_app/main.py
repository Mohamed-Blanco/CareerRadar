from flask import Flask
from flask_apscheduler import APScheduler

from opp_seeker.database.database_connection import Database_connection
from opp_seeker.flask_app.routes.piplines_routes import piplines_bluprint
from opp_seeker.logger import Logger
from opp_seeker.pipelines.pipeline_data import Pipline

logger = Logger().get_logger()

def create_app():
    """Application factory function with Flask-APScheduler"""
    app = Flask(__name__)
    app.config.from_pyfile('./config/config.py')
    
    app.config['SCHEDULER_TIMEZONE'] = 'Africa/Casablanca'
    app.config['SCHEDULER_API_ENABLED'] = True
    app.config['SCHEDULER_JOBSTORES'] = {
        'default': {'type': 'memory'}
    }

    scheduler = APScheduler()
    scheduler.init_app(app)

    @scheduler.task('cron', id='daily_pipeline_job', hour=0, minute=40)
    def scheduled_job():
        """Scheduled pipeline job"""
        with app.app_context():
            try:
                logger.info("Starting scheduled pipeline job")
                database_connection = Database_connection()
                pipline = Pipline(database_connection)
                pipline.execute_pipeline(8000)
                logger.info("Scheduled pipeline job completed successfully")
            except Exception as e:
                logger.error(f"Error in scheduled job: {str(e)}")

    app.register_blueprint(piplines_bluprint, url_prefix='/api/pipelines')

    if app.config.get('SCHEDULER_API_ENABLED'):
        scheduler.start()
        logger.info("Scheduler started successfully")

    return app

if __name__ == '__main__':
    app = create_app()
    try:
        app.run(
            host=app.config['HOST'],
            debug=app.config['ENV'],
            port=app.config['PORT'],
            threaded=True,
            processes=1
        )
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
