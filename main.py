from fastapi import FastAPI
import uvicorn
from api.CRUDOUT import router as CRUD_router
from database.database_up import insert_data

app = FastAPI()
app.include_router(CRUD_router)

if __name__ == '__main__':
    insert_data()
    uvicorn.run("main:app", host="0.0.0.0", port=8000)