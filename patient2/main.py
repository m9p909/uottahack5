from json import JSONEncoder
from uuid import uuid4
from fastapi import FastAPI, Request, Response, Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from pydantic import BaseModel
import db
import secrets
from metamask import Metamask
from web3 import Web3
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

sessions = {}

templates = Jinja2Templates(directory="templates")


class Sessions:
    sessions = {}
    sessionKey = 'session'

    def init_session(self, response: Response, request: Request):
        if self.sessionKey in request.cookies:
            id = str(uuid4())
            self.sessions[id] = {}
            response.set_cookie(self.sessionKey, id)
            return response
        else:
            return response

    def getSessionValue(self, request: Request, key: str | int):
        id = request.cookies[self.sessionKey]
        return self.sessions[id][key]

    def setSessionValue(self, request: Request, key: str | int, value):
        print(JSONEncoder().encode(self.sessions))
        id = request.cookies[self.sessionKey]
        if id in self.sessions:
            self.sessions[id][key] = value
        else:
            self.sessions[id] = {key: value}


sessions = Sessions()
metamask = Metamask(db.getUserRepo())


class SessionKeys:
    address = 0
    nonce = 1
    verified = 2


session_keys = SessionKeys()


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):

    response = templates.TemplateResponse("index.html", {"request": request})
    return sessions.init_session(response, request)


@app.get('/login')
async def login_request(request: Request,  publicAddress: str):
    nonce = metamask.login_request(publicAddress)
    if nonce:
        res = Response(nonce)
        sessions.setSessionValue(
            request,  session_keys.address, publicAddress)
        print("login request")
        print(publicAddress)
        sessions.setSessionValue(request,  session_keys.nonce, nonce)
        return res
    else:
        return Response("could not get nonce", status_code=401)


class VerifySignatureBody(BaseModel):
    sig: str


@app.post('/verify-signature')
async def verify_signature(request: Request, body: VerifySignatureBody):
    address = sessions.getSessionValue(request, session_keys.address)
    originalMessage = sessions.getSessionValue(request, session_keys.nonce)
    if (metamask.verify_signature(body.sig, originalMessage, address)):
        sessions.setSessionValue(
            request,  session_keys.verified, True)
        res = Response("success")
        return res
    else:
        return Response("unsuccessful", 401)
