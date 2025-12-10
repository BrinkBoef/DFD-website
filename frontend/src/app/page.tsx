'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import CompanyCard from '@/components/CompanyCard'
import Header from '@/components/Header'
import SearchBar from '@/components/SearchBar'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Company {
  id: number
  name: string
  total_funds: number
}

export default function Home() {
  const [companies, setCompanies] = useState<Company[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filteredCompanies, setFilteredCompanies] = useState<Company[]>([])

  useEffect(() => {
    fetchCompanies()
  }, [])

  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredCompanies(companies)
    } else {
      const filtered = companies.filter(company =>
        company.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredCompanies(filtered)
    }
  }, [searchTerm, companies])

  const fetchCompanies = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/api/companies?limit=500`)
      setCompanies(response.data)
      setFilteredCompanies(response.data)
    } catch (error) {
      console.error('Error fetching companies:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Header />

      <div className="container-custom py-8">
        <SearchBar searchTerm={searchTerm} onSearchChange={setSearchTerm} />

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : (
          <>
            <div className="mb-6 text-gray-600">
              Showing {filteredCompanies.length} of {companies.length} companies
            </div>

            <div className="grid gap-4 md:gap-6">
              {filteredCompanies.map((company) => (
                <CompanyCard key={company.id} company={company} />
              ))}
            </div>

            {filteredCompanies.length === 0 && (
              <div className="text-center py-20 text-gray-500">
                <p className="text-xl">No companies found matching "{searchTerm}"</p>
                <p className="mt-2">Try a different search term</p>
              </div>
            )}
          </>
        )}
      </div>
    </main>
  )
}
