// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  ChoiceList.js
//  A component for displaying and selecting from a choice list
// -----------------------------------------------------------

import React, { useState } from 'react';

const ChoiceList = ({ choices, onSelect }) => {
  const [selectedChoice, setSelectedChoice] = useState('');

  const handleSelect = (choice) => {
    setSelectedChoice(choice);
    onSelect(choice);
  };

  return (
    <div className="inline-block relative">
      <select
        className="block appearance-none bg-white border border-gray-300 hover:border-gray-400 w-80 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline"
        value={selectedChoice}
        onChange={(e) => handleSelect(e.target.value)}
      >
        <option value="" disabled>Select an option</option>
        {choices.map((choice) => (
          <option key={choice.value} value={choice.value}>
            {choice.label}
          </option>
        ))}
      </select>
      <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
        <svg
          className="fill-current h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M14.95 7.95a1 1 0 01-1.41 0L10 4.91 6.46 8.46a1 1 0 01-1.41-1.41l4.24-4.24a1 1 0 011.41 0l4.24 4.24a1 1 0 010 1.41z"
            clipRule="evenodd"
          />
        </svg>
      </div>
    </div>
  );
};

export default ChoiceList;
