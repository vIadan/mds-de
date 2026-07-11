import secrets

class Message:

    def __init__(self, content: str):
        self.content = content

class Minibatch:

    def __init__(self):
        self.id = secrets.token_urlsafe(4)
        self.messages = []

    def __repr__(self):
        return f'Minibatch({len(self.messages)} messages)'

    def add(self, message: Message):
        self.messages.append(message)