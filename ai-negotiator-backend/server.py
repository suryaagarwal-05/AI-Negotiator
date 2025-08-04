# api_server.py
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from main import main  # Import your refactored main function
from fastapi.middleware.cors import CORSMiddleware

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Check for CSV file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    
    # Save the uploaded file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # Run your backend logic
    try:
        result = await main(file_location)  # Await main and get result with pdf_path
        pdf_path = result.get("pdf_path")
        if not pdf_path or not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="PDF report was not generated.")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    # Return the PDF file as a download
    return FileResponse(
        path=pdf_path,
        filename=os.path.basename(pdf_path),
        media_type="application/pdf"
    )
