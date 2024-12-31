from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi import FastAPI

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML pages
@app.get("/", response_class=HTMLResponse)
async def home():
    return Path("templates/home.html").read_text()

@app.get("/commands", response_class=HTMLResponse)
async def commands():
    return Path("templates/commands.html").read_text()

@app.get("/help", response_class=HTMLResponse)
async def help_page():
    return Path("templates/help.html").read_text()

@app.get("/about", response_class=HTMLResponse)
async def about_page():
    return Path("templates/about.html").read_text()
