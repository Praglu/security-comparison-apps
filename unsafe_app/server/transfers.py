import base64
import sqlite3
from fastapi import APIRouter, Cookie, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import engine
from sqlalchemy.exc import SQLAlchemyError

from database import get_db


router = APIRouter(
    prefix='/transfers',
    tags=['transfers']
)


templates = Jinja2Templates(directory='templates')


@router.post('/', response_class=HTMLResponse)
def create_transfer(
    request: Request,
    title: str = Form(...),
    account_number: str = Form(...),
    amount: str = Form(...),
    reciever_info: str = Form(...),
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

        db.execute(
            'INSERT INTO transfers (user_id, title, account_number, amount, reciever_info, date) VALUES (?, ?, ?, ?, ?, ?)', 
            (user_id, title, account_number, amount, reciever_info, date),
        )
        db.commit()
        return templates.TemplateResponse(
            request=request,
            name='successful-transfer.html',
            context={
                'message': 'Transfer created successfully!',
            }
        )
    except SQLAlchemyError as e:
        return HTTPException(status_code=500, detail='Error creating transfer: ' + str(e))


@router.get('/')
def list_transfers(db: engine.base.Connection = Depends(get_db)):
    try:
        result = db.execute("SELECT * FROM transfers")
        transfers = result.fetchall()

        if not transfers:
            raise HTTPException(status_code=404, detail='No transfers in the database')
        return transfers
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Error listing transfers: ' + str(e))


@router.get('/transfer')
def retrieve_transfer(transfer_id, db: engine.base.Connection = Depends(get_db)):
    try:
        result = db.execute(f"SELECT * FROM transfers WHERE id='{transfer_id}'")
        transfer = result.fetchone()

        if not transfer:
            raise HTTPException(status_code=404, detail='Transfer not found')
        return transfer
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Error retrieving transfer: ' + str(e))
