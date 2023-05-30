// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  Header.js
//  A Header component that is being displayed on every page instead of the login page
// -----------------------------------------------------------
import React, { useContext, useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import logo from "../static/images/flowo.png";
import avatar from "../static/images/avatar.png";
import "../static/css/styles.css";
import AuthContext from "../context/AuthContext";

function Header() {
  const { user, logoutUser } = useContext(AuthContext);
  const location = useLocation();
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    // use an object with pathname keys to corresponding indexes
    const indexMap = {
      "/dashboard/": 0,
      "/": 1,
      "/vc": 2,
    };
    setActiveIndex(indexMap[location.pathname] || 0);
    // set default value to 0 when location.pathname not found in indexMap
  }, [location.pathname]);

  const handleItemClick = (index) => {
    setActiveIndex(index);
  };

  return (
    <header className="header">
      <Link to="/">
        <img className="logo" src={logo} alt="flowo.com" />
      </Link>
      <nav className="nav flex grow ml-96 justify-center">
        <ul className="nav-list">
          <li
            className={`nav-item ${activeIndex === 0 ? "active" : ""}`}
            onClick={() => handleItemClick(0)}
          >
            <Link to="/dashboard/">Dashboard</Link>
          </li>
          <li
            className={`nav-item ${activeIndex === 1 ? "active" : ""}`}
            onClick={() => handleItemClick(1)}
          >
            <Link to="/">Records</Link>
          </li>
          <li
            className={`nav-item ${activeIndex === 2 ? "active" : ""}`}
            onClick={() => handleItemClick(2)}
          >
            <Link to="/vc">Collections</Link>
          </li>
        </ul>
      </nav>
      <div className="profile">
        <Link
          to="/records/new/"
          className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mr-5"
        >
          New Record
        </Link>
        {user && (
          <div className="flex flex-row gap-5">
            <Link to="/profile" title="Profile settings">
              <div className="flex flex-row justify-items-end">
                <img className="avatar" src={avatar} alt="Profile" />
                <span className="name hover:text-blue-700 ">{user.username}</span>
              </div>
            </Link>
            <button
              onClick={logoutUser}
              className="text-black hover:text-blue-700 font-bold rounded focus:outline-none cursor-pointer"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
}

export default Header;
