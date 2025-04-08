//DataFetchingModal.jsx

export default function DataFetchingModal({ columnsData }) {
  if (columnsData) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-2xl p-6 w-96 shadow-lg text-center">
        <h2 className="text-lg font-semibold mb-2">Fetching Data</h2>
        <p className="text-gray-700">Please wait for server to boot...</p>
      </div>
    </div>
  );
}
