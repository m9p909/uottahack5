class User:
    publicKey: str
    nonce: str
    key: str
    data: map
    doctorData: map # a copy of data encrypted with the doctor's credentials


class UserRepo:
    data =  { }
    def getUser(self, publicKey: str) ->  User | None:
        return self.data[publicKey]

repo = UserRepo()

def getUserRep():
    return repo




