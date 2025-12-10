# Complete Beginner's Guide to Running DealFlowData

This guide will walk you through everything you need to get your website running on your local computer - **no prior experience needed!**

## What You'll Need to Install

### 1. Visual Studio Code (VS Code) - Code Editor
1. Go to https://code.visualstudio.com/
2. Click "Download for Windows" (or Mac/Linux)
3. Install it like any normal program
4. Open VS Code

### 2. Git - Version Control
1. Go to https://git-scm.com/downloads
2. Download and install for your operating system
3. Use default settings during installation

### 3. Docker Desktop - Runs the Backend
1. Go to https://www.docker.com/products/docker-desktop/
2. Download Docker Desktop for your operating system
3. Install it
4. **Important**: Start Docker Desktop and keep it running

### 4. Node.js - Runs the Frontend
1. Go to https://nodejs.org/
2. Download the **LTS version** (left side, recommended)
3. Install it with default settings

## Step-by-Step: Getting the Code

### Option 1: Clone with VS Code (Easiest)

1. **Open VS Code**
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
3. Type "Git: Clone" and press Enter
4. Paste this URL:
   ```
   https://github.com/BrinkBoef/DFD-website.git
   ```
5. Choose a folder on your computer to save the project
6. When asked "Would you like to open the cloned repository?", click **Yes**

### Option 2: Download ZIP

1. Go to https://github.com/BrinkBoef/DFD-website
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file
5. Open VS Code → File → Open Folder → Select the extracted folder

## Step-by-Step: Running the Website

### Step 1: Open Terminal in VS Code

In VS Code:
- Click **Terminal** in the top menu
- Click **New Terminal**
- A command line window will appear at the bottom

### Step 2: Switch to the Right Branch

In the terminal, type these commands (press Enter after each):

```bash
git checkout claude/company-data-platform-01Tu4Ta1YgBw27cshroLcc4z
```

### Step 3: Start the Backend (Database + API)

**Make sure Docker Desktop is running first!**

In the terminal, type:

```bash
docker-compose up -d
```

This will:
- Download PostgreSQL database
- Start the backend API
- Takes 1-2 minutes the first time

**Wait until you see**: "✔ Container dfd_backend Started"

### Step 4: Import Your Data

In the terminal, type:

```bash
docker exec -it dfd_backend python scripts/import_data.py
```

This imports all 34,843 funds and 10,738 companies from GP.xlsx into the database.

**You'll see**:
```
Importing funds...
Successfully imported 34843 funds
Total Companies: 10738
Total Funds: 34843
```

This takes about 1-2 minutes.

### Step 5: Start the Frontend (Website)

In the terminal, type these commands:

```bash
cd frontend
npm install
```

**Wait for it to finish** (downloads website dependencies, takes 1-2 minutes the first time).

Then type:

```bash
npm run dev
```

**You'll see**:
```
- Local:        http://localhost:3000
```

### Step 6: Open Your Website! 🎉

Open your web browser and go to:

**http://localhost:3000**

You should see your DealFlowData website with:
- Your DFD logo
- Search bar
- List of all companies
- Click any company to see its funds

## How to Stop Everything

### Stop Frontend
In the terminal where it says "Local: http://localhost:3000":
- Press `Ctrl+C` (Windows/Linux) or `Cmd+C` (Mac)

### Stop Backend
In the terminal, type:
```bash
docker-compose down
```

## Next Time You Want to Run It

You don't need to reinstall anything! Just:

1. **Start Docker Desktop** (must be running)
2. **Open VS Code** → Open your DFD-website folder
3. **Open Terminal**
4. Type:
   ```bash
   docker-compose up -d
   cd frontend
   npm run dev
   ```
5. Go to **http://localhost:3000**

## Troubleshooting

### "docker: command not found"
→ Docker Desktop is not installed or not running. Start Docker Desktop.

### "npm: command not found"
→ Node.js is not installed. Install it from https://nodejs.org/

### Backend won't start
→ Check if Docker Desktop is running
→ Type: `docker-compose logs` to see errors

### Frontend shows "Failed to fetch"
→ Backend is not running. Start it with `docker-compose up -d`

### Port already in use
→ Something else is using port 3000 or 8000
→ Close other programs or change the port

## File Structure

```
DFD-website/
├── backend/           ← Python API (runs in Docker)
├── frontend/          ← Website (Next.js)
│   └── public/
│       └── logo.png   ← Your logo is here
├── GP.xlsx            ← Your company data
└── docker-compose.yml ← Backend configuration
```

## Checking if Everything Works

### Check Backend API
Go to: http://localhost:8000/docs
You should see the API documentation.

### Check Database
In terminal:
```bash
docker exec -it dfd_postgres psql -U postgres -d dfd_db -c "SELECT COUNT(*) FROM companies;"
```
Should show: 10738

## Making Changes

### Want to edit the website?
1. Open `frontend/src/components/` in VS Code
2. Edit any `.tsx` file
3. Save it
4. The website refreshes automatically!

### Want to change colors?
Edit `frontend/tailwind.config.ts`:
- `primary`: Currently orange (#FF8C42)
- `secondary`: Currently dark blue (#2D3142)

## Questions?

- Backend API docs: http://localhost:8000/docs
- Check terminal for errors
- Make sure Docker Desktop shows "running" status

## Summary of Commands

```bash
# First time setup
git checkout claude/company-data-platform-01Tu4Ta1YgBw27cshroLcc4z
docker-compose up -d
docker exec -it dfd_backend python scripts/import_data.py
cd frontend
npm install
npm run dev

# Every time after
docker-compose up -d
cd frontend
npm run dev

# To stop
# Press Ctrl+C in frontend terminal
docker-compose down
```

**That's it! You're now running a full-stack web application locally!** 🚀
