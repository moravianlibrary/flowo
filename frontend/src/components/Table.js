// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  Table.js
//  A component for displaying and managing all records on the main page and dashboard.
//  Allows a functionality to sord the tables data and paging
// -----------------------------------------------------------

import React, {useState} from 'react'
import { Link } from 'react-router-dom';

const Table = ({ data, headers, handleButtonClick }) => {
  const [sortBy, setSortBy] = useState("datetime_updated");
  const [sortOrder, setSortOrder] = useState("desc");
  const [currentPage, setCurrentPage] = useState(1);
  const recordsPerPage = 20;

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
    console.log(sortBy);
    console.log(sortOrder);
  };

  const sortedData = data.slice().sort((a, b) => {
    if (sortOrder === 'asc') {
      return a[sortBy] > b[sortBy] ? 1 : -1;
    } else if (sortOrder === 'desc') {
      return a[sortBy] < b[sortBy] ? 1 : -1;
    }
    return 0;
  });


  const totalPages = Math.ceil(sortedData.length / recordsPerPage);

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
          {sortedData
            .slice((currentPage - 1) * recordsPerPage, currentPage * recordsPerPage)
            .map((row, index) => (
              <tr key={index} className="odd:bg-blue-100 hover:bg-gray-200">
                {/* table data */}
                {headers.map((header) => (
                  <td key={header.key}>
                    {row[header.value] === null && header.value === 'user' && row['process'] !== 'Archive' ? (
                      <button
                        className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mr-5"
                        onClick={() => handleButtonClick(row['uuid'])}
                      >
                        Take
                      </button>
                    ) : null}
                    {header.value === 'uuid' ? (
                      <Link
                        to={`/record/${row[header.value]}`}
                        className="underline decoration-sky-500"
                      >
                        {row[header.value]}
                      </Link>
                    ) : (
                      row[header.value]
                    )}
                  </td>
                ))}
              </tr>
            ))}
        </tbody>
      </table>
      <div className="text-gray-600 text-center pt-5">
          Page {currentPage} of {totalPages}
        </div>
      <div className="flex justify-center gap-5 mt-5">
        <button 
          className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
          onClick={() => setCurrentPage(currentPage - 1)}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <button 
          className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
          onClick={() => setCurrentPage(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default Table;
