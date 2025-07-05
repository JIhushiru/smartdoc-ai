import { useState } from 'react';
import { fetchStatus, triggerRetrain } from "../services/adminService";

export default function AdminPanel() {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState('');

    const handleFetchStatus = async () => {
    try {
        const data = await fetchStatus(token);
        setStatus(data);
    } catch (err) {
        alert("Failed to fetch status. Check your token.");
        setStatus(null);
    }
    };


    const handleRetrain = async () => {
      try {
        setLoading(true);
        const data = await triggerRetrain(token);
        alert(data.message);
        handleFetchStatus();
      } catch (err) {
        alert("Retrain failed. Check your token.");
      } finally {
        setLoading(false);
      }
    };


  return (
    <div className="max-w-xl mx-auto p-6 mt-10 bg-white shadow rounded-xl space-y-6">
      <h2 className="text-2xl font-bold">Admin Panel</h2>

      <input
        type="password"
        placeholder="Admin Token"
        className="w-full p-2 border rounded"
        value={token}
        onChange={(e) => setToken(e.target.value)}
      />

      <div className="flex gap-3">
        <button
          onClick={handleFetchStatus}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          Check Model Status
        </button>
        <button
          onClick={handleRetrain}
          disabled={loading}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
        >
          {loading ? "Retraining..." : "Trigger Retrain"}
        </button>
      </div>

      {status && (
        <div className="mt-4 bg-gray-50 border p-4 rounded">
          <p><strong>Feedback Entries:</strong> {status.count}</p>
          <p><strong>Last Feedback Time:</strong> {status.last_entry}</p>
        </div>
      )}
    </div>
  );
}
