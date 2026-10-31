from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="TaskBox API")

# --- МОДЕЛИ ДАННЫХ (С учетом Задания 2: priority) ---
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    priority: int = Field(3, ge=1, le=5)  # Валидация 1-5, по умолчанию 3

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = None
    completed: bool | None = None
    priority: int | None = Field(None, ge=1, le=5)

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    priority: int = 3

# --- ХРАНИЛИЩЕ В ПАМЯТИ ---
tasks = {}
next_id = 1

# --- 1. Проверка сервера ---
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"service": "taskbox-api", "status": "good"}

# --- 2. Состояние сервиса ---
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK"}

# --- 3. Получение списка задач (С учетом Задания 3: поиск search) ---
@app.get("/tasks", response_model=list[Task])
def list_tasks(completed: bool | None = None, search: str | None = None):
    results = list(tasks.values())
    if completed is not None:
        results = [t for t in results if t.completed == completed]
    if search is not None:
        search_lower = search.lower()
        results = [t for t in results if search_lower in t.title.lower()]
    return results

# --- 4. Статистика (Задание 1) ---
@app.get("/stats", status_code=status.HTTP_200_OK)
def get_stats():
    all_tasks = list(tasks.values())
    total = len(all_tasks)
    completed_count = len([t for t in all_tasks if t.completed])
    pending_count = total - completed_count
    return {"total": total, "completed": completed_count, "pending": pending_count}

# --- 5. Получение одной задачи ---
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

# --- 6. Создание задачи ---
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate):
    global next_id
    task = Task(id=next_id, **data.model_dump())
    tasks[next_id] = task
    next_id += 1
    return task

# --- 7. Изменение задачи (PATCH) ---
@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    stored_task = tasks[task_id]
    update_data = data.model_dump(exclude_unset=True, exclude_none=True)
    updated_task = stored_task.model_copy(update=update_data)
    tasks[task_id] = updated_task
    return updated_task

# --- 8. Удаление задачи ---
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return None
