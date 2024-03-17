"""
Use the Large Language Model to perform verbatim classification.
"""

import json
from typing import List, Dict

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

from config.config import (
    CONFIG_PATH, 
    CATEGORY_DEFINITIONS_FILE,
    PLANNING_PROMPT_PATH,
    IDENTIFICATION_PROMPT_PATH,
    SENTIMENT_PROMPT_PATH,
    IGNORE_LIST_PATH
)
from config.format_instructions import SentimentCategories
import llm.mistral as mistral

def load_category_definitions() -> List[Dict[str, str]]:
    """
    Loads the category definitions from the category definitions file.
    """
    category_definitions = []

    file_path = f"{CONFIG_PATH}/{CATEGORY_DEFINITIONS_FILE}"
    with open(file_path, 'r') as f:
        for line in f:
            category_definitions.append(json.loads(line))

    return category_definitions

def load_prompt_template(path:str) -> str:
    """
    Loads the prompt template from the specified path.
    """
    with open(path, 'r') as f:
        return f.read()

def load_ignore_list() -> List[str]:
    """
    Loads the ignore list from the specified path.
    """
    ignore_list = []

    file_path = f"{CONFIG_PATH}/{IGNORE_LIST_PATH}"
    with open(file_path, 'r') as f:
        for line in f:
            ignore_list.append(line.strip().lower())

    return ignore_list

# load the constants
CATEGORY_DEFINITIONS = load_category_definitions()

PLANNING_PROMPT_TEMPLATE = load_prompt_template(
    f"{CONFIG_PATH}/{PLANNING_PROMPT_PATH}")

IDENTIFICATION_PROMPT_TEMPLATE = load_prompt_template(
    f"{CONFIG_PATH}/{IDENTIFICATION_PROMPT_PATH}")

SENTIMENT_PROMPT_TEMPLATE = load_prompt_template(
    f"{CONFIG_PATH}/{SENTIMENT_PROMPT_PATH}")

IGNORE_LIST = load_ignore_list()

# create the prompt templates
prompt_planning = PromptTemplate.from_template(PLANNING_PROMPT_TEMPLATE)
prompt_identification = PromptTemplate.from_template(IDENTIFICATION_PROMPT_TEMPLATE)
prompt_sentiment = PromptTemplate.from_template(SENTIMENT_PROMPT_TEMPLATE)

# chain objects
chain_planning = None
chain_identification = None
chain_sentiment = None
sentiment_output_parser = None

def configure_chains(llm):
    global chain_planning
    global chain_identification
    global chain_sentiment
    global sentiment_output_parser

    # create the chains
    chain_planning = prompt_planning | llm | StrOutputParser()
    chain_identification = prompt_identification | llm | StrOutputParser()

    sentiment_output_parser = PydanticOutputParser(pydantic_object=SentimentCategories)
    chain_sentiment = prompt_sentiment | llm | sentiment_output_parser

def should_ignore(text:str) -> bool:
    """
    Determines if the specified text should be ignored.
    """
    global IGNORE_LIST

    return text.lower() in IGNORE_LIST

def get_classification(text:str, llm):
    """
    Classify the top level categories for the specified text.
    """
    global chain_planning
    global chain_identification
    global chain_sentiment

    global CATEGORY_DEFINITIONS
    global sentiment_output_parser

    try:
        # check if the text should be ignored
        if should_ignore(text):
            return None

        # configure the chains
        configure_chains(llm=llm)

        # get the initial thoughts
        initial_thoughts = chain_planning.invoke({
            "category_definitions": CATEGORY_DEFINITIONS,
            "text": text
        })

        # get the identified topics
        identified_topics = chain_identification.invoke({
            "category_definitions": CATEGORY_DEFINITIONS,
            "initial_thoughts": initial_thoughts,
            "text": text
        })

        # get the sentiment
        sentiment = chain_sentiment.invoke({
            "category_definitions": CATEGORY_DEFINITIONS,
            "identified_categories": identified_topics,
            "format_instructions": sentiment_output_parser.get_format_instructions(),
            "text": text
        })

        return sentiment
    except ValueError as e:
        print(f"Value Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None
