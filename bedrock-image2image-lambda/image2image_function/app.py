"""

  S3 からダウンロードした画像＋プロンプトで新しい画像を生成、S3バケットに格納し署名付きURLを返す

""" 
import base64
import io
import os
import json
import logging
import boto3
from PIL import Image

from botocore.exceptions import ClientError

import datetime
import time

from aws_xray_sdk.core import patch
patch(['boto3'])

class ImageError(Exception):
    "Custom exception for errors returned by SDXL"
    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_image(model_id, body):
    """
    Generate an image using SDXL 1.0 on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        image_bytes (bytes): The image generated by the model.
    """

    logger.info("Generating image with SDXL model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')
   
    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())
    print(response_body['result'])

    base64_image = response_body.get("artifacts")[0].get("base64")
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = response_body.get("artifacts")[0].get("finishReason")

    if finish_reason == 'ERROR' or finish_reason == 'CONTENT_FILTERED':
        raise ImageError(f"Image generation error. Error code is {finish_reason}")


    logger.info("Successfully generated image withvthe SDXL 1.0 model %s", model_id)

    return image_bytes



def main_handler(event,context):
    """
    Entrypoint for SDXL example.
    """
    
    lambda_runtime = os.environ.get('LambdaRuntime')
    if lambda_runtime:
        prifix = "/tmp/"
    else:
        prifix = ""

    logging.basicConfig(level = logging.INFO,
                        format = "%(levelname)s: %(message)s")
    
    bucket = event["bucket"]
    key = event["key"]
    resized = prifix +  "resized.png"
    model_id='stability.stable-diffusion-xl-v1'
    prompt=event["prompt"]
                        
    s3 = boto3.client('s3')
    # download file from S3 bucket
    time_start = time.perf_counter()
    response = s3.get_object(Bucket = bucket, Key = key)
    s3obj = response["Body"].read()

    time_end = time.perf_counter()
    time_diff = time_end- time_start
    print(time_diff)  # 経過時間（秒）
                        
    # Resize モデルに渡す画像の幅と高さは 64 の倍数である必要がある
    # また、base64 にした後のサイズにも制限がある
    
    # リサイズ前の画像を読み込み
    img = Image.open(io.BytesIO(s3obj))
    # 読み込んだ画像の幅、高さを取得し変更
    (width, height) = (img.width // 4, img.height // 4)
    # 画像をリサイズする
    img_resized = img.resize((width, height))
    img_resized.save(resized)
   
    # Read reference image from file and encode as base64 strings.
    with open(resized,"rb") as image_file:
        init_image = base64.b64encode(image_file.read()).decode('utf8')

    print('-----------------')
    print(len(init_image))
    # Create request body.
    body=json.dumps({
        "text_prompts": [
        {
        "text": prompt
        }
    ],
    "init_image": init_image,
    "style_preset" : "isometric"
    })

    try:
        image_bytes=generate_image(model_id = model_id,
                                 body = body)
        #image = Image.open(io.BytesIO(image_bytes))
        #image.show()
        dt_now = datetime.datetime.now()
        generated_image = "gen_" + str(dt_now) + ".png"
        #image.save(prifix + generated_image)
        s3.put_object(Body=image_bytes, Bucket = bucket, Key = generated_image )
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket,
                                                            'Key': generated_image},
                                                    ExpiresIn=600)
        return response


    except ClientError as err:
        message=err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    except ImageError as err:
        logger.error(err.message)
        print(err.message)

    else:
        print(f"Finished generating text with SDXL model {model_id}.")


if __name__ == "__main__":
    event = {"prompt":"Scenery of two dogs sitting and relaxing", "bucket":"tnobe-images", "key": "dog11MB.png"}
    context = {}
    url = main_handler(event,context)
    print(url)

