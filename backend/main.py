import datetime
from http.client import HTTPException
import json
from typing import List
from typing_extensions import Annotated
from llm import generateQuestions
from database import engine
from fastapi import Depends, FastAPI, UploadFile, File
from sqlalchemy.orm import Session
import models
from database import SessionLocal
import models, schemas
from database import engine, get_db
from fastapi import FastAPI, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import logging
import aiofiles
import os
import uuid
#uvicorn main:app --host localhost --port 8080


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://0.0.0.0:8080/"],  # Adjust this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"quizId":1}


@app.post("/generatequestions/")
async def generate_questions(
    tags: List[str] = Form(...),
    numQuestions: int = Form(...),
    difficulty: str = Form(...),
    files: List[UploadFile] = File(None),
):
    query = " ".join(tags)
    quizId = str(uuid.uuid4())
    
    questions =  await generateQuestions(query, quizId,numQuestions,difficulty,files)
    
    os.makedirs(f"uploads/{quizId}", exist_ok=True)
    
    if files:
        for file in files:
            async with aiofiles.open(f"uploads/{quizId}/{file.filename}", "wb") as buffer:
                content = await file.read()
                await buffer.write(content)

    db = SessionLocal()
    try:
        question_json = json.loads(questions)
        question_json["quizId"] = str(quizId)
        
        quiz_schema = schemas.QuizCreate(**question_json)
        create_quiz(quiz=quiz_schema, db=db)
    finally:
        db.close()
    return {"quizId": quizId}

@app.post("/createquizzes/", response_model=schemas.Quiz)
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(get_db)):
    db_quiz = models.Quiz(quizId=quiz.quizId, questions=[question.model_dump() for question in quiz.questions])
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@app.get("/quizzes/", response_model=List[schemas.Quiz])
def read_quizzes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    quizzes = db.query(models.Quiz).offset(skip).limit(limit).all()
    return quizzes

@app.get("/quizzes/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(quiz_id: str, db: Session = Depends(get_db)):
    db_quiz = db.query(models.Quiz).filter(models.Quiz.quizId == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz