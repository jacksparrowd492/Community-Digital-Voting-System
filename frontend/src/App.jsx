import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './Navbar';
import UserDashboard from './UserDashboard';
import AdminDashboard from './AdminDashboard';
import { CheckCircle2, AlertCircle } from 'lucide-react';

function AppInner() {
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };


  return (
    <>
      {/* Global Toast */}
      {toast && (
        <div className={`toast-banner toast-${toast.type}`}>
          {toast.type === 'success'
            ? <CheckCircle2 size={16} />
            : <AlertCircle size={16} />}
          <span>{toast.message}</span>
        </div>
      )}

      <Navbar />

      <Routes>
        <Route
          path="/"
          element={<UserDashboard showToast={showToast} />}
        />
        <Route
          path="/admin"
          element={
            <AdminDashboard showToast={showToast} />
          }
        />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppInner />
    </BrowserRouter>
  );
}
