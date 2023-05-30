// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  Checkbox.js
//  A component for creating a checkbox and setting its value to a variable
// -----------------------------------------------------------
import React from 'react';

function Checkbox(props) {
  const { checked, onChange, onText, offText } = props;

  const handleChange = () => {
    onChange();
  };

  return (
    <div>
      <label>
        <input
          type="checkbox"
          checked={checked}
          onChange={handleChange}
        />
        {checked ? onText : offText}
      </label>
    </div>
  );
};

export default Checkbox;
