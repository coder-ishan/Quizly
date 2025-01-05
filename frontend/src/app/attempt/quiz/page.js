"use client"

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export default function QuizPage() {
            const [quizId, setQuizId] = useState('');
            const router = useRouter();

            const handleInputChange = (e) => {
                setQuizId(e.target.value);
            };

            const handleSubmit = (e) => {
                e.preventDefault();
                if (quizId) {
                    router.push(`/attempt/quiz/${quizId}`);
                }
            };
    return (
        <>
            <Navbar />
            <h1 className="text-4xl font-bold text-center mb-3 mt-6">Enter the Quiz Id of the quiz you want to attempt</h1>
            <div className="flex flex-col items-center justify-center mt-10">
                <form onSubmit={handleSubmit} className="w-full max-w-sm">
                    <input
                        type="text"
                        value={quizId}
                        onChange={handleInputChange}
                        placeholder="Enter Quiz ID"
                        className="w-full px-4 py-2 mb-4 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button type="submit" className="w-full px-4 py-2 font-bold text-white bg-green-600 rounded hover:bg-blue-700">
                        Go to Quiz
                    </button>
                </form>
            </div>
            <Footer />
        </>
    );
};

    

