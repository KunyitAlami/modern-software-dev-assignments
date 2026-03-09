from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import Base, engine, SessionLocal
from models import Task

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    db = SessionLocal()
    tasks = db.query(Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


@app.post("/add")
def add_task(title: str = Form(...), description: str = Form("")):
    db = SessionLocal()
    task = Task(title=title, description=description)
    db.add(task)
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).get(task_id)
    db.delete(task)
    db.commit()
    return RedirectResponse("/", status_code=303)

@app.get("/edit/{task_id}", response_class=HTMLResponse)
def edit_page(request: Request, task_id: int):
    db = SessionLocal()
    task = db.query(Task).get(task_id)

    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "task": task}
    )


@app.post("/update/{task_id}")
def update_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form("")
):
    db = SessionLocal()
    task = db.query(Task).get(task_id)

    task.title = title
    task.description = description

    db.commit()

    return RedirectResponse("/", status_code=303)
