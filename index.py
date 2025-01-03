from fastapi import FastAPI, File, UploadFile
from markitdown import convert_to_markdown

app = FastAPI()

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    try:
        content = await file.read()
        markdown = convert_to_markdown(content)
        return {"markdown": markdown}
    except Exception as e:
        return {"error": str(e)}
