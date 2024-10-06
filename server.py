from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.users import router as users_router
from routes.assistant import router as asistant_router
from routes.files import router as files_router
from routes.authentication import router as authentication_router
from routes.pastries import router as pastries_router

app = FastAPI(
    title="Asistente Virtual de Pastelería",
    version="1.0",
    description="Asistente Virtual de Pastelería para la atención al cliente y asistencia de empleados.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(users_router)
app.include_router(asistant_router)
app.include_router(files_router)
app.include_router(authentication_router)
app.include_router(pastries_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
