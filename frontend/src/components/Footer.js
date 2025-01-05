export default function Footer(){
return(
    <footer className="bg-gray-900 text-white mt-48 p-6 text-center w-full m-0">
        <div className="flex justify-center space-x-6 mt-6">
            <a href="/about" className="text-gray-400 hover:text-white transition duration-300">About Us</a>
            <a href="/contact" className="text-gray-400 hover:text-white transition duration-300">Contact</a>
            <a href="/privacy" className="text-gray-400 hover:text-white transition duration-300">Privacy Policy</a>
            <a href="/terms" className="text-gray-400 hover:text-white transition duration-300">Terms of Service</a>
        </div>
      
        <p className="mt-6 text-gray-500">&copy; 2025 Quizly. All rights reserved.</p>
    </footer>
);
}
