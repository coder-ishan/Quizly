from fastapi import FastAPI
import uvicorn


#uvicorn main:app --host 0.0.0.0 --port 8080


app = FastAPI()


@app.get("/") 
async def root():
    return {"message": "Heo World"}



