import React from 'react';
import { Sidebar } from '../components/layout/Sidebar';
import { MobileNav } from '../components/layout/MobileNav';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';
import { Toast } from '../components/common/Toast';
import { useInterview } from '../context/InterviewContext';

export const MainLayout = ({ children }) => {
  const { toastMessage, setToastMessage } = useInterview();

  return (
    <div className="min-h-screen flex flex-col lg:flex-row bg-[#0b0f19] text-slate-100 font-sans">
      <Sidebar />
      <MobileNav />

      <div className="flex-1 flex flex-col min-w-0">
        <Navbar />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
          {children}
        </main>

        <Footer />
      </div>

      {toastMessage && (
        <Toast
          message={toastMessage.message}
          type={toastMessage.type}
          onClose={() => setToastMessage && setToastMessage(null)}
        />
      )}
    </div>
  );
};
