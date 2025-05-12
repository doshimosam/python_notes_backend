from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from .db.session import engine
from .models import m_note, m_user
from .routes import auth, notes, users

app = FastAPI()

app.include_router(users.router)
app.include_router(notes.router)
app.include_router(auth.router)

m_user.Base.metadata.create_all(engine)
m_note.Base.metadata.create_all(engine)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # Log or process the error as needed
    return JSONResponse(
        status_code=422,
        content={"message": "Invalid input data, please check your JSON format."},
    )
