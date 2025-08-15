import React from 'react';
import { Link } from 'react-router-dom';

interface WrestlerAvatarProps {
  id: string;
  img: string;
}

const WrestlerAvatar: React.FC<WrestlerAvatarProps> = ({ id, img }) => {
  return (
    <Link to={`/wrestlers/${id}`} className="flex h-full flex-1 flex-col gap-4 text-center rounded-lg min-w-32 pt-4">
      <div
        className="bg-center bg-no-repeat aspect-square bg-cover rounded-full flex flex-col self-center w-full"
        style={{ backgroundImage: `url("${img}")` }}
      ></div>
    </Link>
  );
};

export default WrestlerAvatar; 