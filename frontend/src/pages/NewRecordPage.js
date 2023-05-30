// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  NewRecordPage.js
//  A page allowing user to browse a catalogue for a barcode of documents.
//  After selecting the right document, user can create a new record.
// -----------------------------------------------------------
import { useState, useContext } from "react";
import AuthContext from "../context/AuthContext";
import axios from "axios";


const NewRecordPage = () => {
    const [barcode, setQuery] = useState("");
    // const titles = null;
    const [data, setData] = useState([]);
    let [record, setRecord] = useState(null)
    let {authTokens} = useContext(AuthContext)
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + String(authTokens.access);

    const handleInputChange = (event) => {
      setQuery(event.target.value);
    };
  
    const handleSearch = async (event) => {
      event.preventDefault();
      const response = await axios.post("/api/record/search/", { barcode });
      console.log(response.data);
      setData(Array.isArray(response.data) ? response.data : [response.data]);

    };


    const handleSelect = async (value) => {
      const reqBarcode = {'barcode': value.barcode};
      console.log(JSON.stringify(reqBarcode));

      const response = await axios.post("/api/record/new/", JSON.stringify(reqBarcode) );

      console.log(response.data);
      setRecord(response.data)
    };
  
    const filteredData = data.filter((item) => item.title !== "");
    return (
      <div className="flex flex-col justify-center items-center my-52">
        <form onSubmit={handleSearch} className="w-2/5">
          <div className="flex items-center border-b-2 border-blue-500 py-3 w-full">
            <input
              className="appearance-none bg-transparent border-none w-full text-blue-500 mr-3 py-3 px-10 leading-tight focus:outline-none"
              type="text"
              placeholder="Enter barcode..."
              value={barcode}
              onChange={handleInputChange}
            />
            <button
              className="flex-shrink-0 bg-blue-500 hover:bg-blue-700 border-blue-500 hover:border-blue-700 text-md text-white py-3 px-4 rounded"
              type="submit"
            >
              Search
            </button>
          </div>
        </form>
        {record?.uuid &&(
          <div className="my-52">
            <h1 className="font-bold">Created: {record?.uuid}</h1>
          </div>
        )} 
        <div className="my-52 flex flex-row items-center gap-10">
        {/* <p className="text-center my-8 text-3xl font-bold">{record?.uuid}</p> */}
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Barcode</th>
              <th>Select</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.map((item, index) => (
              <tr key={index}>
                <td>{item.title}</td>
                <td>{item.barcode}</td>
                <td>
                  <button
                    onClick={() => handleSelect(item)}
                    className="flex-shrink-0 bg-blue-500 hover:bg-blue-700 border-blue-500 hover:border-blue-700 text-md text-white py-3 px-4 rounded"
                  >
                    Choose
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
      </div>
    );
  }

export default NewRecordPage