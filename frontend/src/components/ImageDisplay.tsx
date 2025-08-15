import React, { useState } from 'react';

interface ImageDisplayProps {
  src: string;
  alt: string;
  className?: string;
  fallbackText?: string;
  aspectRatio?: 'video' | 'square' | 'portrait';
  objectFit?: 'cover' | 'contain' | 'fill';
  objectPosition?: 'center' | 'top' | 'bottom' | 'left' | 'right';
}

const ImageDisplay: React.FC<ImageDisplayProps> = ({
  src,
  alt,
  className = '',
  fallbackText = '',
  aspectRatio = 'video',
  objectFit = 'cover',
  objectPosition = 'center'
}) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const aspectRatioClasses = {
    video: 'aspect-video',
    square: 'aspect-square',
    portrait: 'aspect-[4/5]'
  };

  const objectFitClasses = {
    cover: 'object-cover',
    contain: 'object-contain',
    fill: 'object-fill'
  };

  const objectPositionClasses = {
    center: 'object-center',
    top: 'object-top',
    bottom: 'object-bottom',
    left: 'object-left',
    right: 'object-right'
  };

  const handleImageLoad = () => {
    setImageLoaded(true);
    setImageError(false);
  };

  const handleImageError = () => {
    setImageError(true);
    setImageLoaded(false);
  };

  return (
    <div
      className={`relative overflow-hidden rounded-xl bg-[#382929] ${aspectRatioClasses[aspectRatio]} ${className}`}
    >
      {/* Background fallback */}
      <div
        className="absolute inset-0 bg-center bg-no-repeat bg-cover"
        style={{
          backgroundImage: `url("${src}")`,
          backgroundPosition: 'center center',
          backgroundSize: 'cover'
        }}
      />

      {/* Main image with better control */}
      <img
        src={src}
        alt={alt}
        className={`absolute inset-0 w-full h-full transition-opacity duration-300 ${
          imageLoaded ? 'opacity-100' : 'opacity-0'
        } ${objectFitClasses[objectFit]} ${objectPositionClasses[objectPosition]}`}
        onLoad={handleImageLoad}
        onError={handleImageError}
        loading="lazy"
      />

      {/* Loading state */}
      {!imageLoaded && !imageError && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#e9242a]"></div>
        </div>
      )}

      {/* Error state with fallback text */}
      {imageError && (
        <div className="absolute inset-0 flex items-center justify-center text-[#b89d9e] text-sm">
          {fallbackText || alt.charAt(0)}
        </div>
      )}
    </div>
  );
};

export default ImageDisplay;
