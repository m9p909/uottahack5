class User:
    publicKey: str
    nonce: str
    key: str
    data: map
    doctorData: map  # a copy of data encrypted with the doctor's credentials


class UserRepo:
    data = {}

    def getUser(self, publicKey: str) -> User | None:
        if publicKey in self.data:
            return self.data[publicKey]
        return None

    def setUser(self, user: User) -> User | None:
        if user.publicKey in self.data:
            self.data[user.publicKey] = user
            return user
        return None

    def createUser(self, user: User) -> User | None:
        self.data[user.publicKey] = user


repo = UserRepo()


def getUserRepo():
    return repo
