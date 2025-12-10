# DealFlowData - Private Equity Market Mapping Platform

A web platform for browsing and exploring private equity companies and their funds.

## Features

- 📊 **Company Database**: Browse 10,700+ private equity companies
- 💼 **Fund Details**: View detailed information on 34,000+ funds
- 🔍 **Search**: Quick search functionality to find companies
- 📱 **Responsive Design**: Beautiful UI that works on all devices
- 🎯 **Expandable Cards**: Click to see all funds for each company
- 📈 **Performance Metrics**: IRR, DPI, MOIC, and more

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Relational database
- **SQLAlchemy**: ORM for database operations
- **Docker**: Containerization

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### 1. Start Backend with Docker

```bash
# Start PostgreSQL and backend API
docker-compose up -d

# Check if services are running
docker-compose ps
```

The backend API will be available at `http://localhost:8000`

### 2. Import Data

```bash
# Enter the backend container
docker exec -it dfd_backend bash

# Run the import script
python scripts/import_data.py

# Exit container
exit
```

This will import all companies and funds from `GP.xlsx` into the database.

**Expected output:**
- ~10,738 companies imported
- ~34,843 funds imported

### 3. Start Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

```
GET  /api/companies              # List all companies
GET  /api/companies/{id}         # Get company with funds
GET  /api/funds                  # List all funds
POST /api/companies              # Create new company
POST /api/companies/{id}/people  # Add person to company
```

## Project Structure

```
DFD-website/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # Database operations
│   │   └── database.py      # DB connection
│   ├── scripts/
│   │   └── import_data.py   # Data import script
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx     # Main page
│   │   │   └── layout.tsx   # Layout
│   │   └── components/
│   │       ├── CompanyCard.tsx  # Expandable company card
│   │       ├── Header.tsx       # Header with logo
│   │       └── SearchBar.tsx    # Search component
│   ├── package.json
│   └── tailwind.config.ts
├── docker-compose.yml
├── GP.xlsx                  # Source data
└── README.md
```

## Database Schema

### Companies Table
- `id`: Primary key
- `name`: Company name (General Partner)
- `total_funds`: Number of funds
- `created_at`, `updated_at`: Timestamps

### Funds Table
- `id`: Primary key
- `company_id`: Foreign key to companies
- `fund_name`: Name of the fund
- `vintage`: Year founded
- `size`: Fund size (e.g., "213.0M")
- `status`: Current status (Investing, Harvesting, Liquidated, etc.)
- `strategy`: Investment strategy (Buyout, Venture, etc.)
- `region`: Geographic focus
- `sector`: Industry sector
- Performance metrics: `net_irr`, `dpi`, `moic`, `rvpi`, etc.
- 30+ additional fields

### People Table (Ready for future use)
- `id`: Primary key
- `company_id`: Foreign key to companies
- `name`, `email`, `job_title`: Contact info
- `created_at`, `updated_at`: Timestamps

## Adding People Data

When you have people data, you can import it using the API:

```python
import requests

# Add a person to a company
response = requests.post(
    'http://localhost:8000/api/companies/1/people',
    json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'job_title': 'Managing Partner'
    }
)
```

The people will automatically appear in the "Related People" section when you expand a company.

## Development

### Backend Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run locally (without Docker)
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dfd_db
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

### Environment Variables

Create `.env` file in the root:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dfd_db
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Adding the Logo

1. Add your logo file (PNG, SVG, etc.) to `frontend/public/`
2. Update `frontend/src/components/Header.tsx`:

```tsx
// Replace the placeholder div with:
<Image
  src="/logo.png"
  alt="DealFlowData"
  width={128}
  height={64}
/>
```

## Deployment

### Backend
- Deploy to Railway, Render, or AWS
- Use managed PostgreSQL database
- Set `DATABASE_URL` environment variable

### Frontend
- Deploy to Vercel (recommended for Next.js)
- Set `NEXT_PUBLIC_API_URL` to your backend URL

## Troubleshooting

**Backend won't start:**
```bash
# Check PostgreSQL is running
docker-compose ps

# Check logs
docker-compose logs backend
docker-compose logs postgres
```

**Data import fails:**
```bash
# Make sure GP.xlsx is in the root directory
# Check database connection
docker exec -it dfd_postgres psql -U postgres -d dfd_db -c "\dt"
```

**Frontend can't connect to backend:**
- Check that backend is running on port 8000
- Verify CORS is enabled in backend
- Check `NEXT_PUBLIC_API_URL` environment variable

## License

Proprietary - DealFlowData

## Support

For issues or questions, please contact the development team.
