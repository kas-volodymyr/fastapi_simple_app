from pydantic import BaseModel


class JournalMessage(BaseModel):
    message: str
