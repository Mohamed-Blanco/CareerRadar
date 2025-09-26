from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from opp_seeker.logger import Logger
logger = Logger().get_logger()
from opp_seeker.general_params import CHROME_API

class Chromedriver_Manager:

    def __init__(self):
        pass

    def get_chrome_driver(self):
        try:
            options = self.chrome_driver_configure()
            capabilities = options.to_capabilities()

            #driver = webdriver.Chrome()
            driver = webdriver.Remote(command_executor=CHROME_API,options=options)
            driver.set_window_size(1920,1080 )
            return driver
        except Exception as e:
            logger.error(f"Error when trying to Configure and start a Chromium driver {e}")
            driver = webdriver.Remote(command_executor=CHROME_API)
            driver.set_window_size(1920, 1080)
            return driver



    # def chrome_driver_configure(self):
    #     # initializing chrome driver with no Options !
    #     chrome_options = Options()
    #     chrome_options.add_argument("--start-maximized")  # Maximized
    #     chrome_options.add_argument("--disable-notifications")
    #     chrome_options.add_argument("--disable-extensions")
    #     chrome_options.add_argument(
    #         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
    #     # self.chrome_options.add_experimental_option("excludeSwitches" + "enable-automation")
    #     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    #     chrome_options.add_argument("--log-level=3")
    #     chrome_options.add_argument("--lang=en-US")

    def chrome_driver_configure(self):
        chrome_options = Options()

        # REQUIRED Docker/headless arguments
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")

        # Set window size (instead of --start-maximized which doesn't work headless)
        chrome_options.add_argument("--window-size=1920,1080")

        # Your existing arguments (keeping the good ones)
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--lang=en-US")

        return chrome_options




    def cleanup_stuck_sessions(self):
        """Clean up any stuck Selenium sessions"""
        try:
            import requests

            if not CHROME_API or not CHROME_API.strip():
                return

            status_url = CHROME_API.replace('/wd/hub', '/wd/hub/status')
            response = requests.get(status_url, timeout=10)

            if response.status_code != 200:
                return

            status = response.json()
            nodes = status.get('value', {}).get('nodes', [])

            for node in nodes:
                slots = node.get('slots', [])
                for slot in slots:
                    if 'session' in slot:
                        session_id = slot['session']['sessionId']
                        logger.info(f"Found stuck session {session_id}, attempting cleanup")

                        # Try to delete the session
                        delete_url = CHROME_API + f"/session/{session_id}"
                        requests.delete(delete_url, timeout=5)
                        logger.info(f"Attempted to clean up session {session_id}")

        except Exception as e:
            logger.warning(f"Could not cleanup stuck sessions: {e}")
            return

def main():
    ch = Chromedriver_Manager()
    drvr = ch.get_chrome_driver()
    drvr.get("https://www.test.com")

if __name__ == "__main__" :
    main()