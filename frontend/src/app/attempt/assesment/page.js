"use client"

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export default function AssesmentPage() {
    const [formData, setFormData] = useState({
        name: '',
        studentId: '',
        email: '',
        contactNo: '',
        assesmentId: ''
    });
    const router = useRouter();

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
            
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const { name, email, contactNo, assesmentId } = formData;
        if (name && email && contactNo && assesmentId) {
            router.push(`/attempt/assesment/${assesmentId}`);
        }
    };

    const isValidContactNo = (contactNo) => {
        const regex = /^[0-9]{10}$/;
        return regex.test(contactNo);
    };

    return (
        <>
            <Navbar />
            <h1 className="text-4xl font-bold text-center  mb-3 mt-6">Enter your details</h1>
            <div className="flex flex-col items-center justify-center mt-10">
                <form onSubmit={handleSubmit} className="w-full max-w-sm">
                    <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleInputChange}
                        placeholder="Enter Name"
                        className="w-full px-4 py-2 mb-4 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <input
                        type="text"
                        name="studentId"
                        value={formData.studentId}
                        onChange={handleInputChange}
                        placeholder="Enter Student ID"
                        className="w-full px-4 py-2 mb-4 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        placeholder="Enter Email"
                        className="w-full px-4 py-2 mb-4 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <div className="relative">
                        <input
                            type="text"
                            name="contactNo"
                            value={formData.contactNo}
                            onChange={(e) => {
                                handleInputChange(e);
                            }}
                            placeholder="Enter Contact Number"
                            className="w-full px-4 py-2 mb-4 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        {!isValidContactNo(formData.contactNo)  && (
                            <></>
                        )}
                    </div>
                    <input
                        type="text"
                        name="assesmentId"
                        value={formData.assesmentId}
                        onChange={handleInputChange}
                        placeholder="Enter Assesment ID"
                        className="w-full px-4 py-2 mb-4 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button type="submit" className="w-full px-4 py-2 font-bold text-white bg-green-600 rounded hover:bg-blue-700">
                        Go to Assesment
                    </button>
                </form>
            </div>
            <Footer />
        </>
    );
};
