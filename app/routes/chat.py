from fastapi import APIRouter, HTTPException

from app.controllers.react_controller import ReActController
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter()

controller = ReActController()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:

        response = controller.handle_message(request.message)

        return ChatResponse(
            response=response
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )