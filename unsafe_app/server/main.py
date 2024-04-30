from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import router as login_router
from database import initialize_database
from users import router as users_router


app = FastAPI(
    title='Unsafe App',
)

initialize_database()

templates = Jinja2Templates(directory='templates')

app.include_router(users_router)
app.include_router(login_router)


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name='index.html', context={},
    )


@app.get('/sign-up', response_class=HTMLResponse)
def sign_up(request: Request):
    return templates.TemplateResponse(
        request=request, name='sign_up.html', context={},
    )
