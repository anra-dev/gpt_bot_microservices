import logging

logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('log_file.log')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
