import { FC, ReactNode } from 'react';

interface CardProps {
  children: ReactNode;       // Defines 'children' as any valid React child
  bg?: string;               // 'bg' is optional and defaults to a string
}

const Card: FC<CardProps> = ({ children, bg = 'bg-gray-100' }) => {
  return (
    <div className={`${bg} p-6 rounded-lg shadow-md`}>
      {children}
    </div>
  );
};

export default Card;