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


class Metamask:
    repo: db.UserRepo

    def __init__(self, repo: db.UserRepo):
        self.repo = repo

    def get_nonce(self):
        return f"""
    Hey User! Sign this token to acces the website. It won't have any fees, gas or otherwise. 
    UUID: {uuid4()}
    """

    def createUser(self, address: str):
        user = db.User()
        user.publicKey = address
        user.nonce = self.get_nonce()
        self.repo.createUser(user)
        return user

    def login_request(self, address):
        user = self.repo.getUser(address)

        if user:
            return user.nonce
        else:
            user = self.createUser(address)
            return user.nonce

    def verify_signature(self, sighash: str, ogmessage: str, address: str):
        messageEncoded = encode_defunct(text=ogmessage)
        print("verify1")
        print(sighash)
        print(ogmessage)

        signed_address = w3.eth.account.recover_message(
            messageEncoded, signature=HexBytes(sighash))

        print("verify")
        print(signed_address)
        print(address)
        if signed_address == address:
            user = self.repo.getUser(address)
            if user:
                user.nonce = self.get_nonce()
                self.repo.getUser(user.publicKey)
                return True
            raise Exception("Should not be reachable")
        return False


sessions = Sessions()
metamask = Metamask(db.getUserRepo())


class SessionKeys:
    address = 0
    nonce = 1
    verified = 2


session_keys = SessionKeys()

w3 = Web3(Web3.HTTPProvider(""))


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
    message: str
    sig: str


@app.post('/verify-signature')
async def verify_signature(request: Request, body: VerifySignatureBody):
    address = sessions.getSessionValue(request, session_keys.address)
    originalMessage = sessions.getSessionValue(request, session_keys.nonce)
    print('verify controller')
    print(address)
    if (metamask.verify_signature(body.sig, originalMessage, address)):
        sessions.setSessionValue(
            request,  session_keys.verified, True)
        res = Response("success")
        return res
    else:
        return Response("unsuccessful", 401)
