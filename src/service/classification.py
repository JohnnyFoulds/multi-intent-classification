"""
This module uses an LLM to classify user verbatims.
"""

import asyncio
import copy
from typing import List
import logging
import config.config as config
import llm.classification as classification
from service.app_schemas import Verbatim, Classification

logger = config.logger

def remove_other(input:Classification) -> Classification:
    """If there is more than one category, remove the other category"""

    # It is possible that the classification service returns None
    if input is None:
        return None

    updated = copy.deepcopy(input)
    if len(updated.categories) > 1:
        updated.categories = [x for x in updated.categories if x.category != "Other"]

    return updated if len(updated.categories) else input

def get_classification(text:str, llm):
    """Classify the top level categories for the specified text."""
    try:
        logging.info("Classifying verbatim...")
        result = remove_other(classification.get_classification(text=text, llm=llm))
        logging.info("Classiffication done.")
    except Exception as e:
        logger.warning("Error classifying verbatim: %s", e)
        result = None

    return result

async def async_classification_wrapper(verbatim:Verbatim) -> Classification:
    """Wrap the classification function in an async function."""
    logger.info("Classifying verbatim %s", verbatim.id)
    result = await asyncio.to_thread(get_classification, verbatim.text)

    return Classification(
        id=verbatim.id,
        classification=result
    )

async def bulk_classify(verbatim_list: List[Verbatim],
                        batch_size:int=500) -> List[Classification]:
    """
    Classify a list of verbatims.

    Test with:
    [
        { "id": "1", "text": "one" },
        { "id": "2", "text": "The quick brown fox jumps over the lazy dog." },
        { "id": "3", "text": "the service is ok" }
    ]
    """
    logger.info("Classifying %d verbatims", len(verbatim_list))
    classifications = []

    # confirm that the endpoint is running
    if endpoint.get_endpoint_status() != "InService":
        logger.error("Endpoint is not running")
        raise Exception("Endpoint is not running")


    for batch_start in range(0, len(verbatim_list), batch_size):
        batch = verbatim_list[batch_start:batch_start + batch_size]

        tasks = [asyncio.create_task(async_classification_wrapper(item)) \
                for item in batch]

        results = await asyncio.gather(*tasks)
        classifications.extend(results)

    return classifications
