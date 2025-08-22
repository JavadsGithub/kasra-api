
from fastapi import FastAPI
import routers
from model import database, model
import ssl
from routers import (
    authentication,
    broker,
    explorer,
    researcher,
    supervisor,
    user,
    admin,
    file,
    seed,
)
from fastapi.middleware.cors import CORSMiddleware

# from routers import admin

# from seed import seeding
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("./cert.pem", keyfile="./key.pem")


model.Base.metadata.create_all(database.engine)
app.include_router(authentication.router)
app.include_router(seed.router)
app.include_router(broker.router)
app.include_router(user.router)
app.include_router(explorer.router)
app.include_router(researcher.router)
app.include_router(file.router)
app.include_router(supervisor.router)
app.include_router(seed.router)
app.include_router(admin.router)


# seeding()
