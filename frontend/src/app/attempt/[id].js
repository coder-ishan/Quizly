"use client"
import Navbar from "@/components/logo";
import Question from "@/components/question";

export default function QuizPage(quizId) {
   
    return (

        <div>
            <Navbar />
            <Question QuestionNo="1" Question="What is the capital of India?" Options={["Delhi", "Mumbai", "Kolkata", "Chennai"]} correctAnswer="1"/>
            <Question QuestionNo="2" Question="What is the capital of USA?" Options={["New York", "Washington DC", "Los Angeles", "Chicago"]} correctAnswer="2" />
            <Question QuestionNo="3" Question="What is the capital of UK?" Options={["London", "Manchester", "Birmingham", "Liverpool"]} correctAnswer="3"/>
            <Question QuestionNo="4" Question="What is the capital of Australia?" Options={["Sydney", "Melbourne", "Canberra", "Brisbane"]} correctAnswer="1"/>
        </div>
    );
    
}

