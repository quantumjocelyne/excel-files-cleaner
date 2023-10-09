import os

from starlette.responses import FileResponse

from AFM import clean_and_process_excel_files, expected_header_names, unwanted_header_elements
import fastapi
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from typing import List
import shutil


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="tempAPI")

#the index.html file for the HTML frontend where users can upload Excel files is in tempAPI directory


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/upload/")
def redirect_to_home():
    return fastapi.responses.RedirectResponse("/")


@app.post("/upload/")
async def upload_files(request: Request, files: List[UploadFile] = File(...), plot_option: str = Form("combined"), dpi: int = Form(500), timestamp_count: int = Form(10),
                       temp_range: str = Form("10,30"), relH_range: str = Form("25,70")
                       ):

    global temp_min, temp_max, relH_min, relH_max
    if plot_option == "combined" and len(files) == 1:
        error_message = "For the 'combined' option, you need to upload more than one file."
        return templates.TemplateResponse("index.html", {"request": request, "error_message": error_message})

        #return {"error": "For the 'combined' option, you need to upload more than one file."}

    temp_dir = "temp_files"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    temp_files = []

    for file in files:
        temp_file = os.path.join(temp_dir, file.filename)
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        temp_files.append(temp_file)

        # Split the ranges and convert them to integers
        temp_min, temp_max = map(int, temp_range.split(','))
        relH_min, relH_max = map(int, relH_range.split(','))

    clean_and_process_excel_files(temp_files, expected_header_names, unwanted_header_elements, dpi, timestamp_count, combined_plot=plot_option == "combined",
                                  temp_range=(temp_min, temp_max), relH_range=(relH_min, relH_max))

    if plot_option == "combined":
        file_path = os.path.join("static", "Plots.png")
        return FileResponse(file_path, headers={"Content-Disposition": "attachment; filename=Plots.png"})
    else:
        # Zip all the individual plot files and serve
        shutil.make_archive(os.path.join(temp_dir, "plots"), 'zip', temp_dir)
        return FileResponse(os.path.join(temp_dir, "plots.zip"),
                            headers={"Content-Disposition": "attachment; filename=plots.zip"})

    #return {"uploaded_files": [file.filename for file in files], "plot_option": plot_option, "dpi": dpi,
            #"timestamp": timestamp}

"""
@app.post("/upload/result")
async def redirect_to_result():
    return {"uploaded_files": [file.filename for file in files], "plot_option": plot_option, "dpi": dpi,
            "timestamp": timestamp}"""