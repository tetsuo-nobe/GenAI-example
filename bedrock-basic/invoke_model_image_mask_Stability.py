"""

イメージのマスク(Stability Stable Diffusion XL:Pillowは使わない)

"""
import logging
import boto3
import json
from botocore.exceptions import ClientError

### For Image
#from PIL import Image
import base64
import io

import datetime


logger = logging.getLogger(__name__)


#
# Stability Stable Diffusion XL
# https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/model-parameters-diffusion-1-0-text-image.html
#

print("---" * 42)
print("Stability Stable Diffusion XL")
print("---" * 42)

prompt_data = "A cat in the woods. A red balloon floating next to a car."

try:
    image_file = "car-woods.jpg"
    mask_file = "mask.jpg"
    
    image_data = None
    mask_data = None
    
    # 元のイメージの読み込み
    with open(image_file,"rb") as f:
        image_data = f.read()
    
    base64_image_data = base64.b64encode(image_data).decode()
    
    # マスクイメージの読み込み
    with open(mask_file,"rb") as f:
        mask_data = f.read()
    
    base64_mask_data = base64.b64encode(mask_data).decode()
    
    
    bedrock_runtime = boto3.client('bedrock-runtime')

    # プロンプト
    body = json.dumps(
            {
                "text_prompts": [
                    {
                      "text": prompt_data
                    }
                ],
                "init_image_mode": "IMAGE_STRENGTH",
                "image_strength": 0.7,
                "init_image": base64_image_data,
                "mask_source": "MASK_IMAGE_WHITE",
                "mask_image": base64_mask_data,
                "sampler": "K_DPM_2_ANCESTRAL",
                "cfg_scale": 7,
                "clip_guidance_preset": "FAST_BLUE",
                "samples": 1, 
                "steps": 30
            }
        )
    modelId = "stability.stable-diffusion-xl-v1"
    accept = "application/json"
    contentType = "application/json"
    
    # invoke model 
    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    # body は StreamingBody オブジェクトで返されるので read() で取得する
    response_body = json.loads(response.get("body").read())
    
    # body の base64: に base64 でエンコードされたイメージがある
    base64_image = response_body.get("artifacts")[0].get("base64")
    
    # base64コードから HTML の img タグなどで出力は可能
    
    # base64コードからファイルに保存するには、バイナリに戻す
    image_bytes = base64.b64decode(base64_image)
    dt_now = str(datetime.datetime.now())
    with open(f"{dt_now}.png", "wb") as f:
        f.write(image_bytes)
    print(f'save to "{dt_now}.png".')    
    
    
    # # Pillow を使ってファイルに書く方法
    # base64_bytes = base64_image.encode('ascii')
    # image_bytes = base64.b64decode(base64_bytes)
    # dt_now = datetime.datetime.now()
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save(str(dt_now) + ".png")
    

   

except ClientError as error:
    if error.response['Error']['Code'] == 'AccessDeniedException':
           print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubeshoot this issue please refer to the following resources.\
                 \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                 \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")

    else:
        raise error
