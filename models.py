from pydantic import BaseModel

class FileUpload(BaseModel):
    name = str
    filepath = str
