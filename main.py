from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.route import router as user_router
from auth.route import router as auth_router


app: FastAPI = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)


@app.get('/')
def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "Running!"})
