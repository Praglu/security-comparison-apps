import base64
from fastapi import APIRouter, Depends, Form, Header, HTTPException, Request, Response, status
from sqlalchemy import engine
from sqlalchemy.exc import SQLAlchemyError

from database import get_db


router = APIRouter(
    prefix='/login',
    tags=['login']
)


@router.post('/get-token')
def login_user(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: engine.base.Connection = Depends(get_db),
):
    try:
        result = db.execute(f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'")
        user = result.fetchone()

        if user:
            email_bytes = email.encode('ascii')
            email_base64_bytes = base64.b64encode(email_bytes)
            token = email_base64_bytes.decode('ascii')
            response.headers['X-Token'] = token
            return {'token': token}
        raise HTTPException(status_code=401, detail='Incorrect email or password')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Error logging in user: ' + str(e))


def get_current_user(token: str = Header(...), db: engine.base.Connection = Depends(get_db)):
    try:
        token_base64_bytes = token.encode('ascii')
        email_bytes = base64.b64decode(token_base64_bytes)
        email = email_bytes.decode('ascii')

        result = db.execute('SELECT * FROM users WHERE email=?', (email,))
        user = result.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail='Invalid token')
        return True
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Error while trying to find user: ' + str(e))
