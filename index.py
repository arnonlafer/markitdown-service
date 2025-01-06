import os
import shutil
from markitdown import MarkItDown
from fastapi import FastAPI, UploadFile, Form
from uuid import uuid4
from openai import OpenAI
from docling.document_converter import DocumentConverter

# FastAPI app
app = FastAPI()

# Writable directory for temporary files
WRITABLE_DIR = "/tmp"  # Replace with "/workspace" or another writable path if needed

@app.post("/convert")
async def convert_markdown(file: UploadFile, api_key: str = Form(None), use_docling: bool = Form(False)):
    try:
        # Initialize the converter based on the parameter
        if use_docling:
            converter = DocumentConverter()
        else:
            if api_key:
                client = OpenAI(api_key=api_key)
                converter = MarkItDown(llm_client=client, llm_model="gpt-4o")
            else:
                converter = MarkItDown()

        # Create a unique temporary directory
        unique_id = uuid4()
        temp_dir = os.path.join(WRITABLE_DIR, str(unique_id))
        os.makedirs(temp_dir, exist_ok=True)

        # Save the uploaded file to the temporary directory
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Convert the file
        if use_docling:
            result = converter.convert_to_markdown(file_path)  # Assuming Docling's method
        else:
            result = converter.convert(file_path)  # MarkItDown's method

        # Extract content based on the converter used
        content = result.text_content if not use_docling else result

        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

        return {"result": content}

    except Exception as e:
        # Clean up in case of error
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return {"error": str(e)}
