from typing import List
from pydantic import BaseModel

class QuestionBase(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class QuizBase(BaseModel):
    quizId: str  # Ensure quizId is a string
    questions: List[QuestionBase]

class QuizCreate(QuizBase):
    pass

class Quiz(QuizBase):
    id: int

    class Config:
        orm_mode = True