'use client'

import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Company {
  id: number
  name: string
  total_funds: number
}

interface Fund {
  id: number
  fund_name: string
  vintage: number | null
  size: string | null
  status: string | null
  strategy: string | null
  region: string | null
  sector: string | null
  net_irr: number | null
  dpi: number | null
  moic: number | null
  rvpi: number | null
}

interface Person {
  id: number
  name: string
  email: string | null
  job_title: string | null
}

interface CompanyDetails {
  id: number
  name: string
  total_funds: number
  funds: Fund[]
  people: Person[]
}

export default function CompanyCard({ company }: { company: Company }) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [details, setDetails] = useState<CompanyDetails | null>(null)
  const [loading, setLoading] = useState(false)

  const fetchCompanyDetails = async () => {
    if (details) {
      setIsExpanded(!isExpanded)
      return
    }

    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/api/companies/${company.id}`)
      setDetails(response.data)
      setIsExpanded(true)
    } catch (error) {
      console.error('Error fetching company details:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
      {/* Company Header - Clickable */}
      <button
        onClick={fetchCompanyDetails}
        className="w-full px-6 py-5 flex items-center justify-between hover:bg-gray-50 transition-colors duration-150 rounded-lg"
      >
        <div className="flex-1 text-left">
          <h3 className="text-xl font-semibold text-secondary">{company.name}</h3>
          <p className="text-sm text-gray-600 mt-1">
            {company.total_funds} {company.total_funds === 1 ? 'fund' : 'funds'}
          </p>
        </div>
        <div className="ml-4">
          <svg
            className={`w-6 h-6 text-gray-400 transform transition-transform duration-200 ${
              isExpanded ? 'rotate-180' : ''
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </div>
      </button>

      {/* Expandable Details */}
      {isExpanded && (
        <div className="px-6 pb-6 border-t border-gray-200">
          {loading ? (
            <div className="py-8 flex justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : details ? (
            <>
              {/* Funds Section */}
              <div className="mt-6">
                <h4 className="text-lg font-semibold text-secondary mb-4">
                  Funds ({details.funds.length})
                </h4>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Fund Name
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Vintage
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Size
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Strategy
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Region
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          IRR %
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          DPI
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          MOIC
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {details.funds.map((fund) => (
                        <tr key={fund.id} className="hover:bg-gray-50">
                          <td className="px-4 py-3 text-sm text-gray-900">
                            {fund.fund_name || '-'}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            {fund.vintage ? Math.floor(fund.vintage) : '-'}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            {fund.size || '-'}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            {fund.strategy || '-'}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            {fund.region || '-'}
                          </td>
                          <td className="px-4 py-3 text-sm">
                            <span
                              className={`px-2 py-1 rounded-full text-xs font-medium ${
                                fund.status === 'Investing'
                                  ? 'bg-green-100 text-green-800'
                                  : fund.status === 'Harvesting'
                                  ? 'bg-yellow-100 text-yellow-800'
                                  : fund.status === 'Liquidated'
                                  ? 'bg-gray-100 text-gray-800'
                                  : 'bg-blue-100 text-blue-800'
                              }`}
                            >
                              {fund.status || '-'}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            {fund.net_irr ? fund.net_irr.toFixed(2) : '-'}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            {fund.dpi ? fund.dpi.toFixed(2) : '-'}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            {fund.moic ? fund.moic.toFixed(2) : '-'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* People Section */}
              {details.people && details.people.length > 0 && (
                <div className="mt-8">
                  <h4 className="text-lg font-semibold text-secondary mb-4">
                    Related People ({details.people.length})
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {details.people.map((person) => (
                      <div
                        key={person.id}
                        className="bg-gray-50 rounded-lg p-4 border border-gray-200"
                      >
                        <h5 className="font-medium text-secondary">{person.name}</h5>
                        {person.job_title && (
                          <p className="text-sm text-gray-600 mt-1">{person.job_title}</p>
                        )}
                        {person.email && (
                          <a
                            href={`mailto:${person.email}`}
                            className="text-sm text-primary hover:underline mt-2 inline-block"
                          >
                            {person.email}
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Empty State for People */}
              {(!details.people || details.people.length === 0) && (
                <div className="mt-8 bg-gray-50 rounded-lg p-6 text-center">
                  <p className="text-gray-500">
                    No people data available for this company yet.
                  </p>
                </div>
              )}
            </>
          ) : null}
        </div>
      )}
    </div>
  )
}
