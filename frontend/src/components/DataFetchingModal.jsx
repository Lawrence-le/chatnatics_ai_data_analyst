export default function DataFetchingModal({ columnsData }) {
  if (columnsData) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-2xl p-6 w-96 shadow-lg text-center space-y-4">
        <h2 className="text-lg font-semibold">Fetching Data</h2>

        {/* Spinner + Label */}
        <div className="flex items-center justify-center gap-2 text-blue-400">
          <svg
            className="w-5 h-5 animate-spin text-blue-400"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-100"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
          </svg>
          <span>Please wait a minute for server to boot...</span>
        </div>
      </div>
    </div>
  );
}
