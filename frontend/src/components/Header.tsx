import Image from 'next/image'

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container-custom py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            {/* Logo placeholder - will be replaced when logo is uploaded */}
            <div className="w-32 h-16 bg-gradient-to-r from-primary to-orange-600 rounded flex items-center justify-center">
              <span className="text-white text-2xl font-bold">DFD</span>
            </div>
            <div>
              <h1 className="text-3xl font-bold text-secondary">DealFlowData</h1>
              <p className="text-gray-600 text-sm mt-1">Private Equity Market Mapping</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
