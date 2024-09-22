import schedule
import time
import subprocess
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the full path to the Python executable
python_executable = "/usr/local/bin/python"

def run_app_registration():
    logging.info("Running app registration task...")
    result = subprocess.run(
        [python_executable, "-m", "apps.services.app_registration"],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": os.path.abspath(os.path.dirname(__file__) + "/../..")}
    )
    if result.returncode == 0:
        logging.info("App registration task completed successfully.")
    else:
        logging.error(f"App registration task failed with error: {result.stderr}")

def run_enterprise_application():
    logging.info("Running enterprise application task...")
    result = subprocess.run(
        [python_executable, "-m", "apps.services.enterprise_application"],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": os.path.abspath(os.path.dirname(__file__) + "/../..")}
    )
    if result.returncode == 0:
        logging.info("Enterprise application task completed successfully.")
    else:
        logging.error(f"Enterprise application task failed with error: {result.stderr}")

# Schedule the tasks
schedule.every(1).minutes.do(run_app_registration)
schedule.every(1).minutes.do(run_enterprise_application)

while True:
    schedule.run_pending()
    time.sleep(1)