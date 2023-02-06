import tempfile
from pytube import YouTube

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_video")
async def get_video(url: str = Form(), only_audio: bool = Form()):
    yt = YouTube(url)
    if only_audio:
        video = yt.streams.filter(
            only_audio=True
        ).first()
    else:
        video = yt.streams.filter(
            file_extension="mp4",
            only_video=True,
        ).order_by('resolution').desc().first()
    
    out_file = video.download(output_path=tempfile.gettempdir())
    return FileResponse(
        path=out_file,
        filename=out_file,
        media_type='text/mp4'
    )