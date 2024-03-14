"""
Functions for instantiating and evaluating the LLMs for 
sentiment analysis and topic classification.
"""

import os
from typing import Any, Dict, List, Optional
import json
from tqdm.notebook import tqdm

import pandas as pd

import boto3
import sagemaker
from sagemaker.jumpstart.model import JumpStartModel
from botocore.exceptions import ClientError

from langchain.llms import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

from enum import Enum
from pydantic import BaseModel, Field, validator
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.transform import BaseTransformOutputParser

import config.config as config

import logging

# the aws profile and role to use
aws_profile = config.AWS_PROFILE
role = "arn:aws:iam::419655394329:role/Dev-SMStudio-SA-smrolessagemakerstudioroleD609A8C1-6MN86HHE7ATH"
region_name = "eu-west-1"
logger = logging.getLogger(__name__)

def deploy_model(model_id:str, model_version:str):
    """
    Deploys the specified model version to the specified model id.
    """
    global aws_profile
    global role
    global region_name

    model = None
    predictor = None

    try:
        # setup sagemaker session
        boto_session = boto3.Session(profile_name=aws_profile, region_name=region_name)
        sagemaker_session = sagemaker.Session(boto_session=boto_session)

        # create the model
        model = JumpStartModel(
            model_id=model_id,
            name=model_id,
            model_version=model_version,
            sagemaker_session=sagemaker_session,
            role=role,
            region=region_name,
            instance_type=config.get_instance_type())

        # deploy the endpoint
        predictor = model.deploy(
            initial_instance_count=config.INSTANCE_COUNT,
            endpoint_name=model_id,
            accept_eula=True)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        return model, predictor

def get_model_status(model_id:str):
    """
    Gets the status of the specified model.
    """
    global aws_profile
    global region_name

    try:
        # setup sagemaker client
        boto_session = boto3.Session(profile_name=aws_profile, region_name=region_name)
        sagemaker_client = boto_session.client('sagemaker')

        # describe the endpoint
        endpoint_description = sagemaker_client.describe_endpoint(EndpointName=model_id)

        return endpoint_description['EndpointStatus']
        
    except ClientError as e:
        if e.response['Error']['Message'].startswith("Could not find endpoint"):
            return 'NotFound'

    
def create_llm_client(predictor, model_kwargs:Dict[str, Any]):
    class ContentHandler(LLMContentHandler):
        content_type = "application/json"
        accepts = "application/json"

        def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
            input_str = json.dumps({
                "inputs": f"<s>[INST] {prompt} [/INST] ", 
                "parameters": model_kwargs})

            return input_str.encode("utf-8")

        def transform_output(self, output: bytes) -> str:
            response_json = json.loads(output.read().decode("utf-8"))
            return response_json[0]["generated_text"].strip()

    # create the content handler
    content_handler = ContentHandler()

    # create the llm clinet
    return SagemakerEndpoint(
        cache=False,
        endpoint_name=predictor.endpoint_name,
        region_name=region_name,
        model_kwargs=model_kwargs,
        credentials_profile_name=aws_profile,
        content_handler=content_handler,
        streaming=False,
        verbose=True,
    )

def delete_endpoint(model_id:str):
    """
    Deletes the specified endpoint.
    """
    global aws_profile
    global region_name

    try:
        # setup sagemaker client
        boto_session = boto3.Session(profile_name=aws_profile, region_name=region_name)
        sagemaker_client = boto_session.client('sagemaker')

        # delete the endpoint
        sagemaker_client.delete_endpoint(EndpointName=model_id)

        # delete the endpoint config
        sagemaker_client.delete_endpoint_config(EndpointConfigName=model_id)
        
    except ClientError as e:
        if e.response['Error']['Message'].startswith("Could not find endpoint"):
            logger.error("Endpoint not found")

def get_predictor(model_id:str):
    """
    Gets the predictor for the specified model.

    Returns:
        model: The model for the specified model.
        predictor: The predictor for the specified model.

    """
    global aws_profile
    global region_name

    try:
        # setup sagemaker session
        boto_session = boto3.Session(profile_name=aws_profile, region_name=region_name)
        sagemaker_session = sagemaker.Session(boto_session=boto_session)

        # create the predictor
        predictor = sagemaker.predictor.Predictor(
            endpoint_name=model_id,
            sagemaker_session=sagemaker_session)        

        return predictor
        
    except ClientError as e:
        if e.response['Error']['Message'].startswith("Could not find endpoint"):
            logger.error("Endpoint not found")