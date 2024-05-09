import base64
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import router as auth_router
from database import initialize_database
from officials import router as officials_router
from transfers import router as transfers_router
from users import router as users_router


app = FastAPI(
    title='Unsafe App',
)

initialize_database()

templates = Jinja2Templates(directory='templates')

app.include_router(auth_router)
app.include_router(officials_router)
app.include_router(transfers_router)
app.include_router(users_router)


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name='index.html', context={},
    )


@app.get('/sign-up', response_class=HTMLResponse)
def sign_up(request: Request):
    return templates.TemplateResponse(
        request=request, name='sign-up.html', context={},
    )


@app.get('/create-transfer', response_class=HTMLResponse)
def create_transfer(request: Request):
    return templates.TemplateResponse(
        request=request, name='create-transfer.html', context={},
    )


@app.get('/create-official', response_class=HTMLResponse)
def create_official(request: Request):
    return templates.TemplateResponse(
        request=request, name='create-official.html', context={},
    )
