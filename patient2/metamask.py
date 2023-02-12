from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from web3 import Web3
import db
from uuid import uuid4

w3 = Web3(Web3.HTTPProvider(""))


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
        signed_address = w3.eth.account.recover_message(
            messageEncoded, signature=HexBytes(sighash)).lower()

        if signed_address == address:
            user = self.repo.getUser(address)
            if user:
                user.nonce = self.get_nonce()
                self.repo.getUser(user.publicKey)
                return True
            raise Exception("Should not be reachable")
        return False
