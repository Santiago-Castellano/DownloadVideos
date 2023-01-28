from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from downloader import download

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_video")
async def get_video(url: str = Form(), only_audio: bool = Form()):
    file_path = download(url, only_audio, "/tmp/video/")
    return FileResponse(
        path=file_path,
        filename=file_path,
        media_type='text/mp4'
    )
    #return JSONResponse({"file_path":file_path})
    #return FileResponse()