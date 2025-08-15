import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: 'primary' | 'secondary' | 'white';
  text?: string;
  className?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  size = 'md', 
  color = 'primary', 
  text,
  className = '' 
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  const colorClasses = {
    primary: 'border-purple-500',
    secondary: 'border-blue-500',
    white: 'border-white'
  };

  return (
    <div className={`flex flex-col items-center justify-center ${className}`}>
      <div className={`${sizeClasses[size]} animate-spin rounded-full border-2 border-t-transparent ${colorClasses[color]}`}></div>
      {text && (
        <p className={`mt-3 text-sm font-medium ${
          color === 'white' ? 'text-white' : 'text-gray-400'
        }`}>
          {text}
        </p>
      )}
    </div>
  );
};

export default LoadingSpinner;
