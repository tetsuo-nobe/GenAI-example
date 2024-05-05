"""

list_foundation_models の基本

"""
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

bedrock = boto3.client('bedrock')
#bedrock_runtime = boto3.client('bedrock-runtime')

try:
    response = bedrock.list_foundation_models()
    models = response["modelSummaries"]
    logger.info("Got %s foundation models.", len(models))
except ClientError:
    logger.error("Couldn't list foundation models.")
    raise
else:
    for model in models:
            print("\n" + "=" * 42)
            print(f' Model: {model["modelId"]}')
            print("-" * 42)
            print(f' Name: {model["modelName"]}')
            print(f' Provider: {model["providerName"]}')
            print(f' Model ARN: {model["modelArn"]}')
            print(f' Input modalities: {model["inputModalities"]}')
            print(f' Output modalities: {model["outputModalities"]}')
            print(f' Supported customizations: {model["customizationsSupported"]}')
            print(f' Supported inference types: {model["inferenceTypesSupported"]}')
            print("=" * 42)