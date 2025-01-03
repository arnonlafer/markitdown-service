import shutil
from markitdown import MarkItDown
from fastapi import FastAPI, UploadFile
from uuid import uuid4

md = MarkItDown()

app = FastAPI()

@app.post("/convert")
async def convert_markdown(file: UploadFile):
    unique_id = uuid4()
    temp_dir = f"./temp/{unique_id}"

    shutil.os.makedirs(temp_dir, exist_ok=True)

    file_path = f"{temp_dir}/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    result = md.convert(file_path)
    content = result.text_content

    shutil.rmtree(temp_dir)

    return {"result": content}
