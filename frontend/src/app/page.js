"use client"
import Footer from "@/components/Footer.js";
import Navbar from "../components/Navbar.js";
import Image from "next/image.js";
import { useRouter } from 'next/navigation';
export default function Page() {
  const router = useRouter();

  const handleGetStartedClick = () => {
    router.push('/generate');
  };
  
  return (
    <div>
      <Navbar />
      <div className="container mx-auto mt-10">
        <h1 className="text-6xl font-bold text-center text-purple-800">Welcome to Quizly</h1>
        <p className="text-center mt-4 text-blue-600">Your comprehensive solution for creating and taking quizzes and tests.</p>
        
        <div className="mt-10">
          <h2 className="text-4xl font-bold text-center text-purple-800">Features</h2>
          <div className="flex flex-wrap justify-center mt-6 ">
            {[
              {
                src: "/generatequiz.png",
                title: "Generate Quizzes",
                description: "Effortlessly Generate multiple-choice quizzes with customizable settings using AI."
              },
              {
                src: "/generatequiz.png",
                title: "Attempt Quizzes",
                description: "Engage with quizzes created by others and receive detailed explanations for the answers."
              },
              {
                src: "/generatequiz.png",
                title: "Take Graded Assessments",
                description: "Participate in graded assessments to evaluate your knowledge and qualify."
              }
              
            ].map((feature, index) => (
              <div key={index} className="w-full md:w-1/3 p-4">
                <Image src={feature.src} width={200} height={200} alt={feature.title} className="w-full h-48 object-cover rounded-md" />
                <h3 className="text-xl font-bold text-center text-purple-800 mt-4">{feature.title}</h3>
                <p className="text-center text-blue-600 mt-2">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="flex justify-center mt-6">
        <button 
          className="bg-green-500 text-white px-4 py-2 rounded-md shadow-lg hover:bg-green-700 transition duration-300 ease-in-out transform hover:scale-105"
          onClick={handleGetStartedClick}
        >
          Get Started
        </button>        
      </div>
      <Footer />
    </div>
  );
}
