import base64
from fastapi import APIRouter, Cookie, Depends, Form, Header, HTTPException,Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import engine
from sqlalchemy.exc import SQLAlchemyError

from database import get_db


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


templates = Jinja2Templates(directory='templates')


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
            response = RedirectResponse(url='/users/user-info', status_code=status.HTTP_302_FOUND)
            response.set_cookie(key='token', value=token)
            return response
        raise HTTPException(status_code=401, detail='Incorrect email or password')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Error logging in user: ' + str(e))


@router.get('/logout')
def logout(response: Response):
    response = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key='token')
    return response


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
