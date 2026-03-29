# VRMS — Setup Guide
## Vehicle Rental Management System | DriveEasy Rentals

---

## 📁 Files
| File             | Purpose                                      |
|------------------|----------------------------------------------|
| `seed.sql`       | Creates the database, all tables, and sample data |
| `main.py`        | FastAPI backend (all API endpoints)          |
| `requirements.txt` | Python dependencies                        |
| `App.jsx`        | React frontend (drop into your Vite project) |

---

## Step 1 — MySQL: Run the seed file

Open MySQL (Workbench, CLI, DBeaver, etc.) and run:

```sql
SOURCE /path/to/seed.sql;
```

Or paste the contents directly. This will:
- Create the `vrms` database
- Create all 7 tables with constraints
- Create the index on `RentalAgreement(CustomerID)`
- Insert sample data (4 branches, 5 customers, 10 vehicles, 10 agreements, 5 maintenance records)

---

## Step 2 — Backend: FastAPI

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure DB credentials
Either edit the defaults in `main.py` (lines with `os.getenv`), or set environment variables:
```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=vrms
```

### Start the server
```bash
uvicorn main:app --reload
```

API runs at: `http://localhost:8000`  
Auto-docs at: `http://localhost:8000/docs`

---

## Step 3 — Frontend: React + Vite + Tailwind

### Create a new Vite project (if you don't have one)
```bash
npm create vite@latest vrms-frontend -- --template react
cd vrms-frontend
npm install
```

### Install Tailwind CSS
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Edit `tailwind.config.js`:
```js
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
}
```

Add to `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Drop in the App
Replace `src/App.jsx` with the provided `App.jsx` file.

Make sure `src/main.jsx` imports the CSS:
```jsx
import "./index.css";
```

### Start the dev server
```bash
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## API Endpoints

| Method | Endpoint                              | Description                          |
|--------|---------------------------------------|--------------------------------------|
| GET    | `/vehicles`                           | List all vehicles (with type/branch) |
| POST   | `/vehicles`                           | Add a new vehicle                    |
| GET    | `/customers`                          | List all customers                   |
| GET    | `/rental-agreements?customer_id={id}` | Get agreements for a customer        |
| GET    | `/vehicle-types`                      | List vehicle types (for dropdown)    |
| GET    | `/branches`                           | List branches (for dropdown)         |

---

## AI Disclosure
Portions of `main.py` and `App.jsx` were generated/assisted by **Claude Sonnet (Anthropic)**.  
Specifically: API route structure, Pydantic validators, React component layout, and Tailwind styling.  
The development team reviewed, tested, and remains fully responsible for all code.