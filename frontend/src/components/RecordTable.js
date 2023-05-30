// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  RecordTable.js
//  A component of simple table displaying a records data
// -----------------------------------------------------------

import React from 'react';
function RecordTable({ record }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Field</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>UUID</td>
          <td>{record.uuid}</td>
        </tr>
        <tr>
          <td>Barcode</td>
          <td>{record.barcode}</td>
        </tr>
        <tr>
          <td>Name</td>
          <td>{record.name}</td>
        </tr>
        <tr>
          <td>Created</td>
          <td>{record.datetime_created}</td>
        </tr>
        <tr>
          <td>Updated</td>
          <td>{record.datetime_updated}</td>
        </tr>
        <tr>
          <td>Process</td>
          <td>{record.process}</td>
        </tr>
        <tr>
          <td>VC</td>
          <td>{record.vc}</td>
        </tr>
        <tr>
          <td>OCR</td>
          <td>{record.ocr}</td>
        </tr>
        <tr>
          <td>Imprep</td>
          <td>{record.imprep}</td>
        </tr>
        <tr>
          <td>State</td>
          <td>{record.state}</td>
        </tr>
        <tr>
          <td>User</td>
          <td>{record.user}</td>
        </tr>
        <tr>
          <td>Note</td>
          <td>{record.note}</td>
        </tr>
        <tr>
          <td>Directory</td>
          <td>{record.directory}</td>
        </tr>
        <tr>
          <td>BatchID</td>
          <td>{record.batchId}</td>
        </tr>
      </tbody>
    </table>
  );
}

export default RecordTable;
