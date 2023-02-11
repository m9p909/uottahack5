from uuid import uuid4
import uuid
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import db
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

sessions = {}

templates = Jinja2Templates(directory="templates")

sessionKey = 'session'

class MetaMask:
    def loginRequest(publicAddress: str ):





@app.get("/", response_class=HTMLResponse)
async def getIndex(request: Request):

    response =  templates.TemplateResponse("index.html", {"request": request});
    if sessionKey in request.cookies:
        return response
    else:
        key = str(uuid.uuid4())
        sessions[key] = {}
        response.set_cookie(sessionKey,key )
        return response

@app.get('/login')
async def loginRequest(publicAddress: str):
    user = db.getUserRep().getUser(publicAddress)
    if(user):
        return user.nonce


    


