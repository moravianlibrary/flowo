// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  VCchoiceBox.js
//  A component that displays a choice box for virtual collections and handles the selection and addition of them to records.
// -----------------------------------------------------------
import { useState } from 'react';

function VCchoiceBox(props) {
    const [selectedVirtualCollection, setSelectedVirtualCollection] = useState('');

    const handleVirtualCollectionChange = (event) => {
      setSelectedVirtualCollection(event.target.value);
    };

    const handleAddRecordToVC = () => {
      props.handleAddRecordToVC(selectedVirtualCollection, props.recordId);
    };
    
    const handleRemoveRecordFromVC = () => {
      props.handleRemoveRecordFromVC(selectedVirtualCollection, props.recordId);
    };
    

    return (
    <div className="flex flex-col items-center mt-8">
        <label htmlFor="virtual-collection" className="text-lg font-bold mb-2">
        Virtual Collection:
        </label>
        <select
        id="virtual-collection"
        name="virtual-collection"
        value={selectedVirtualCollection}
        onChange={handleVirtualCollectionChange}
        className="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        >
        <option value="">-- Select a Virtual Collection --</option>
        {props.virtualCollections.map(vc => (
            <option key={vc.vc_id} value={vc.vc_id}>{vc.name}</option>
        ))}
        </select>
        <div className='flex flex-row items-center gap-5'>
            <button onClick={handleAddRecordToVC} className="mt-4 py-2 px-4 border border-gray-400 rounded shadow hover:bg-gray-100 focus:outline-none focus:shadow-outline">
            Add to VC
            </button>
            <button onClick={handleRemoveRecordFromVC} className="mt-4 py-2 px-4 border border-gray-400 rounded shadow hover:bg-gray-100 focus:outline-none focus:shadow-outline">
            Remove from VC
            </button>
        </div>

    </div>
    );
  }


export default VCchoiceBox