from click import option
from app.middleware.middleware import TimerMiddleware
from fastapi import FastAPI
from app.models import models
from app.controllers import admin, common, portfolios, stand_alone_controllers,websocket,loginAPI,options
from fastapi.middleware.cors import CORSMiddleware
from app.db.db import engine
from app.admin import setup_admin

app = FastAPI(debug=True)

@app.get("/")
def hc():
    return {
    "APP": "",
    "VERSION": "0.1"
}

app.add_middleware(TimerMiddleware)

# Configure CORS settings
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_admin(app)
def create_app():
    models.Base.metadata.create_all(bind=engine)
    app.include_router(common.router, prefix="/common")
    app.include_router(websocket.router, prefix="/websocket")
    app.include_router(loginAPI.router, prefix="/login")
    app.include_router(portfolios.router, prefix="/portfolios")
    app.include_router(admin.router, prefix="/custom/admin")
    app.include_router(stand_alone_controllers.router, prefix="/standalone")
    app.include_router(options.router, prefix="/option")

    return app


create_app()

