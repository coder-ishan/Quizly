"use client"
import Logo from "@/components/Navbar";
import Question from "@/components/question";
import axios from "axios";
import { useEffect, useState } from "react";

export default function QuizPage({params}) {
    const id = params.quizId;
    const [quiz, setQuiz] = useState(null);
    const [isAvailable, setIsAvailable] = useState(true);
    useEffect(() => {
        const fetchQuiz = async () => {
            try {
                const res = await axios.get(`http://localhost:8080/quizzes/${id}`);
                setQuiz(res.data);
            } catch (error) {
                console.error("Error fetching quiz:", error);
                setIsAvailable(false);
            }
            
        };
        fetchQuiz();
        
    }, [id]);
    if (!quiz) {
        if(!isAvailable){
            return (
                <div className="flex flex-col items-center justify-center h-screen">
                <p className="text-lg font-semibold">Quiz not found</p>
                </div>
            );
        }
        else{
            return (
                <div className="flex flex-col items-center justify-center h-screen">
                <div className="w-16 h-16 border-4 border-blue-500 border-dashed rounded-full animate-spin"></div>
                <p className="mt-4 text-lg font-semibold">Loading your Quiz...</p>
                </div>
            );
        }
       

    }
    console.log(quiz);

    
    return (
        <div>
            <Logo />
            {quiz.questions.map((q, index) => (
                <Question
                    key={index}
                    QuestionNo={index + 1}
                    Question={q.question}
                    Options={q.options}
                    correctAnswer={q.correct_answer}
                    ExplanationText = {q.explanation}
                />
            ))}
        </div>
    );
    
}

