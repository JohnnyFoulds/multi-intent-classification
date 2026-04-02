"""
This module is used to get configuration settings.
"""

import os
import logging

CONFIG_PATH = os.path.dirname(__file__)

def get_logger():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

logger = get_logger()

CATEGORY_DEFINITIONS_FILE = os.getenv("CATEGORY_DEFINITIONS_FILE",
                                      "category_definitions.jsonl")

PLANNING_PROMPT_PATH = os.getenv("PLANNING_PROMPT_PATH",
                                 "planning_prompt.txt")

IDENTIFICATION_PROMPT_PATH = os.getenv("IDENTIFICATION_PROMPT_PATH",
                                       "identification_prompt.txt")

SENTIMENT_PROMPT_PATH = os.getenv("SENTIMENT_PROMPT_PATH",
                                  "sentiment_prompt.txt")

IGNORE_LIST_PATH = os.getenv("IGNORE_LIST_PATH",
                             "ignore_list.txt") 