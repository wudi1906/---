'use client'

import { useEffect, useMemo, useState } from 'react'
import Papa from 'papaparse'

type DatasetType = 'subscriptions' | 'churn' | 'acquisition'

interface PreviewData {
  headers: string[]
  rows: string[][]
}

const DATASET_LABELS: Record<DatasetType, string> = {
  subscriptions: 'Subscriptions',
  churn: 'Churn',
  acquisition: 'Acquisition',
}

const DATASET_ORDER: DatasetType[] = ['subscriptions', 'churn', 'acquisition']
const PAGE_SIZE = 5

export default function ImportPage() {
  const [uploading, setUploading] = useState(false)
  const [files, setFiles] = useState<{
    subscriptions?: File
    churn?: File
    acquisition?: File
  }>({})
  const [previews, setPreviews] = useState<Record<DatasetType, PreviewData | undefined>>({
    subscriptions: undefined,
    churn: undefined,
    acquisition: undefined,
  })
  const [activeDataset, setActiveDataset] = useState<DatasetType | null>(null)
  const [page, setPage] = useState(0)
  const [parseError, setParseError] = useState<string | null>(null)

  const handleFileChange = (type: 'subscriptions' | 'churn' | 'acquisition', file: File | null) => {
    if (file) {
      setFiles(prev => ({ ...prev, [type]: file }))
      Papa.parse<Record<string, unknown>>(file, {
        header: true,
        skipEmptyLines: true,
        complete: (result) => {
          const headers = (result.meta.fields && result.meta.fields.length > 0)
            ? result.meta.fields
            : Object.keys(result.data?.[0] ?? {})

          const rows = (Array.isArray(result.data) ? result.data : [])
            .filter(row => row && Object.keys(row).length > 0)
            .map(row => headers.map(header => {
              const value = row?.[header]
              if (value === null || value === undefined) return ''
              return String(value)
            }))

          setPreviews(prev => ({
            ...prev,
            [type]: {
              headers,
              rows,
            }
          }))
          setActiveDataset(type)
          setPage(0)
          setParseError(null)
        },
        error: (error) => {
          console.error(error)
          setParseError(`Failed to parse ${file.name}: ${error.message}`)
        }
      })
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

        <section className="mt-8 bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
            📝 Sample Data Format
          </h3>
          <div className="space-y-4 text-sm">
            <div>
              <strong className="text-blue-900 dark:text-blue-100">subscriptions.csv:</strong>
              <pre className="mt-1 p-3 bg-gray-50 dark:bg-gray-900 rounded text-xs overflow-x-auto">
{`date,customer_id,plan,amount,currency
2024-01-01,C001,Pro,99,USD
2024-01-01,C002,Basic,29,USD`}
              </pre>
            </div>
            <div>
              <strong className="text-blue-900 dark:text-blue-100">churn.csv:</strong>
              <pre className="mt-1 p-3 bg-gray-50 dark:bg-gray-900 rounded text-xs overflow-x-auto">
{`date,customer_id,reason
2024-01-15,C003,price
2024-01-20,C004,feature`}
              </pre>
            </div>
          </div>
        </section>

        <section className="mt-8 bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">🔍 Data Preview</h3>
              <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                Preview the first rows of your CSV files to confirm column headers and values.
              </p>
            </div>
            {parseError && (
              <div className="text-xs text-red-500" role="alert">
                {parseError}
              </div>
            )}
          </div>

          <div className="mt-4 flex flex-wrap items-center gap-2" role="tablist" aria-label="CSV dataset tabs">
            {DATASET_ORDER.map(dataset => {
              const isActive = activeDataset === dataset
              const hasPreview = Boolean(previews[dataset]?.rows.length)
              return (
                <button
                  key={dataset}
                  type="button"
                  onClick={() => {
                    if (previews[dataset]) {
                      setActiveDataset(dataset)
                      setPage(0)
                    }
                  }}
                  disabled={!previews[dataset]}
                  aria-pressed={isActive}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 ${
                    isActive
                      ? 'bg-blue-600 text-white shadow'
                      : previews[dataset]
                        ? 'bg-gray-100 dark:bg-gray-900 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-800'
                        : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  }`}
                  aria-label={previews[dataset] ? `Show ${DATASET_LABELS[dataset]} preview` : `${DATASET_LABELS[dataset]} preview unavailable`}
                >
                  {DATASET_LABELS[dataset]}
                  {!hasPreview && previews[dataset] && (
                    <span className="ml-2 text-xs text-gray-500">(0 rows)</span>
                  )}
                </button>
              )
            })}
          </div>

          <DataPreviewCard
            preview={activeDataset ? previews[activeDataset] : undefined}
            dataset={activeDataset}
            page={page}
            onPageChange={setPage}
          />
        </section>
      </div>
    </div>
  )
}

function DataPreviewCard({
  preview,
  dataset,
  page,
  onPageChange,
}: {
  preview?: PreviewData
  dataset: DatasetType | null
  page: number
  onPageChange: (next: number) => void
}) {
  const totalRows = preview?.rows.length ?? 0
  const totalPages = preview ? Math.max(1, Math.ceil(preview.rows.length / PAGE_SIZE)) : 1
  const safePage = Math.min(page, totalPages - 1)
  const paginatedRows = useMemo(() => {
    if (!preview) return []
    const start = safePage * PAGE_SIZE
    return preview.rows.slice(start, start + PAGE_SIZE)
  }, [preview, safePage])

  useEffect(() => {
    if (preview && page > totalPages - 1) {
      onPageChange(Math.max(totalPages - 1, 0))
    }
  }, [preview, page, totalPages, onPageChange])

  if (!dataset) {
    return (
      <div className="mt-6 text-sm text-gray-500 dark:text-gray-400">Select or upload a CSV file to preview its contents.</div>
    )
  }

  if (!preview) {
    return (
      <div className="mt-6 text-sm text-gray-500 dark:text-gray-400">Upload a CSV for {DATASET_LABELS[dataset]} to see the preview here.</div>
    )
  }

  if (!preview.rows.length) {
    return (
      <div className="mt-6 text-sm text-gray-500 dark:text-gray-400">No rows detected in the uploaded file.</div>
    )
  }

  const startIndex = safePage * PAGE_SIZE + 1
  const endIndex = Math.min((safePage + 1) * PAGE_SIZE, totalRows)

  return (
    <div className="mt-6">
      <div className="overflow-x-auto border border-gray-200 dark:border-gray-700 rounded-lg">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700 text-sm">
          <thead className="bg-gray-50 dark:bg-gray-900">
            <tr>
              {preview.headers.map((header) => (
                <th
                  key={header}
                  scope="col"
                  className="px-4 py-2 text-left font-semibold text-gray-700 dark:text-gray-200 uppercase tracking-wider"
                >
                  {header || '—'}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-950 divide-y divide-gray-100 dark:divide-gray-800">
            {paginatedRows.map((row, rowIndex) => (
              <tr key={`${dataset}-${safePage}-${rowIndex}`} className={rowIndex % 2 === 0 ? 'bg-white dark:bg-gray-950' : 'bg-gray-50 dark:bg-gray-900/60'}>
                {row.map((cell, cellIndex) => (
                  <td key={`${rowIndex}-${cellIndex}`} className="px-4 py-2 text-gray-700 dark:text-gray-200 whitespace-nowrap">
                    {cell || '—'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-4 flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
        <span>
          Showing {startIndex}-{endIndex} of {totalRows} rows
        </span>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => onPageChange(Math.max(safePage - 1, 0))}
            disabled={safePage === 0}
            className={`px-3 py-1.5 rounded-md border text-xs font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 ${
              safePage === 0
                ? 'border-gray-200 dark:border-gray-700 text-gray-400 cursor-not-allowed'
                : 'border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
            aria-label="Previous page"
          >
            Prev
          </button>
          <span aria-live="polite">Page {safePage + 1} / {totalPages}</span>
          <button
            type="button"
            onClick={() => onPageChange(Math.min(safePage + 1, totalPages - 1))}
            disabled={safePage >= totalPages - 1}
            className={`px-3 py-1.5 rounded-md border text-xs font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 ${
              safePage >= totalPages - 1
                ? 'border-gray-200 dark:border-gray-700 text-gray-400 cursor-not-allowed'
                : 'border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
            aria-label="Next page"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  )
}

