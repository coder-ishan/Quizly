import React from 'react';// Make sure to create this CSS file for styling
import Image from 'next/image';

export default function Navbar () {
    return (
            <nav className="p-4">
        <div className="flex justify-between items-center">
        <div className="logo p-4 ">
                <Image src="/logo/QuizlyLogo.svg" href ="/" alt="Logo" height = {100} width ={150}/>
            </div>
          <div className="space-x-4">
            <a href="/" className="text-blue-600 hover:text-green-600">Home</a>
            <a href="/generate" className="text-blue-600 hover:text-green-600">Generate</a>
            <a href="/attempt/quiz" className="text-blue-600 hover:text-green-300">Quiz</a>
            <a href="/attempt/assesment" className="text-blue-600 hover:text-green-300">Assesments</a>
            <a href="#" className="text-blue-600 hover:text-green-300">About</a>
           
          </div>
        </div>
      </nav>
    );
};
