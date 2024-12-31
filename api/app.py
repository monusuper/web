from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

import os

# Get the directory path dynamically
static_dir = os.path.join(os.path.dirname(__file__), "../static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

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
