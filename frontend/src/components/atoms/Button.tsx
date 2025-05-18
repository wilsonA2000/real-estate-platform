'use client';

import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  disabled = false,
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`px-4 py-2 rounded font-medium transition-colors ${
        variant === 'primary'
          ? 'bg-primary text-white hover:bg-blue-600'
          : 'bg-gray-200 text-secondary hover:bg-gray-300'
      } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      {children}
    </button>
  );
};