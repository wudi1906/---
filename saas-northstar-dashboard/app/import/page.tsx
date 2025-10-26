'use client'

import { useState } from 'react'

export default function ImportPage() {
  const [uploading, setUploading] = useState(false)
  const [files, setFiles] = useState<{
    subscriptions?: File
    churn?: File
    acquisition?: File
  }>({})

  const handleFileChange = (type: 'subscriptions' | 'churn' | 'acquisition', file: File | null) => {
    if (file) {
      setFiles(prev => ({ ...prev, [type]: file }))
    }
  }

  const handleUpload = async () => {
    setUploading(true)
    // Simulate upload
    await new Promise(resolve => setTimeout(resolve, 2000))
    setUploading(false)
    alert('CSV files uploaded successfully!')
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Import CSV Data
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Upload your subscription, churn, and acquisition data
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-8">
          <div className="space-y-6">
            {/* Subscriptions */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                📊 Subscriptions Data
              </label>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => handleFileChange('subscriptions', e.target.files?.[0] || null)}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-lg file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100
                  dark:file:bg-blue-900 dark:file:text-blue-300"
              />
              <p className="mt-2 text-xs text-gray-500">
                Format: date, customer_id, plan, amount, currency
              </p>
            </div>

            {/* Churn */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                📉 Churn Data
              </label>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => handleFileChange('churn', e.target.files?.[0] || null)}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-lg file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100
                  dark:file:bg-blue-900 dark:file:text-blue-300"
              />
              <p className="mt-2 text-xs text-gray-500">
                Format: date, customer_id, reason
              </p>
            </div>

            {/* Acquisition */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                📈 Acquisition Data
              </label>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => handleFileChange('acquisition', e.target.files?.[0] || null)}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-lg file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100
                  dark:file:bg-blue-900 dark:file:text-blue-300"
              />
              <p className="mt-2 text-xs text-gray-500">
                Format: date, channel, cost, customers
              </p>
            </div>
          </div>

          <div className="mt-8 flex gap-4">
            <button
              onClick={handleUpload}
              disabled={uploading || Object.keys(files).length === 0}
              className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-colors ${
                uploading || Object.keys(files).length === 0
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              {uploading ? 'Uploading...' : 'Upload Files'}
            </button>
            <a
              href="/"
              className="px-6 py-3 rounded-lg font-semibold bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
            >
              Cancel
            </a>
          </div>
        </div>

        <div className="mt-8 bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
            📝 Sample Data Format
          </h3>
          <div className="space-y-4 text-sm">
            <div>
              <strong className="text-blue-900 dark:text-blue-100">subscriptions.csv:</strong>
              <pre className="mt-1 p-3 bg-white dark:bg-gray-800 rounded text-xs overflow-x-auto">
{`date,customer_id,plan,amount,currency
2024-01-01,C001,Pro,99,USD
2024-01-01,C002,Basic,29,USD`}
              </pre>
            </div>
            <div>
              <strong className="text-blue-900 dark:text-blue-100">churn.csv:</strong>
              <pre className="mt-1 p-3 bg-white dark:bg-gray-800 rounded text-xs overflow-x-auto">
{`date,customer_id,reason
2024-01-15,C003,price
2024-01-20,C004,feature`}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

