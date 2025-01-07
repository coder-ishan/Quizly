'use client'
import React from 'react';
import { useState } from 'react';





export default function Question({ QuestionNo = 1, Question = '', Options = [], correctAnswer = '',ExplanationText = '' }) {
    
   
    const [solved, setSolved] = useState(false);
    const [correct,setCorrect] = useState(0);
    const [incorrect,setIncorrect] = useState(0);

    function handleSolving(index, correctAnswer) {
        setSolved(true);
        if (index === correctAnswer) {
            setCorrect(correct + 1);
            document.getElementById(`${QuestionNo}-${correctAnswer}`).style.backgroundColor = 'green';
        } else {
            setIncorrect(incorrect + 1);
            document.getElementById(`${QuestionNo}-${index}`).style.backgroundColor = 'red';
            document.getElementById(`${QuestionNo}-${correctAnswer}`).style.backgroundColor = 'green';
        }
    }
    
    
    return (
        <div>
            <div className="card flex flex-col lg:flex-row" style={{ marginBottom: '30px', padding: '20px' }}>
                <div className="lg:w-1/2">
                    <div className="card flex flex-row items-center bg-gray-100 shadow-lg rounded-xl w-full h-16-auto ml-4" style={{ marginBottom: '30px', padding: '20px' }}>
                        <div className="flex items-center justify-center bg-gray-100 h-16 w-16 rounded-md">{QuestionNo}.</div>
                        <div className='ml-4 flex items-center bg-white-200 h-full w-full overflow-y-auto text-ellipsis whitespace-normal' style={{ margin: '10px', padding: '20px', textAlign: 'center' }}>{Question}</div>
                    </div>
                    <div style={{ marginTop: '10px'}}>
                        {Options.map((option, index) => (
                            <div key={index} id={`${QuestionNo}-${index}`} className="card flex flex-row items-center bg-white shadow-lg rounded-xl w-full h-16 ml-4" style={{ marginTop: '10px', cursor: 'pointer', padding: '20px' }} onClick={() => solved==false ? handleSolving(index.toString(), correctAnswer) : ()=>{}}>
                                <div className="flex items-center justify-center bg-gray-200 h-8 w-8 rounded-md">{index + 1}</div>
                                <div className='ml-4 flex items-center justify-center bg-white-200 h-full w-96 break-words'  style={{ padding: '20px', textAlign: 'center' }}>{option}</div>
                            </div>
                        ))}
                    </div>
                </div>
                {solved && (
                    <div className="card flex flex-col items-center bg-white shadow-lg rounded-xl w-full lg:w-1/3 h-96 lg:h-auto ml-8" style={{ marginTop: '50px', padding: '20px' }}>
                        <div className="flex items-center justify-center bg-gray-100 h-20 w-full" style={{ padding: '30px' }}>Explanation</div>
                        <div className='ml-4 flex items-center justify-center bg-white-200 h-full w-full overflow-y-auto text-ellipsis whitespace-normal' style={{ margin: '10px', padding: '20px', textAlign: 'center' }}>{ExplanationText}</div>
                    </div>
                )}
            </div>
        </div>
    );
}
