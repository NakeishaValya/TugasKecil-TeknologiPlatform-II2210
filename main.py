import secrets
import base64
import pyotp
import random
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlmodel import create_engine, Session, SQLModel, select
from typing import Annotated
from model import MOTD, MOTDBase

# SQLite Database
sqlite_file_name = "motd.db"
sqlite_url = f"sqlite:////{sqlite_file_name}"
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
security = HTTPBasic()

# Users - lengkapi dengan userid dan shared_secret yang sesuai
allowed_users = {
    "sister": "ii2210_sister_semangatTucil",
    "vaelya": "ii2210_koicaKeren"
}

# Mount static files directory for serving HTML files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    # Menampilkan index.html yang telah dibuat sebelumnya
    return FileResponse("static/index.html")

@app.get("/motd")
async def get_motd(session: SessionDep):
    # Mengambil message of the day secara acak dari database
    result = session.exec(select(MOTD)).all()
    
    if not result:
        return JSONResponse(
            status_code=404,
            content={"message": "No messages found in database."}
        )
    
    # Pilih message secara acak
    random_message = random.choice(result)
    return random_message

@app.post("/motd")
async def post_motd(message: MOTDBase, session: SessionDep, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_password_bytes = credentials.password.encode("utf8")
    valid_username, valid_password = False, False
    
    try:
        if credentials.username in allowed_users:
            valid_username = True
            s = base64.b32encode(allowed_users.get(credentials.username).encode("utf-8")).decode("utf-8")
            totp = pyotp.TOTP(s=s, digest="SHA256", digits=8)
            valid_password = secrets.compare_digest(current_password_bytes, totp.now().encode("utf8"))
            
            if valid_password and valid_username:
                # Menambahkan message of the day ke basis data
                db_message = MOTD.from_orm(message)
                session.add(db_message)
                session.commit()
                session.refresh(db_message)
                return db_message
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid userid or password."
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid userid or password."
            )
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    import uvicorn
    
    create_db_and_tables()
    
    uvicorn.run(app, host="0.0.0.0", port=17787)
