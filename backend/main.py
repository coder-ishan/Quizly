from typing import List
from sqlalchemy import UUID
from typing_extensions import Annotated
from database import engine
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import models
from database import SessionLocal
import models, schemas
from database import engine, get_db
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from llm import generateQuestions
#uvicorn main:app --host localhost --port 8080


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generatequestions/")
async def generate_questions(form_data: Annotated[dict, Depends()]):
    query = form_data.get('tag')
    id = form_data.get('id')
    return generateQuestions(query, id)



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
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = db.query(models.Quiz).filter(models.Quiz.quizId == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz