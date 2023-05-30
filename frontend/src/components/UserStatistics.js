// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  UserStatistics.js
//  A component that displays a statistics of logged user
// -----------------------------------------------------------

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserStatistics = () => {
    const [processesCount, setProcessesCount] = useState(0);
    const [recordsCount, setRecordsCount] = useState(0);

    useEffect(() => {
        axios.get('/api/user/statistics/')
            .then(response => {
                setProcessesCount(response.data.processes_count);
                setRecordsCount(response.data.records_count);
            })
            .catch(error => {
                console.log(error);
            });
    }, []);

    return (
        <div className="bg-gray-200 p-4 rounded-lg">
            <h2 className="text-2xl font-bold mb-4">User Statistics</h2>
            <div className="grid grid-cols-2 gap-4">
                <div className="bg-white p-4 ">
                    <h3 className="text-lg font-bold mb-2">Processes</h3>
                    <p className="text-3xl font-bold">{processesCount}</p>
                </div>
                <div className="bg-white p-4">
                    <h3 className="text-lg font-bold mb-2">Records</h3>
                    <p className="text-3xl font-bold">{recordsCount}</p>
                </div>
            </div>
        </div>
    );
}   

export default UserStatistics;