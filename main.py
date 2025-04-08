import secrets
import base64
import pyotp
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated
from model import MOTD, MOTDBase
from sqlalchemy.sql import func

# SQLite Database
sqlite_file_name = "motd.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# FastAPI 
app = FastAPI(docs_url=None, redoc_url=None)
templates = Jinja2Templates(directory=".")
security = HTTPBasic()

# Users
users = {
    "sister": "ii2210_sister_semangatTucil",
    "vaelya": "ii2210_vaelya"
}

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/motd", response_class=HTMLResponse)
async def get_motd_page(request: Request, session: SessionDep):
    motd = session.query(MOTD).order_by(func.random()).first()
    if motd:
        return templates.TemplateResponse("motd.html", {
            "request": request,
            "motd": motd.motd,
            "creator": motd.creator,
            "created_at": motd.created_at
        })
    raise HTTPException(status_code=404, detail="No message found.")

@app.get("/api/motd")
async def get_motd_json(session: SessionDep):
    motd = session.query(MOTD).order_by(func.random()).first()
    if motd:
        return {
            "motd": motd.motd,
            "creator": motd.creator,
            "created_at": motd.created_at
        }
    raise HTTPException(status_code=404, detail="No message found.")

@app.post("/motd")
async def post_motd(
    message: MOTDBase,
    session: SessionDep,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_password_bytes = credentials.password.encode("utf8")

    if credentials.username in users:
        s = base64.b32encode(users.get(credentials.username).encode("utf-8")).decode("utf-8")
        totp = pyotp.TOTP(s=s, digest="SHA256", digits=8)
        if secrets.compare_digest(current_password_bytes, totp.now().encode("utf8")):
            new_motd = MOTD(motd=message.motd, creator=credentials.username)
            session.add(new_motd)
            session.commit()
            session.refresh(new_motd)
            return {"message": "MOTD created successfully."}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid userid or password.")

if __name__ == "__main__":
    import uvicorn
    create_db_and_tables()
    uvicorn.run("main:app", host="0.0.0.0", port=17787, reload=True)
