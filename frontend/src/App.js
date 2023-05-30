// -----------------------------------------------------------
//  Book Digitization Management System - bachelor's thesis
//
//  Lukas Vaclavek
//  xvacla32
//
//  App.js
//  A main routing for front-end.
//  Specifies which sites should not be available for not logged in users.
// -----------------------------------------------------------

import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import "./App.css";
import Header from "./components/Header";
import MainPage from "./pages/MainPage";
import LoginPage from "./pages/LoginPage";
import RecordPage from "./pages/RecordPage";
import PrivateRoute from "./utils/PrivateRoute";
import NewRecordPage from "./pages/NewRecordPage";
import CollectionsPage from "./pages/CollectionsPage";
import DashboardPage from "./pages/DashboardPage";
import ProfilePage from "./pages/ProfilePage";

function App() {
  const location = useLocation();

  return (
    <div>
      <AuthProvider>
        {location.pathname !== "/login" && <Header />}
        <Routes>
          <Route path="/" exact element={<PrivateRoute />}>
            <Route path="/" exact element={<MainPage />} />
            <Route path="/record/:recordId" element={<RecordPage />} />
            <Route path="/dashboard/" element={<DashboardPage />} />
            <Route path="/vc/" element={<CollectionsPage />} />
            <Route path="/profile/" element={<ProfilePage />} />
            <Route path="/records/new/" element={<NewRecordPage />} />
          </Route>
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </AuthProvider>
    </div>
  );
}

function AppWithRouter() {
  return (
    <Router>
      <App />
    </Router>
  );
}

export default AppWithRouter;
