# 📋 AI Job Application Tracker

A full-stack web application to track job applications and get AI-powered resume tips using Google Gemini API.

**Live Demo:** [Coming Soon]  
**Tech Stack:** React.js • FastAPI • SQLite • Google Gemini API

---

## 🎯 Features

### 1. **Application Tracking**
- Add new job applications with company, role, and application date
- Track application status: Applied, Interview, Rejected, Offer
- View all applications in a clean, sortable list
- Update status on-the-fly with dropdown selector
- Delete applications with confirmation

### 2. **Dashboard with Analytics**
- 4 stat cards showing total applications, interviews, offers, and rejections
- Bar chart visualization of applications by status (using Recharts)
- Real-time statistics that update when you add/modify applications
- Responsive grid layout that works on mobile and desktop

### 3. **AI Resume Tip Generator**
- Paste a job description and get 3 tailored resume bullet points
- Uses Google Gemini API for intelligent, role-specific suggestions
- Copy individual bullet points to clipboard with one click
- Helpful tips on how to use the feature effectively

---

## 🛠️ Tech Stack & Decisions

### **Frontend: React.js + Vite**
- **Why React?** Industry-standard UI library with component reusability and state management
- **Why Vite?** Fast dev server with HMR (Hot Module Replacement) and optimized production builds
- **Why no CSS framework?** Clean, hand-written CSS makes styling lightweight and fully customizable without third-party dependencies
- **Why Recharts?** Lightweight charting library that handles responsive charts with minimal configuration

### **Backend: FastAPI + Python**
- **Why FastAPI?** Modern, fast (comparable to Node.js), built-in async/await support, automatic OpenAPI documentation
- **Why SQLAlchemy ORM?** Type-safe database queries, migrations support, and database-agnostic code
- **Proper separation of concerns:** Routes (API), Models (Database), and AI Helper (Business logic) in separate files

### **Database: SQLite**
- **Why SQLite?** Perfect for small-to-medium projects, no server setup required, file-based persistence
- **Easy deployment:** Single `.db` file vs. managing a database server
- **Zero configuration:** Just works out of the box

### **AI: Google Gemini API (Free Tier)**
- **Why Gemini?** Free tier with good rate limits, powerful multi-modal model, excellent for text generation
- **API Cost:** Free tier provides 60 requests per minute (more than enough for this use case)
- **Fallback handling:** Graceful errors if API key is missing or request fails

### **Architecture Decisions**

**Centralized API Service Layer (`api.js`):**
- All HTTP requests go through one service file
- Easy to add caching, request interceptors, or auth headers in the future
- Single source of truth for API endpoints

**Component-Based UI:**
- `Dashboard` — statistics and applications list
- `ApplicationForm` — add new applications
- `AITip` — AI-powered resume generator
- Each component is single-purpose and reusable

**CORS Enabled:**
- Backend accepts requests from React dev server (ports 3000 & 5173)
- Production-ready: can be configured for specific domains

---

## 🚀 Getting Started

### Prerequisites
- **Node.js 16+** (for frontend)
- **Python 3.9+** (for backend)
- **Google Gemini API Key** (free tier: [https://ai.google.dev](https://ai.google.dev))
- **Git**

### Step 1: Clone & Setup Project Structure
```bash
git clone https://github.com/yourusername/job-tracker.git
cd job-tracker
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

**Get Your Gemini API Key:**
1. Go to [https://ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Create a new API key
4. Paste it in your `.env` file

**Start the backend server:**
```bash
python main.py
```
✅ Backend running at `http://localhost:8000`  
📖 API docs at `http://localhost:8000/docs` (auto-generated Swagger UI)

### Step 3: Frontend Setup

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```
✅ Frontend running at `http://localhost:3000` or `http://localhost:5173`

### Step 4: Start Using!
1. Open http://localhost:3000 in your browser
2. Click "Add Application" and enter a job application
3. Go to "Dashboard" to see your stats and applications list
4. Click "AI Resume Tip", paste a job description, and get AI-generated bullet points

---

## 📋 API Endpoints

### Job Applications
- `GET /applications` — Get all applications (sorted by date)
- `POST /applications` — Create new application
  ```json
  {
    "company": "Google",
    "role": "Senior Software Engineer",
    "application_date": "2024-05-07T00:00:00Z"
  }
  ```
- `PATCH /applications/{id}` — Update application status
  ```json
  {
    "status": "Interview"
  }
  ```
- `DELETE /applications/{id}` — Delete application

### Statistics
- `GET /stats` — Get dashboard statistics
  ```json
  {
    "total_applications": 15,
    "interviews": 3,
    "offers": 1,
    "rejected": 2,
    "by_status": {
      "Applied": 9,
      "Interview": 3,
      "Rejected": 2,
      "Offer": 1
    }
  }
  ```

### AI Features
- `POST /ai-tip` — Generate resume tips from job description
  ```json
  {
    "job_description": "We're looking for a software engineer with..."
  }
  ```
  Response:
  ```json
  {
    "bullet_points": [
      "Led migration of legacy system to microservices...",
      "Implemented real-time data pipeline using...",
      "Mentored junior engineers on..."
    ]
  }
  ```

---

## 📁 Project Structure

```
job-tracker/
├── backend/
│   ├── main.py              # FastAPI app with CORS
│   ├── models.py            # SQLAlchemy models & database setup
│   ├── routes.py            # API endpoints (CRUD, stats, AI)
│   ├── ai_helper.py         # Gemini API integration
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── .gitignore
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Dashboard.css
│   │   │   ├── ApplicationForm.jsx
│   │   │   ├── ApplicationForm.css
│   │   │   ├── AITip.jsx
│   │   │   └── AITip.css
│   │   ├── services/
│   │   │   └── api.js       # Centralized API calls
│   │   ├── App.jsx          # Main app component
│   │   ├── App.css          # Global styles
│   │   └── main.jsx         # React entry point
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── .gitignore
│   └── node_modules/
│
└── README.md
```

---

## 🔄 How It Works

### Adding a Job Application
1. User clicks "Add Application" tab
2. Enters company name, role, and application date
3. Clicks "Add Application" button
4. Frontend sends `POST /applications` request to backend
5. Backend stores in SQLite database
6. Frontend redirects to Dashboard showing updated stats

### Updating Application Status
1. User selects new status from dropdown on Dashboard
2. Frontend sends `PATCH /applications/{id}` request
3. Backend updates database
4. Dashboard re-fetches stats and displays updated chart

### Generating AI Resume Tips
1. User pastes job description in "AI Resume Tip" tab
2. Clicks "Generate Resume Tips" button
3. Frontend sends `POST /ai-tip` request with job description
4. Backend calls Google Gemini API
5. Gemini returns 3 tailored resume bullet points
6. Frontend displays bullet points with copy buttons
7. User can copy individual points to clipboard

---

## 🎨 UI/UX Features

- **Gradient Header:** Modern purple-to-pink gradient for visual appeal
- **Card-Based Layout:** Clean stat cards and application cards with hover effects
- **Real-Time Updates:** Dashboard refreshes immediately after actions
- **Responsive Design:** Works seamlessly on mobile, tablet, and desktop
- **Status Badges:** Color-coded status indicators (blue, yellow, red, green)
- **Loading States:** Visual feedback while making API calls
- **Error Handling:** User-friendly error messages if something fails
- **Empty States:** Helpful messages when no data exists

---

## 🚨 Error Handling

### Frontend
- Network errors display user-friendly messages
- Form validation prevents empty submissions
- Confirmation dialog before deleting applications
- Loading states prevent duplicate requests

### Backend
- Proper HTTP status codes (200, 404, 400, 500)
- Pydantic validation for all request bodies
- Try-catch blocks for API failures
- Fallback messages if Gemini API key is missing

---

## 📈 Future Enhancements

- **User Authentication:** Login/signup to save applications per user
- **Export to CSV:** Download your applications as a spreadsheet
- **Interview Notes:** Attach notes, questions, and feedback for each application
- **Email Reminders:** Get reminded about upcoming interviews
- **Job Description Scraping:** Auto-populate job details from URL
- **Resume Optimization Score:** AI-powered scoring of how well your resume matches the job
- **Mobile App:** React Native version for iOS/Android
- **Dark Mode:** Toggle between light and dark themes
- **Multiple Resumes:** Track applications with different resume versions

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt

# Check if port 8000 is in use
# On Windows: netstat -ano | findstr :8000
# On macOS/Linux: lsof -i :8000
```

### Frontend won't connect to backend
```bash
# Ensure backend is running (http://localhost:8000)
# Check that CORS is enabled (should be, but verify in main.py)
# Try clearing browser cache
# Check browser console for specific error messages
```

### Gemini API errors
```bash
# Verify API key is in .env file
# Check you haven't exceeded free tier rate limits (60 req/min)
# Ensure job description is not too long or empty
```

### Database issues
```bash
# Delete old database to reset
rm job_tracker.db  # or del job_tracker.db on Windows

# Restart backend (will auto-create fresh database)
python main.py
```

---

## 📸 Screenshots

*(Screenshots coming after first release)*

- Dashboard with stats cards and bar chart
- Application form with validation
- AI Resume Tip generator with results
- Mobile-responsive layouts

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.

---

## 💬 Support

Have questions or issues? Please open an issue on GitHub or reach out to the maintainers.

---

## 🎓 Learning Resources

This project demonstrates:
- **React:** Components, hooks (useState, useEffect), event handling
- **FastAPI:** Modern Python web framework, async routes, CORS middleware
- **SQLAlchemy:** ORM, database models, relationships
- **REST API:** CRUD operations, proper HTTP methods and status codes
- **Gemini API:** LLM integration, prompt engineering, error handling
- **Frontend-Backend Communication:** Axios, API service abstraction, error handling

---

## 🙏 Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Recharts Documentation](https://recharts.org/)
- [Google Gemini API](https://ai.google.dev/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)

---

**Built with ❤️ by [Your Name]**  
Last Updated: May 2024
