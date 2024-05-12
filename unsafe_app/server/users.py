import base64
import sqlite3
from fastapi import APIRouter, Cookie, Depends, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import engine
from sqlalchemy.exc import SQLAlchemyError

from database import get_db


router = APIRouter(
    prefix='/users',
    tags=['users']
)


templates = Jinja2Templates(directory='templates')


@router.post('/')
def create_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    pesel: float = Form(...),
    phone: int = Form(...),
    db: sqlite3.Connection = Depends(get_db)
):
    try:
        db.execute(
            'INSERT INTO users (email, password, first_name, last_name, pesel, phone) VALUES (?, ?, ?, ?, ?, ?)', 
            (email, password, first_name, last_name, pesel, phone),
        )
        db.commit()
        return templates.TemplateResponse(request=request, name='created-user.html', context={'email': email})
    except SQLAlchemyError as e:
        return HTTPException(status_code=500, detail='Error creating user: ' + str(e))


@router.get('/')
def list_users(db: engine.base.Connection = Depends(get_db)):
    try:
        result = db.execute("SELECT * FROM users")
        users = result.fetchall()

        if not users:
            raise HTTPException(status_code=404, detail='No users in the database')
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Error listing users: ' + str(e))


@router.get('/user')
def retrieve_user(user_id, db: engine.base.Connection = Depends(get_db)):
    try:
        result = db.execute(f"SELECT * FROM users WHERE id='{user_id}'")
        user = result.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Error retrieving user: ' + str(e))


@router.get('/user-info', response_class=HTMLResponse)
def user_info(
    request: Request,
    token: str = Cookie(...),
    db: engine.base.Connection = Depends(get_db),
):
    if token is None:
        raise HTTPException(status_code=401, detail='Unauthorized')
    
    try:
        token_base64_bytes = token.encode('ascii')
        email_bytes = base64.b64decode(token_base64_bytes)
        email = email_bytes.decode('ascii')

        result = db.execute('SELECT * FROM users WHERE email=?', (email,))
        user = result.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail='Invalid token')
        
        user_transfers_result = db.execute('SELECT * FROM transfers WHERE user_id=?', (user[0],))
        user_transfers = user_transfers_result.fetchall()

        user_officials_result = db.execute('SELECT * FROM officials WHERE user_id=?', (user[0],))
        user_officials = user_officials_result.fetchall()

        return templates.TemplateResponse(
            request=request,
            name='user-info.html',
            context={
                'id': user[0],
                'email': user[1],
                'first_name': user[3],
                'last_name': user[4],
                'pesel': user[5],
                'phone': user[6],
                'transfers': user_transfers,
                'officials': user_officials,
            },
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Error while trying to find user: ' + str(e))
