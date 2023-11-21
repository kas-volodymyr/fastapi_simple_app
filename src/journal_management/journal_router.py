import asyncio
from datetime import datetime
from fastapi import APIRouter, Depends, Security, status
from src.auth.dependencies import auhorized_user_role
from src.auth.schemas import Role
from src.auth.utils import oauth2_scheme
from src.core.exceptions import CustomHTTPException
from src.journal_management.schemas import JournalMessage


journal_router = APIRouter(
    prefix="/journal",
    tags=["journal"],
)

journal_path = "src/journal_management/journal.txt"
journal_lock = asyncio.Lock()

@journal_router.post("/write", response_description="Write to the journal")
async def write_to_journal(
        journal_message: JournalMessage,
        authorized_user_role: str = Depends(auhorized_user_role),
        token: str = Security(oauth2_scheme),
    ):
    if authorized_user_role != Role.admin:
        raise CustomHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Required admin role")
    async with journal_lock:
        try:
            with open(journal_path, mode="a") as file:
                file.write(f"{datetime.now()}: {journal_message.message}\n")
            return {"message": "Message written to the journal successfully"}
        except Exception as e:
            raise CustomHTTPException(status_code=500, detail=f"Error writing to file: {str(e)}")


@journal_router.get("/read", response_description="Read from the journal")
async def read_journal(authorized_user_role: str = Depends(auhorized_user_role), token: str = Security(oauth2_scheme)):
    if authorized_user_role not in [Role.admin, Role.developer]:
        raise CustomHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Required admin or developer role")
    async with journal_lock:
        try:
            with open(journal_path, mode="r") as file:
                lines = file.readlines()

            messages = [line.strip() for line in lines]

            return {"messages": messages}
        except Exception as e:
            raise CustomHTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
