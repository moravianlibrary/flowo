// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  RecordPage.js
//  A page containing all steps of given record.
//  Here, users can modify and manage given record.
// -----------------------------------------------------------

import React, {useState, useEffect, useContext} from 'react'
import AuthContext from "../context/AuthContext";
import { Link, useParams } from 'react-router-dom';
import Checkbox from '../components/Checkbox.js'; 
import RecordTable from '../components/RecordTable.js';
import ChoiceList from '../components/ChoiceList.js';
import RecordDeleteButton from '../components/RecordDeleteButton.js';
import VCchoiceBox from '../components/VCchoiceBox';
import cx from 'classnames';
import NoteBox from '../components/NoteBox';
import axios from "axios"
import '../index.css'

const RecordPage = () => {
  const { recordId } = useParams();
  let [record, setRecord] = useState(null)
  const [virtualCollections, setVirtualCollections] = useState([]);
  const [selectedProfile, setSelectedProfile] = useState("");
  const [selectedDonator, setSelectedDonator] = useState("");
  const [importProfiles, setImportProfiles] = useState([]);
  const [donators, setDonators] = useState([]);
  let {authTokens} = useContext(AuthContext)
  let {user} = useContext(AuthContext)
  const [note, setNote] = useState(null);
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + String(authTokens.access);
  
  useEffect(() => {
    getRecord();
    getVCs();
    getImpProfiles();
    getDonators();
  }, [recordId]);
  

  let getRecord = async (record) => {
    let response = await fetch(`/api/records/${recordId}/`)
    let data = await response.json()
    setNote(data.note)
    console.log(data)
    setRecord(data)
  }

  let getVCs = async (record) => {
    let response = await fetch(`/api/vcs/`)
    let data = await response.json()
    setVirtualCollections(data)
  }

  let getImpProfiles = async (record) => {
    let response = await fetch(`/api/profiles/import/`)
    let data = await response.json()
    setImportProfiles(data)
  }

  let getDonators = async (record) => {
    let response = await fetch(`/api/donators/`)
    let data = await response.json()
    setDonators(data)
  }


  const [newDirPath, setNewDirPath] = useState('');
  const [warningLog, setWarning] = useState('');
  const [stateValue, setStateValue] = useState(null);
  const [OCRchecked, setOCRChecked] = useState(true);
  const [Imprepchecked, setImprepChecked] = useState(true);
  const [exportPolicy, setExportPolicy] = useState(true);
  const [Archivechecked, setArchiveChecked] = useState(true);
  const [KWISchecked, setKWISchecked] = useState(true);
  const [tableVisible, setTableVisible] = useState(false);
  const [selectedChoice, setSelectedChoice] = useState(null);

//Would be better to use differently, but MZK requested a specific order
  const choices = [
    { value: 'device:dc599747-1373-496f-8a79-fb43af41c95c', label: 'Scan master 0' },
    { value: 'device:0993dbf9-4b5b-4d71-9ceb-a7e7054a0199', label: 'ATIZ' },
    { value: 'device:14dc293f-6e7b-42d4-9d8e-8cf9d4bc96c8', label: 'Plustek' },
    { value: 'device:53077591-bc0f-4dec-bb89-73f41cc26067', label: 'Panasonic' },
  ];

  const isState0 = record?.process === 0 && record?.user === user?.username;
  const isState1 = record?.process === 1 && record?.user === user?.username;
  const isState2 = (record?.process === 2 || record?.process === 3) && record?.user === user?.username;
  const isState4 = record?.process === 4 && record?.user === user?.username;
  const isState5 = record?.process === 5 && record?.user === user?.username;
  const isState6 = record?.process === 6 && record?.user === user?.username;

  const handleSelect = (choice) => {
    setSelectedChoice(choice);
  };

  const handleTake = async (uuid) => {
    try {
      let userid = user.id
      const response = await axios.post('/api/record/take/', { uuid, userid });
      console.log(response.data);
      setRecord(response.data)
    } catch (error) {
      console.error(error);
    }
  };

  const handleLeave = async (uuid) => {
    try {
      let userid = user.id
      const response = await axios.post('/api/record/leave/', { uuid, userid });
      console.log(response.data);
      setRecord(response.data)
    } catch (error) {
      console.error(error);
    }
  };

  const handleNextStep = async (event) => {
    event.preventDefault();
    await axios.post('/api/record/state/change/', {
      'uuid': record?.uuid,
      'new_state': record?.process +1,
      'ocr_state': OCRchecked,
      'img_state': Imprepchecked,
      'archive': Archivechecked,
      'kwis': KWISchecked,
      'scanner': selectedChoice,
      'importProfile': selectedProfile,
      'note': note,
      'dirPath': newDirPath,
      'exportPolicy': exportPolicy,
      'donator': selectedDonator,
    }).then(response => {
      if (response.status >= 200 && response.status < 300) {
        if (response.data === 'NoScannerFound'){
          console.log("Error: ", response.data)
          setWarning("Please enter valid scanner")
        } else if(response.data === 'NoImportProfileFound'){
          console.log("Error: ", response.data)
          setWarning("Please enter valid import profile")
        } else {
          console.log(response.data)
          setWarning("")
          setRecord(response.data)
        }
      } else {
        console.error(`Request failed with HTTP status code ${response.status}`);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  const handleChangeStep = async (event) => {
    event.preventDefault();

    await axios.post('/api/admin/record/state/change/', {
      'uuid': record?.uuid,
      'new_state': stateValue,
      'ocr_state': OCRchecked,
      'img_state': Imprepchecked,
      'archive': Archivechecked,
      'kwis': KWISchecked,
      'scanner': selectedChoice,
      'importProfile': selectedProfile,
      'note': note,
      'dirPath': newDirPath,
      'exportPolicy': exportPolicy,
      'donator': selectedDonator,
    }).then(response => {
      if (response.status >= 200 && response.status < 300) {
        if (response.data === 'NoScannerFound'){
          console.log("Error: ", response.data)
          setWarning("Please enter valid scanner")
        } else if(response.data === 'NoImportProfileFound'){
          console.log("Error: ", response.data)
          setWarning("Please enter valid import profile")
        } else {
          console.log(response.data)
          setWarning("")
          setRecord(response.data)
        }
      } else {
        console.error(`Request failed with HTTP status code ${response.status}`);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  const handleRecordDelete = async () => {
    const uuid = record?.uuid
    const response = await axios.post('/api/record/delete/', { uuid });
    console.log(response.data)
    window.location.href = '/';
  }

  async function handleAddRecordToVC(selectedVirtualCollection, recordId) {
    if (selectedVirtualCollection) {
      try {
        const response = await axios.post('/api/vc/add/record/', { uuid: recordId, vc_id: selectedVirtualCollection});
        console.log(response.data);
        setRecord(response.data)
        alert('Record added to virtual collection successfully.');
      } catch (error) {
        console.log(error);
        alert(error.response.data.message);
      }
    }
  }
  
  async function handleRemoveRecordFromVC(selectedVirtualCollection, recordId) {
    if (selectedVirtualCollection) {
      try {
        const response = await axios.post('/api/vc/remove/record/', { uuid: recordId, vc_id: selectedVirtualCollection});
        console.log(response.data);
        setRecord(response.data)
        alert('Record removed from virtual collection successfully.');
      } catch (error) {
        console.log(error);
        alert(error.response.data.message);
      }
    }
  }

  const handleNoteValueChange = (newNoteValue) => {
    setNote(newNoteValue);
  };

  const handleChange = (event) => {
    setNewDirPath(event.target.value);
  };

  const handleStateChange = (event) => {
    setStateValue(event.target.value);
  };

  const handleOCRCheckboxChange = () => {
    setOCRChecked(!OCRchecked);
  };

  const handleImprepCheckboxChange = () => {
    setImprepChecked(!Imprepchecked);
  };

  const handleArchiveCheckboxChange = () => {
    setArchiveChecked(!Archivechecked);
  };

  const handleKWIScheckboxChange = () => {
    setKWISchecked(!KWISchecked);
  };


  function toggleTable() {
    setTableVisible(!tableVisible);
  }

  const handleExportPolicyChange = () => {
    setExportPolicy(!exportPolicy);
  };

  if (record === null) {
    return <p>Loading...</p>;
  }

  return (
    <div className="flex mt-20 flex-col items-center h-full gap-10">
        <div className='flex flex-row gap-2'>
          <p className='font-bold text-4xl'>Title: </p>        
          <p className="text-center text-4xl">{record?.name}</p>
        </div>
        <p className="text-center text-3xl">{record?.uuid}</p>
          {record?.user !== user?.username ?(
            <button
              className='bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded'
              onClick={() => handleTake(record?.uuid)}
            >
              Take
            </button>
          ) : 
          (
            <button
              className='bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded'
              onClick={() => handleLeave(record?.uuid)}
            >
              Leave
            </button>
          )
        }
        <VCchoiceBox virtualCollections={virtualCollections} recordId={record?.uuid} handleAddRecordToVC={handleAddRecordToVC} handleRemoveRecordFromVC={handleRemoveRecordFromVC} />
        <p className="text-center my-8 text-red-700 font-bold text-2xl">{warningLog}</p>
        <div className='flex flex-wrap justify-between gap-10 grow w-3/5'>
          <button onClick={toggleTable}>{tableVisible ? 'Hide data' : 'Show data'}</button>
          {tableVisible && record && <RecordTable record={record} />}
        </div>
        <div className='sm:w-2/3 md:w-2/3 lg:w-1/2 mx-auto h-48'>
          <NoteBox noteValue={note} onNoteValueChange={handleNoteValueChange}/>
        </div>

        
        <div className="flex flex-col items-center justify-center w-full">

        {record?.process >= 6 && (
          <div
              className={cx(
                'w-3/5 h-96 flex flex-col justify-evenly items-center rounded-lg my-5',
                {
                  'opacity-50 pointer-events-none': !isState6,
                  'bg-gray-200': !isState6,
                  'text-gray-400': !isState6,
                  'bg-blue-200': isState6,
                },
              )}>
              <p>ProArc Export</p>
              <div className='flex flex-col gap-5 justify-center items-center w-3/5'>
                <div className='w-1/4'>
                  <select value={selectedDonator}
                      onChange={(e) => setSelectedDonator(e.target.value)}
                      className='block appearance-none bg-gray-200 border w-full border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                      >
                      <option value="">Select a donator</option>
                      {donators.map((profile) => (
                        <option key={profile.value} value={profile.value}>{profile.name}</option>
                      ))}
                  </select>
                </div>
                  <Checkbox
                      onText=" Public"
                      offText=" Private"
                      checked={exportPolicy}
                      onChange={handleExportPolicyChange}
                    />
                  <div className='flex flex-row gap-10'>
                    <Checkbox
                      onText=" Archive"
                      offText=" Do not Archive"
                      checked={Archivechecked}
                      onChange={handleArchiveCheckboxChange}
                    />
                    <Checkbox
                      onText=" KWIS"
                      offText=" Do not KWIS"
                      checked={KWISchecked}
                      onChange={handleKWIScheckboxChange}
                    />
                  </div>
              </div>
                {
                record?.process === 6 ? <button type="submit" onClick={handleNextStep} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Export</button> : null
                }
            </div>
            
          )}

        {record?.process >= 5 && (
          <div
            className={cx(
              'w-3/5 h-64 flex flex-col justify-evenly items-center rounded-lg my-5',
              {
                'opacity-50 pointer-events-none': !isState5,
                'bg-gray-200': !isState5,
                'text-gray-400': !isState5,
                'bg-blue-200': isState5,
              },
            )}>
            <p>ProARC Metadata</p>
            <Link
            // TODO change in docker-compose
                to={'http://dk-proarc.infra.mzk.cz/api/#import:{"type":"EDIT_ITEMS","batch":"'+record?.batchId+'"}'}
                className="underline decoration-sky-500"
                target="_blank"
              >
              LINK TO PROARC
            </Link>
{/* 
            <div>
              <ChoiceBox options={options} onChoiceChange={handleChoiceChange} />
              <p>You selected: {selectedValue}</p>
            </div> */}

            {
            record?.process === 5 ? <button type="submit" onClick={handleNextStep} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Done</button> : null
            }
          </div>
        )}

        {record?.process >= 4 && (
          <div
            className={cx(
              'w-3/5 h-64 flex flex-col justify-evenly items-center rounded-lg my-5',
              {
                'opacity-50 pointer-events-none': !isState4,
                'bg-gray-200': !isState4,
                'text-gray-400': !isState4,
                'bg-blue-200': isState4,
              },
            )}>
            <p>ProARC Import</p>
            <select value={selectedProfile}
                    onChange={(e) => setSelectedProfile(e.target.value)}
                    className='block appearance-none w-1/4 bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                    >
              <option value="">Select an import profile</option>
              {importProfiles.map((profile) => (
                <option key={profile.value} value={profile.value}>{profile.name}</option>
              ))}
            </select>
            {record?.process === 4 && (
              <button type="submit" onClick={handleNextStep} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Import</button>
            )}
          </div>
        )}

        {record?.process >= 2 && (
          <div
            className={cx(
              'w-3/5 h-64 flex flex-col justify-evenly items-center rounded-lg my-5',
              {
                'opacity-50 pointer-events-none': !isState2,
                'bg-gray-200': !isState2,
                'text-gray-400': !isState2,
                'bg-blue-200': isState2,
              },
            )}>
            <p>ROPE</p>
              { record?.process === 2 && (
                <p>Process: Imgprep</p>
              )}
              { record?.process === 3 && (
                 <p>Process: Rope</p>
              )}
              
            <p>Progress: {record.progress}</p>
          </div>
        )}

        {record?.process >= 1 && (
          <div
            className={cx(
              'w-3/5 h-64 flex flex-col justify-evenly items-center rounded-lg my-5',
              {
                'opacity-50 pointer-events-none': !isState1,
                'bg-gray-200': !isState1,
                'text-gray-400': !isState1,
                'bg-blue-200': isState1,
              },
            )}>
            <p>Crop</p>
            <div className='flex flex-row gap-10 items-center justify-between h-2/5'>
            <form className="flex flex-row items-center">
              <label className="mr-2">Folder:</label>
              <input type="text" value={newDirPath} placeholder="Leave empty for default" onChange={handleChange} className="border border-gray-300 px-2 py-1 mr-2 rounded-md" />
            </form>

            </div>
            {
            record?.process === 1 ? <button type="submit" onClick={handleNextStep} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Done</button> : null
            }
          </div>
        )}

        {record?.process >= 0 && (
          <div
            className={cx(
              'w-3/5 h-96 mx-w-[40%] flex flex-col justify-evenly items-center rounded-lg my-5',
              {
                'opacity-50 pointer-events-none': !isState0,
                'bg-gray-200': !isState0,
                'text-gray-400': !isState0,
                'bg-blue-200': isState0,
              },
            )}>
            <p>Scanning</p>
            <div className='flex flex-row justify-center w-4/5'>
              <div className='flex flex-col justify-evenly gap-5'>
                <form className="flex flex-row items-center">
                  <label className="mr-2">Folder:</label>
                  <input type="text" value={newDirPath} placeholder="Leave empty for default" onChange={handleChange} className="border border-gray-300 px-2 py-1 mr-2 rounded-md" />
                </form>
                <div className='w-full'>
                  <label className="mr-2">Scanner:</label>
                  <ChoiceList choices={choices} onSelect={handleSelect} />
                </div>
               
              </div>


              <div className='flex flex-col justify-center items-center gap-5 lg:w-60 2xl:w-1/3'>
                <div className='flex flex-col gap-5 '>
                  <Checkbox
                    onText=" OCR"
                    offText=" Not OCR"
                    checked={OCRchecked}
                    onChange={handleOCRCheckboxChange}
                  />
                  <Checkbox
                    onText=" Imgprep"
                    offText=" Not Imageprep"
                    checked={Imprepchecked}
                    onChange={handleImprepCheckboxChange}
                  />
                </div>

              </div>



            </div>
          
            {
              record?.process === 0 ? <button type="submit" onClick={handleNextStep} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Done</button> : null
            }
          </div>
        )} 
        <div className='flex flex-row items-center gap-5 mb-5'>
          {user.is_superuser && (
          <form onSubmit={handleChangeStep} className="flex flex-row items-center">
              <label className="mr-2">Current state:</label>
              <input type="number" placeholder={record?.process} onChange={handleStateChange} className="w-20 border border-gray-300 px-2 py-1 mr-2 rounded-md" />
              <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Change</button>
          </form>
          )}
          {user.is_superuser && (
              <RecordDeleteButton onDelete={handleRecordDelete}/>
            )}
        </div>
        </div>

      
    </div>
  )
}

export default RecordPage