from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware


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

from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

discord = oauth.register(
    name="discord",
    client_id=DISCORD_CLIENT_ID,
    client_secret=DISCORD_CLIENT_SECRET,
    access_token_url="https://discord.com/api/oauth2/token",
    authorize_url="https://discord.com/api/oauth2/authorize",
    api_base_url="https://discord.com/api/",
    client_kwargs={"scope": "identify guilds"},
)
# Login Route
@app.get("/login")
async def login(request: Request):
    redirect_uri = "https://web-pdm2.onrender.com/callback"
    return await discord.authorize_redirect(request, redirect_uri)

# Callback Route
@app.get("/callback")
async def callback(request: Request):
    token = await discord.authorize_access_token(request)
    user = await discord.get("users/@me", token=token)
    request.session["user"] = user.json()
    return RedirectResponse("/")

# Logout Route
@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse("/")

# Middleware to Check Login
async def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@app.get("/profile")
async def profile(user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {"request": user, "user": user})

@app.get("/dashboard")
async def dashboard(user: dict = Depends(get_current_user)):
    guilds = await discord.get("users/@me/guilds", token=user["token"])
    for guild in guilds.json():
        guild["icon_url"] = (
            f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}.png"
            if guild["icon"]
            else "https://via.placeholder.com/128"
        )
    return templates.TemplateResponse(
        "dashboard.html", {"request": user, "guilds": guilds.json()}
    )

