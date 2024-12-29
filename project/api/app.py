from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML Pages
@app.get("/", response_class=HTMLResponse)
async def home():
    html_path = Path("templates/home.html")
    return HTMLResponse(content=html_path.read_text())

@app.get("/commands", response_class=HTMLResponse)
async def commands():
    html_path = Path("templates/commands.html")
    return HTMLResponse(content=html_path.read_text())

@app.get("/help", response_class=HTMLResponse)
async def help_page():
    html_path = Path("templates/help.html")
    return HTMLResponse(content=html_path.read_text())

@app.get("/about", response_class=HTMLResponse)
async def about_page():
    html_path = Path("templates/about.html")
    return HTMLResponse(content=html_path.read_text())
