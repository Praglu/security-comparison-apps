import sqlite3
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy import engine
from sqlalchemy.exc import SQLAlchemyError

from database import get_db


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/')
def create_user(
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
        return {'message': 'User created successfully'}
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
