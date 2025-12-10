import Image from 'next/image'

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container-custom py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Image
              src="/logo.png"
              alt="DealFlowData Logo"
              width={160}
              height={80}
              className="object-contain"
              priority
            />
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
