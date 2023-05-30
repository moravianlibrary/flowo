// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  DashboardPage.js
//  A page showing specific statistics about logged in user and for administrator
//    a information about all users.
//  Shows a list of records a logged in user owns and the history of his processes.
// -----------------------------------------------------------

import React, { useState, useEffect, useContext} from 'react'
import AuthContext from "../context/AuthContext";
import UserStatistics from '../components/UserStatistics';
import AdminStatistics from '../components/AdminStatistics';
import Table from "../components/Table"
import "../static/css/table.css";
import axios from "axios"


const API = "/api/user/records/";

const DashboardPage = () => {
  let {user} = useContext(AuthContext);
  let {authTokens} = useContext(AuthContext)
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + String(authTokens.access);
  const [data, setData] = useState([]);
  const [doneData, setDoneData] = useState([]);
  const headers = [
    { key: 'uuid', label: 'UUID', value: 'uuid' },
    { key: 'name', label: 'Name', value: 'name' },
    { key: 'datetime_updated', label: 'Updated', value: 'datetime_updated' },
    { key: 'process', label: 'Process', value: 'process' },
  ];



  const fetchData = async (url) => {
    try {
      const response = await axios.get(url);
      const data = response.data;
      if (data.length > 0) {
        setData(data);
        console.log(data);
      }
    } catch (error) {
      console.error(error);
    }
  }

  const fetchHistoryData = async (url) => {
    try {
      const response = await axios.get(url);
      const data = response.data;
      if (data.length > 0) {
        setDoneData(data);
        console.log(data);
      }
    } catch (error) {
      console.error(error);
    }
  }


  
  const handleButtonClick = async (uuid) => {
    try {
      let userid = user.user_id
      const res = await axios.post('/api/record/take/', { uuid, userid });
      console.log(res.data);
      window.location.reload(false)
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData(API);
    fetchHistoryData("/api/user/history/")
  }, [])


    return (
      <div className="flex flex-col justify-center items-center my-5 gap-20">
        <h1 className='font-bold text-4xl mt-20'>Hello {user.username}!</h1>
        <div className='flex flex-row gap-20 justify-center '>
          <div>
          <UserStatistics/>
          </div>
          {user.is_superuser && (
            <AdminStatistics/>
            )}
        </div>

        <div className='flex flex-row gap-20 justify-start w-4/5'>
          <div className="flex flex-col justify-start items-center w-full">
            <p>Your records</p>
            <div className="w-full">
              <Table data={data} headers={headers} handleButtonClick={handleButtonClick}/>
            </div>
          </div>
          <div className="flex flex-col justify-start items-center w-full">
            <p>Your history</p>
            <div className="w-full">
              <Table data={doneData} headers={headers} handleButtonClick={handleButtonClick}/>
            </div>
          </div>
        </div>

      </div>
    );
    
 }

export default DashboardPage;
