from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from upload import s3, BUCKET_NAME
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

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
