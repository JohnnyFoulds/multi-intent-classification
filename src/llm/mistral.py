# from typing import Any, Dict
# import config.config as config
# import llm.language_model as language_model

# """
# This class is used to start and stop a SageMaker Endpoint for using the
# `huggingface-llm-mistral-7b-instruct` LLM.
# """

# MODEL_ID = "huggingface-llm-mistral-7b-instruct"
# MODEL_VERSION = "2.0.0"

# predictor = None
# logger = config.logger

# def deploy_model(
#         model_id:str=MODEL_ID,
#         model_version:str=MODEL_VERSION):
#     """
#     Deploys the specified model version to the specified model id.
#     """
#     logger.info("Deploying model")
#     global predictor

#     try:
#         # check if the model was already deployed
#         if predictor is not None:
#             logger.info("Model already deployed")
#         elif get_endpoint_status() != 'NotFound':
#             # the model is deployed, but not initialized from this module
#             logger.warn("Model already deployed, using existing endpoint.")
#             predictor = language_model.get_predictor(model_id=model_id)
#         else:
#             # deploy the model
#             logger.info("Deploying new model")
#             _, predictor = language_model.deploy_model(
#                 model_id=model_id,
#                 model_version=model_version)
#     except Exception as e:
#         logger.error("Error deploying model: %s", e)
#         raise e

#     return predictor

# def get_endpoint_status(model_id:str=MODEL_ID):
#     """
#     Gets the status of the specified model.
#     """
#     logger.info("Getting endpoint status")
#     return language_model.get_model_status(model_id=model_id)

# def delete_endpoint(model_id:str=MODEL_ID):
#     """
#     Deletes the specified endpoint.
#     """
#     logger.info("Deleting endpoint")
#     global predictor

#     language_model.delete_endpoint(model_id=model_id)
#     predictor = None

# def create_llm_client(model_kwargs:Dict[str, Any] = {
#         'max_new_tokens': 512,
#         'top_p': 0.001,
#         'temperature': 0.001,
#     }):
#     """
#     Creates a LLMClient for the specified model.
#     """
#     #logger.info("Creating LLM Client")
#     global predictor

#     # deploy the model if it is not already deployed
#     if predictor is None:
#         deploy_model()

#     # create the client
#     return language_model.create_llm_client(
#         predictor=predictor, model_kwargs=model_kwargs)
