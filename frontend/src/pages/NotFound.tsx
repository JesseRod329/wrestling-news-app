import React from 'react';
import { Link } from 'react-router-dom';

const NotFound: React.FC = () => {
  return (
    <div className="bg-[#171212] min-h-screen text-white flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-4">404 - Not Found</h1>
      <p className="mb-8">Sorry, the page you are looking for does not exist.</p>
      <Link to="/" className="text-cyan-400">Go back to the homepage</Link>
    </div>
  );
};

export default NotFound; 