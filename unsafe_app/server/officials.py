import base64
import sqlite3
from fastapi import APIRouter, Cookie, Depends, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import engine
from sqlalchemy.exc import SQLAlchemyError

from database import get_db


router = APIRouter(
    prefix='/officials',
    tags=['officials']
)


templates = Jinja2Templates(directory='templates')


@router.post('/')
def create_official(
    request: Request,
    user_first_name: str = Form(...),
    user_last_name: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    token: str = Cookie(...),
    db: sqlite3.Connection = Depends(get_db)
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
        
        user_id = user[0]
        user_email = user[1]

        db.execute(
            '''INSERT INTO officials (
                user_id,
                user_email,
                user_first_name,
                user_last_name,
                description,
                date
            ) VALUES (?, ?, ?, ?, ?, ?)''', 
            (user_id, user_email, user_first_name, user_last_name, description, date),
        )
        db.commit()
        return templates.TemplateResponse(
            request=request,
            name='successful-official.html',
            context={
                'message': 'Official created successfully!',
            }
        )
    except SQLAlchemyError as e:
        return HTTPException(status_code=500, detail='Error creating official: ' + str(e))


@router.get('/')
def list_officials(db: engine.base.Connection = Depends(get_db)):
    try:
        result = db.execute("SELECT * FROM officials")
        transfers = result.fetchall()

        if not transfers:
            raise HTTPException(status_code=404, detail='No officials in the database')
        return transfers
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Error listing officials: ' + str(e))


@router.get('/official')
def retrieve_transfer(official_id, db: engine.base.Connection = Depends(get_db)):
    try:
        result = db.execute(f"SELECT * FROM officials WHERE id='{official_id}'")
        transfer = result.fetchone()

        if not transfer:
            raise HTTPException(status_code=404, detail='Official not found')
        return transfer
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Error retrieving officials: ' + str(e))
