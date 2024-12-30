"use client"
import Logo from '@/components/logo';
import React, { useState } from 'react';

export default function GeneratePage(){
    const [files, setFiles] = useState([]);
    const [tags, setTags] = useState([]);
    const [tagInput, setTagInput] = useState('');
    const [numQuestions, setNumQuestions] = useState(5);
    const [difficulty, setDifficulty] = useState('easy');

    const handleFileChange = (e) => {
        setFiles([...e.target.files]);
    };

    const handleTagChange = (e) => {
        setTagInput(e.target.value);
    };

    const addTag = () => {
        if (tags.length < 5 && tagInput.trim() !== '') {
            setTags([...tags, tagInput.trim()]);
            setTagInput('');
        }
        if(tags.length === 5){
            alert("You can only add up to 5 tags")
        }
    };

    const removeTag = (index) => {
        setTags(tags.filter((_, i) => i !== index));
    };

    const handleSubmit = async (e) => {

        e.preventDefault();
        window.location.href = '/attempt/' + "sampleQuizId";
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));
        formData.append('tags', JSON.stringify(tags));
        formData.append('numQuestions', numQuestions);
        formData.append('difficulty', difficulty);

        try {
            const response = await fetch('YOUR_API_ENDPOINT', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            
            
            
            console.log('Success:', result);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            
            <Logo />
            <h1 className="text-4xl font-bold mb-6">Quiz Smarter, Learn Faster</h1>
            <div className="flex flex-row items-center mb-6">
                <form onSubmit={handleSubmit} className="w-full max-w-lg mr-6 ml-6">
                    <div className="mb-4">
                        <label htmlFor="fileUpload" className="block text-gray-700 text-lg">Upload your documents:</label>
                        <input
                            type="file"
                            id="fileUpload"
                            accept='.pdf'
                            multiple
                            onChange={handleFileChange}
                            className="mt-2 p-2 border border-gray-300 rounded w-full"
                        />
                    </div>
                    <div className="mb-4">
                        <label htmlFor="tagInput" className="block text-gray-700 text-lg">Add Tags:</label>
                        <div className="flex items-center mt-2">
                            <input
                                type="text"
                                id="tagInput"
                                value={tagInput}
                                onChange={handleTagChange}
                                className="p-2 border border-gray-300 rounded flex-grow"
                            />
                            <button
                                type="button"
                                onClick={addTag}
                                className="ml-2 p-2 bg-blue-500 text-white rounded"
                            >
                                Add Tags
                            </button>
                        </div>
                    </div>
                   
                    <div className="mb-4">
                        <label htmlFor="numQuestions" className="block text-gray-700 text-lg">Number of Questions:</label>
                        <select
                            id="numQuestions"
                            className="mt-2 p-2 border border-gray-300 rounded w-full"
                            onChange={(e) => setNumQuestions(e.target.value)}
                        >
                            {[5, 10, 15, 20].map((num) => (
                                <option key={num} value={num}>
                                    {num}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="mb-4">
                        <label className="block text-gray-700 text-lg">Difficulty:</label>
                        <div className="flex mt-2">
                            {['Easy', 'Medium', 'Hard'].map((level) => (
                                <label key={level} className="flex items-center mr-6">
                                    <input
                                        type="radio"
                                        name="difficulty"
                                        value={level.toLowerCase()}
                                        onChange={(e) => setDifficulty(e.target.value)}
                                        className=" mr-2 appearance-none border border-gray-300 rounded-full h-8 w-8 checked:bg-blue-500 checked:border-transparent focus:outline-none "
                                    />
                                    {level}
                                </label>
                            ))}
                        </div>
                    </div>
                    <button type="submit" className="p-2 bg-green-500 text-white rounded w-full">Generate my personal Quiz</button>
                </form>
                
                <div className="flex flex-col items-center w-1/2 h-max">
                    <div className="flex flex-col items-center w-1/2-auto h-1/2 bg-gray-200 p-4 rounded-lg shadow-md ml-6">
                        <h2 className="text-xl mb-4">How it works</h2>
                        <h3 className="text-lg mb-4">Add the single/multiple files and up to 5 topics you want to generate your quiz for (Leave empty if you want a quiz from the whole document), select difficulty and number of questions and you are good to go</h3>
                    </div>
                    <div>
                    <div className="flex flex-col items-center w-1/2-auto h-1/2 bg-gray-200 p-4 rounded-lg shadow-md mt-8">
                        <label htmlFor="tagInput" className="block text-gray-700 text-lg">My Quiz should focus on:</label>
                        <div className="mt-8">
                                <div className="flex flex-wrap">
                                    {tags.map((tag, index) => (
                                        <div key={index} className="flex items-center mb-2 mr-2">
                                            <span className="bg-gray-400 text-gray-700 p-2 rounded">{tag}</span>
                                            <button
                                                type="button"
                                                onClick={() => removeTag(index)}
                                                className="ml-2 p-2 bg-red-500 text-white rounded h-6 w-6 flex items-center justify-center"
                                            >
                                                X
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                        </div>
                </div>
            </div>
        </div>
    );
};