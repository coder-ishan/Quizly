"use client"
import Navbar from "@/components/logo";

export default function QuizPage({quizData}) {
   
    
    return (
        <div className="min-h-screen bg-gray-100">
            <Navbar />
            <div className="flex justify-center mt-4">
                <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWliM210eXJiZGl5eGRta3VkY2NwOTN3Z2doZHl6NzNvdmEwM3hiMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9Dk1b9ZQt98GShqy8P/giphy.webp" alt="Quiz Gif" className="w-1/2 h-auto rounded-lg shadow-lg" />
            </div>
            <div className="flex flex-col items-center justify-center mt-10">
                <p className="text-lg font-semibold mb-4">Generate a quiz to attempt it</p>
                <button 
                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
                    onClick={() => window.location.href = '/generate'}
                >
                    Generate Quiz
                </button>
            </div>
        </div>
    );
    
    
}



