import { useState } from 'react';
import SmartDocClassifier from "./components/SmartDocClassifier";
import AdminPanel from "./components/AdminPanel";
import './App.css';

function App() {
  const [showAdminPanel, setShowAdminPanel] = useState(false);

  return (
    <div className="relative space-y-10">
      {/* Admin Panel Button - Upper Right */}
      {!showAdminPanel && (
        <div className="absolute top-4 right-4 z-10">
          <button
            onClick={() => setShowAdminPanel(true)}
            className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg font-medium transition-colors shadow-md"
          >
            Admin
          </button>
        </div>
      )}

      {!showAdminPanel ? (
        <SmartDocClassifier/>
      ) : (
        <AdminPanel onBack={() => setShowAdminPanel(false)} />
      )}
    </div>
  );
}

export default App;