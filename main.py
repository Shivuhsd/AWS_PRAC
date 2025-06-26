from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from upload import s3, BUCKET_NAME
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import boto3
import json
from utils import get_objects
from fastapi.responses import StreamingResponse
from io import BytesIO

app = FastAPI()

load_dotenv()



@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    with open(f"uploaded_{file.filename}", "wb") as f:
        f.write(contents)
    try:
        s3.upload_file(f"uploaded_{file.filename}", BUCKET_NAME, f"uploaded_{file.filename}")
        os.remove(f"uploaded_{file.filename}")
    except ClientError as e:
        return {'error': e}
    return """
    <html>
        <body>
            <h1>File Uploaded Successfully.</h1>
        </body>
    </html>
    """
    # return {"filename": file.filename, "content_type": file.content_type}

@app.get("/", response_class=HTMLResponse)
def main():
    return """
    <html>
        <body>
            <form action="/upload/" enctype="multipart/form-data" method="post" style="background-color: red;">
                <input name="file" type="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """


@app.get("/get-files")
def get_files():
    res = get_objects(BUCKET_NAME)
    return res

@app.get("/get-object/{object_name}")
def get_object(object_name:str):
    object_n = object_name
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=object_name)
        file_stream = BytesIO(response['Body'].read())
        return StreamingResponse(file_stream, media_type="image/png")
    except ClientError as e:
        return {"error": "Something went wrong"}