// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  NoteBox.js
//  A component for displaying and managing notes of a given record
// -----------------------------------------------------------

import { useState, useEffect } from 'react';


function NoteBox({ noteValue, onNoteValueChange }) {
  const [note, setNote] = useState(noteValue);

  useEffect(() => {
    setNote(noteValue);
  }, [noteValue]);

  const handleNoteChange = (event) => {
    const newNoteValue = event.target.value;
    setNote(newNoteValue);
    onNoteValueChange(newNoteValue);
  };

  return (
    <div className="bg-blue-200 rounded-lg shadow-md p-4 h-full">
        <textarea
        placeholder="This is an area for the notes"
        className="bg-white rounded-lg shadow-md h-full w-full overflow-y-scroll resize-none"
        value={note}
        onChange={handleNoteChange}
        />
    </div>
  );
}

export default NoteBox;