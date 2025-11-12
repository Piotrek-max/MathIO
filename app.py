from fastapi import FastAPI, Request, Form, Response, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import os

import matrix_operations
from plotting_functions.plot_from_txt import parse_xy_from_text, save_plot_png

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

PLOTS_DIR = os.path.join("static", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "To jest wiadomość dynamiczna!"})

@app.get("/matmul", response_class=HTMLResponse)
async def get_api(request: Request):
    return templates.TemplateResponse("matmul.html", {"request": request})


@app.post("/matmul", response_class=HTMLResponse)
async def submit_matrices(request: Request, inputText1: str = Form(...), inputText2: str = Form(...)):
    result = matrix_operations.multiply_matrix_end(inputText1.strip(), inputText2.strip())
    if result != 'Matrix multiplication is not possible':
        result_text = '\n'.join([' '.join(map(str, row)) for row in result])
    else:
        result_text = 'Matrix multiplication is not possible'
    return templates.TemplateResponse("matmul.html", {"request": request,"textA":inputText1, "textB":inputText2, "resultText": result_text})

@app.get("/api/json", response_class=JSONResponse)
async def get_json():
    data = {"message": "This is a JSON response", "status": "success"}
    return JSONResponse(content=data)


@app.get("/plot", response_class=HTMLResponse)
async def plot_form(request: Request):
    return templates.TemplateResponse("plot.html", {"request": request, "img_url": None, "error": None})

@app.post("/plot", response_class=HTMLResponse)
async def plot_upload(request: Request, file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".txt"):
            raise ValueError("Wyślij plik z rozszerzeniem .txt.")
        raw = await file.read()
        x, y, title = parse_xy_from_text(raw, file.filename)
        png_name = save_plot_png(x, y, title, PLOTS_DIR)
        img_url = f"/static/plots/{png_name}"
        return templates.TemplateResponse("plot.html", {"request": request, "img_url": img_url, "error": None})
    except ValueError as e:
        return templates.TemplateResponse("plot.html", {"request": request, "img_url": None, "error": str(e)})
    except Exception:
        return templates.TemplateResponse("plot.html", {"request": request, "img_url": None, "error": "Nieoczekiwany błąd podczas generowania wykresu."})
