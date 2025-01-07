from typing import List, Optional
from pydantic import BaseModel


#pydanctic schema for the Question

class QuestionBase(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    

class QuizBase(BaseModel):
    quizId: int
    questions: List[QuestionBase]

class QuizCreate(QuizBase):
    pass

class Quiz(QuizBase):
    id: int

    class Config:
        orm_mode = True
