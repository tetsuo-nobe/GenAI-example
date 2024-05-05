"""

S3バケットからサイズの大きなイメージを取得して保存
(Pillowパッケージ使用)

"""
from PIL import Image
import io

import base64
import io
import os
import json
import logging
import boto3
import datetime
from PIL import Image

from botocore.exceptions import ClientError

event = {"prompt":"Scenery where a dog is relaxing", "bucket":"tnobe-images", "key": "dog11MB.png"}

bucket = event["bucket"]
key = event["key"]

# Download from S3
s3 = boto3.client('s3')
response = s3.get_object(Bucket = bucket, Key = key)

# S3 の Body は StreamingBody が返るので byteにしたければ read() で読む
image_data = response["Body"].read()

image = Image.open(io.BytesIO(image_data))
#image.show()
dt_now = datetime.datetime.now()
image.save("basic_" + str(dt_now) + ".png")

