// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  ChangePasswordForm.js
//  A component for users password management
// -----------------------------------------------------------

import AuthContext from "../context/AuthContext";
import React, { useState, useContext } from 'react';
import axios from 'axios';

function ChangePasswordForm() {
let {authTokens} = useContext(AuthContext)
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageGreen, setGreenMessage] = useState('');
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + String(authTokens.access);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const response = await axios.post('/api/user/password/change/', {
        current_password: currentPassword,
        new_password: newPassword,
        confirm_password: confirmPassword,
        });
        if (response.data.message === 'Password changed successfully'){
            setGreenMessage(response.data.message);
            setMessage('');
        } else {
            setMessage(response.data.message);
            setGreenMessage('')
        }
    } catch (error) {
        setGreenMessage('')
        setMessage('An error occurred');
    }
  };

  return (
    <form className="flex flex-col justify-center max-w-md mx-auto my-8" onSubmit={handleSubmit}>
      <label className="block mb-2">
        Current password:
        <input
          className="block w-full border-gray-400 border rounded py-2 px-3 mt-1"
          type="password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
        />
      </label>
      <label className="block mb-2">
        New password:
        <input
          className="block w-full border-gray-400 border rounded py-2 px-3 mt-1"
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
      </label>
      <label className="block mb-2">
        Confirm new password:
        <input
          className="block w-full border-gray-400 border rounded py-2 px-3 mt-1"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </label>
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5" type="submit">
        Change password
      </button>
      {message && <p className="mt-2 text-red-500">{message}</p>}
      {messageGreen && <p className="mt-2 text-green-600">{messageGreen}</p>}
    </form>
  );
}

export default ChangePasswordForm;