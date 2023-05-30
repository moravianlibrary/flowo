// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  VCtable.js
//  A component rendering a table of all virtual collections.
//  Includes button for clearing a virtual collection.
//  Collections can be downloaded by clicking at the collection id
// -----------------------------------------------------------

import React, {useState, useContext} from 'react'
import axios from "axios"
import AuthContext from "../context/AuthContext";

const VCtable = ({ data, headers}) => {
    let {user} = useContext(AuthContext)
    let {authTokens} = useContext(AuthContext)
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + String(authTokens.access);
    const [sortBy, setSortBy] = useState(null);
    const [warningLog, setWarning] = useState('');
    const [sortOrder, setSortOrder] = useState(null);

    const handleSort = (column) => {
        if (sortBy === column) {
        setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
        } else {
        setSortBy(column);
        setSortOrder('asc');
        }
    };

    const handleDownload = async (virtualCollectionId) => {
        try {
          const response = await axios.get(`/api/vc/${virtualCollectionId}/`, {
            responseType: 'blob',
          });
          if (response.data === 'No records found for given virtual collection'){
            setWarning("Please enter valid scanner")
          } else {
            setWarning("")
            const filename = response.headers['content-disposition'].split('filename=')[1];
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }
        } catch (error) {
          console.error(error);
        }
      };

      const handleClear = async (value) => {
        await axios.post('/api/vc/clear/all/', {
          'vc_id': value
        }).then(response => {
            console.log(response)
        })
        .catch(error => {
          console.error('Error:', error);
        });
      }
    const sortedData = data.slice().sort((a, b) => {
    if (sortOrder === 'asc') {
        return a[sortBy] > b[sortBy] ? 1 : -1;
    } else if (sortOrder === 'desc') {
        return a[sortBy] < b[sortBy] ? 1 : -1;
    }
    return 0;
    });

    return (
    <div>
        <table>
            <thead>
            <tr>
                {headers.map((header) => (
                <th key={header.key} onClick={() => handleSort(header.value)}>
                    {header.label}{' '}
                    {sortBy === header.value && (sortOrder === 'asc' ? '▲' : '▼')}
                </th>
                ))}
            </tr>
            </thead>
            <tbody>
                {sortedData.map((row, index) => (
                    <tr key={index} className="odd:bg-blue-100 hover:bg-gray-200">
                        {headers.map((header) => (
                        <td key={header.key}>
                            {
                            header.value === 'button' ? (
                                user.is_superuser ? (
                                    <button
                                    onClick={() => (handleClear(row[headers[0].value])) }
                                    className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-2xl font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto"
                                >
                                    Clear
                                </button>
                                    ) : (<p>Only admin is allowed to clear VC</p>)
                            ) : header.value === 'vc_id' ? (
                                <button
                                className="underline decoration-sky-500"
                                onClick={() => handleDownload(row['vc_id'])}
                            >
                                {row[header.value]}
                            </button>
                            ) : (
                            row[header.value]
                            )}
                        </td>
                        ))}
                        </tr>
                ))}
            </tbody>
        </table>
        <p className="text-center my-8 text-red-700 font-bold text-2xl">{warningLog}</p>
    </div>
    );
};

export default VCtable;

