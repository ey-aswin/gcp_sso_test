from fastapi import FastAPI, Request
import httpx
from fastapi_sso.sso.microsoft import MicrosoftSSO
from dotenv import load_dotenv

load_dotenv()
import os

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT = os.getenv("TENANT")
REDIRECT_URI = os.getenv("REDIRECT_URI")
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


sso = MicrosoftSSO(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    tenant=TENANT,
    redirect_uri=REDIRECT_URI,
    allow_insecure_http=True,
)


@app.get("/auth/login")
async def auth_init():
    """Initialize auth and redirect"""
    async with sso:
        return await sso.get_login_redirect()


@app.get("/auth/callback") 
async def auth_callback(request: Request):
    """Verify login"""
    async with sso:
        return await sso.verify_and_process(request)
