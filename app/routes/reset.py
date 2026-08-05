from fastapi import APIRouter

from app.routes.chat import controller

router = APIRouter()


@router.post("/reset")
def reset():

    controller.reset_conversation()

    return {
        "message": "Conversation reset successfully."
    }