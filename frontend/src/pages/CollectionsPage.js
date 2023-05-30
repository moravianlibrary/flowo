// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  CollectionsPage.js
//  A page showing all virtual collections
//  Has a functionality of downloading data from virtual collections
// -----------------------------------------------------------
import React, { useState, useEffect} from 'react'
import "../static/css/table.css";
import VCtable from '../components/VCtable';

const API = "/api/vcs/";

const CollectionsPage = () => {
  const [data, setData] = useState([]);
  const headers = [
    { key: 'id', label: 'ID', value: 'vc_id' },
    { key: 'name', label: 'Name', value: 'name' },
    { key: 'record_count', label: 'Records', value: 'record_count' },
    { key: 'button', label: 'Action', value: 'button' },
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

    return (
      <div className="flex justify-center items-center my-5">
        <div className="w-full">
          <VCtable data={data} headers={headers}/>
        </div>
      </div>
    );
    
 }

export default CollectionsPage;
