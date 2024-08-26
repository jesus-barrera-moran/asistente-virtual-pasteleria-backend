from typing import Annotated
from fastapi import Depends, APIRouter, Request, Response
from langserve import APIHandler

from agents.generic_agent.agent import Agent
from services.authentication import get_current_active_user_configuration, get_public_user_configuration

router = APIRouter()

@router.post("/asistente/invoke")
async def invoke_with_auth(
    request: Request,
    current_user: Annotated[dict, Depends(get_current_active_user_configuration)],
) -> Response:

    dynamic_api_handler = APIHandler(
        Agent(
            current_user["llm"],
            current_user["tools"](),
            current_user["prompt"]
        ).get_agent(),
        path="/asistente",
    )

    return await dynamic_api_handler.invoke(request)

@router.post("/atencion_cliente/invoke")
async def invoke_without_auth(
    request: Request,
    user_config: Annotated[dict, Depends(get_public_user_configuration)],
) -> Response:

    dynamic_api_handler = APIHandler(
        Agent(
            user_config["llm"],
            user_config["tools"](),
            user_config["prompt"]
        ).get_agent(),
        path="/atencion_cliente",
    )

    return await dynamic_api_handler.invoke(request)
