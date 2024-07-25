from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.register.route import router as user_router
from auth.route import router as auth_router
from users.get_profile.router import router as profile_router
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware import Middleware
from core.security import JWTAuth

app: FastAPI = FastAPI()

middleware: Middleware = Middleware(AuthenticationMiddleware, backend=JWTAuth())

app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(profile_router)


@app.get('/')
def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "Running!"})
