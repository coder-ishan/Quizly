import React from 'react';// Make sure to create this CSS file for styling

export default function Logo () {
    return (
        <nav className="logo">
            <div className="logo p-4 ">
                <img src="/logo/QuizlyLogo.svg" alt="Logo" style={{ height: '50px' }} />
            </div>
        </nav>
    );
};
