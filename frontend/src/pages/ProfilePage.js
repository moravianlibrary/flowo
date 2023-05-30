// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  ProfilePage.js
//  A page containing a password change form.
// -----------------------------------------------------------

import React, { useEffect, useContext } from 'react'
import AuthContext from "../context/AuthContext";
import ChangePasswordForm from "../components/ChangePasswordForm.js"
import axios from "axios"


const ProfilePage = () => {
  let {authTokens} = useContext(AuthContext)
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + String(authTokens.access);
  

  useEffect(() => {
  }, [])


    return (
      <div className="flex flex-col justify-center items-center my-5 gap-20">
        <ChangePasswordForm />
      </div>
    );
    
 }

export default ProfilePage;
