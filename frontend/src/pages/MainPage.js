// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  MainPage.js
//  A main page showing all records in the database, allows to open records processes
//    and to tahe the ownership of the record.
// -----------------------------------------------------------

import React, { useState, useEffect, useContext} from 'react'
import AuthContext from "../context/AuthContext";
import "../static/css/table.css";
import Table from "../components/Table"
import axios from "axios"

const API = "/api/records/";

const MainPage = () => {
  let {user} = useContext(AuthContext);
  const [data, setData] = useState([]);
  const headers = [
    { key: 'uuid', label: 'UUID', value: 'uuid' },
    { key: 'name', label: 'Name', value: 'name' },
    { key: 'barcode', label: 'Barcode', value: 'barcode' },
    { key: 'datetime_created', label: 'Created', value: 'datetime_created' },
    { key: 'datetime_updated', label: 'Updated', value: 'datetime_updated' },
    { key: 'process', label: 'Process', value: 'process' },
    { key: 'state', label: 'State', value: 'state' },
    { key: 'user', label: 'User', value: 'user' },
  ];


  const fetchUsers = async (url) => {
      try {
          const res = await fetch(url);
          const data = await res.json();
          if (data.length > 0) {
              setData(data);
              console.log(data)
          }
      } catch (e) {
          console.error(e)
      }
  }

  useEffect(() => {
      fetchUsers(API);
  }, [])

    
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

    return (
      <div className="flex justify-center items-center my-5">
        <div className="w-full">
          <Table data={data} headers={headers} handleButtonClick={handleButtonClick}/>
        </div>
      </div>
    );
    
 }

export default MainPage;
