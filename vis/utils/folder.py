import os
from loguru import logger

def check_path_exists(path:str):
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f'Create path {path}')
    else:
        logger.warning(f'Path {path} exists')