import React, { useState, useEffect } from 'react';

interface EnhancedImageDisplayProps {
  src: string;
  alt: string;
  className?: string;
  fallbackText?: string;
  aspectRatio?: 'square' | 'video' | 'wrestler';
  objectFit?: 'cover' | 'contain' | 'fill';
  smartPositioning?: boolean;
  onLoad?: () => void;
  onError?: () => void;
}

const EnhancedImageDisplay: React.FC<EnhancedImageDisplayProps> = ({
  src,
  alt,
  className = '',
  fallbackText,
  aspectRatio = 'square',
  objectFit = 'cover',
  smartPositioning = true,
  onLoad,
  onError
}) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [currentSrc, setCurrentSrc] = useState(src);

  useEffect(() => {
    setCurrentSrc(src);
    setImageLoaded(false);
    setImageError(false);
  }, [src]);

  const handleImageLoad = () => {
    setImageLoaded(true);
    setImageError(false);
    onLoad?.();
  };

  const handleImageError = () => {
    setImageError(true);
    onError?.();
  };

  const aspectRatioClasses = {
    square: 'aspect-square',
    video: 'aspect-video',
    wrestler: 'aspect-[4/5]'
  };

  const objectFitClasses = {
    cover: 'object-cover',
    contain: 'object-contain',
    fill: 'object-fill'
  };

  // If image failed to load, show fallback
  if (imageError || !src) {
    return (
      <div className={`${aspectRatioClasses[aspectRatio]} ${className} bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center`}>
        <span className="text-2xl font-bold text-white">
          {fallbackText || alt.charAt(0).toUpperCase()}
        </span>
      </div>
    );
  }

  return (
    <div className={`relative ${aspectRatioClasses[aspectRatio]} ${className} overflow-hidden`}>
      <img
        src={currentSrc}
        alt={alt}
        className={`w-full h-full ${objectFitClasses[objectFit]} transition-all duration-300 ${
          imageLoaded ? 'opacity-100 scale-100' : 'opacity-0 scale-105'
        }`}
        onLoad={handleImageLoad}
        onError={handleImageError}
        style={{
          objectPosition: smartPositioning ? 'center 20%' : 'center'
        }}
      />
      
      {/* Loading overlay */}
      {!imageLoaded && (
        <div className="absolute inset-0 bg-gray-800 flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
        </div>
      )}
    </div>
  );
};

export default EnhancedImageDisplay;
