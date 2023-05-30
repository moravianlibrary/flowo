// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  AdminStatistics.js
//  A component for displaying administration statistics of all users
// -----------------------------------------------------------
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminStatistics = () => {
  const [stats, setStats] = useState([]);

  useEffect(() => {
    axios.get('/api/admin/statistics/')
      .then(response => {
        setStats(response.data.stats);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div className="bg-gray-200 p-4 rounded-lg">
      <h2 className="text-2xl font-bold mb-4">All Users Statistics</h2>
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white p-4 ">
          <h3 className="text-lg font-bold mb-2">Username</h3>
        </div>
        <div className="bg-white p-4">
          <h3 className="text-lg font-bold mb-2">Processes</h3>
        </div>
        <div className="bg-white p-4">
          <h3 className="text-lg font-bold mb-2">Records</h3>
        </div>
        {stats.map(stat => (
          <React.Fragment key={stat.user}>
            <div className="bg-white p-4 ">
              <p className="text-lg font-bold mb-2">{stat.user}</p>
            </div>
            <div className="bg-white p-4">
              <p className="text-lg font-bold mb-2">{stat.processes_count}</p>
            </div>
            <div className="bg-white p-4">
              <p className="text-lg font-bold mb-2">{stat.records_count}</p>
            </div>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export default AdminStatistics;
