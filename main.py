from fastapi import FastAPI
import routers
from model import database, model
import ssl
from routers import authentication
from fastapi.middleware.cors import CORSMiddleware

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

# test
model.Base.metadata.create_all(database.engine)
app.include_router(authentication.router)
