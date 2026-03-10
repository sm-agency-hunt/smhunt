# SMHUNT - AI Lead Generation Platform

## Overview
SMHUNT is now equipped with a comprehensive AI-powered lead generation and client communication system. The platform includes:

1. **Dashboard** - Real-time analytics and insights
2. **Lead Search** - AI-powered lead discovery
3. **AI Agent** - Automated outreach and client communication

## New Features Added

### 1. Navigation Bar (Navbar)
- **Location**: `frontend/src/components/Navbar.js`
- **Features**:
  - Responsive sidebar navigation
  - Mobile-friendly drawer menu
  - Quick access to all sections
  - User profile menu

### 2. Lead Search Page
- **Location**: `frontend/src/pages/LeadSearch.js`
- **Features**:
  - Search by industry/niche
  - Filter by location
  - Set number of leads to generate
  - View detailed lead information
  - Save leads to database
  - Generate AI outreach messages instantly

### 3. AI Lead Agent
- **Location**: `frontend/src/pages/AIAgent.js`
- **Features**:
  - **5-Step Campaign Workflow**:
    1. Configure campaign settings
    2. Generate qualified leads
    3. Create personalized messages
    4. Launch outreach campaign
    5. Monitor & auto follow-up
  
  - **Campaign Customization**:
    - Message tone (Professional, Friendly, Enthusiastic)
    - Campaign goal (Meeting booking, Product demo, Partnership)
    - Daily lead limits
    - Auto follow-up enabled/disabled

### 4. Backend AI Agent Service
- **Location**: `src/services/ai/ai_lead_agent.py`
- **Capabilities**:
  - Automated lead generation and scoring
  - Personalized message creation
  - Multi-channel outreach
  - Response handling with sentiment analysis
  - Intent classification
  - Smart follow-up automation
  - Conversation management

### 5. API Endpoints
- **Location**: `src/api/v1/routers/ai_agent.py`
- **Endpoints**:
  - `POST /api/v1/ai-agent/generate-leads` - Generate qualified leads
  - `POST /api/v1/ai-agent/create-outreach` - Create personalized messages
  - `POST /api/v1/ai-agent/send-campaign` - Send outreach campaign
  - `POST /api/v1/ai-agent/handle-response` - Process lead responses
  - `POST /api/v1/ai-agent/send-followup` - Send automated follow-ups
  - `GET /api/v1/ai-agent/campaign-status/{id}` - Get campaign status

## Installation & Setup

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

The app will run on `http://localhost:3000`

### Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

The API will run on `http://localhost:8000`

## How to Use the AI Agent

### Step 1: Navigate to AI Agent
Click on "AI Agent" in the sidebar menu

### Step 2: Configure Campaign
- Enter campaign name
- Select target industry
- Choose location
- Set message tone
- Define campaign goal
- Set daily lead limit

### Step 3: Generate Leads
- Click "Generate Leads"
- AI will find qualified businesses
- Review lead scores and qualifications

### Step 4: Create Messages
- AI generates personalized messages for each lead
- Review and customize if needed
- Each message is tailored to the specific business

### Step 5: Launch Campaign
- Start automated outreach
- Messages are sent via email
- System tracks delivery and responses

### Step 6: Monitor & Follow-up
- View active conversations
- AI analyzes responses
- Automatic follow-ups based on engagement
- Schedule meetings directly

## Key Features

### AI Capabilities
- ✅ Lead scoring and qualification
- ✅ Sentiment analysis
- ✅ Intent classification
- ✅ Personalized content generation
- ✅ Smart follow-up timing
- ✅ Response prioritization

### Dashboard Features
- ✅ Total businesses tracked
- ✅ Total leads generated
- ✅ Outreach messages sent
- ✅ Conversion rates
- ✅ Industry distribution charts
- ✅ Weekly activity tracking

### Search Features
- ✅ Advanced filtering
- ✅ Location-based search
- ✅ Industry-specific queries
- ✅ Bulk lead generation
- ✅ Real-time results

## API Documentation

Access interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
smhunt.online/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.js          # Navigation component
│   │   ├── pages/
│   │   │   ├── LeadSearch.js      # Lead search page
│   │   │   └── AIAgent.js         # AI agent interface
│   │   └── App.js                 # Main app with routing
│   └── package.json
├── src/
│   ├── services/
│   │   └── ai/
│   │       └── ai_lead_agent.py   # AI agent service
│   └── api/
│       └── v1/
│           └── routers/
│               └── ai_agent.py    # AI agent API routes
└── main.py
```

## Technology Stack

### Frontend
- React 18
- Material-UI (MUI)
- React Router v6
- Axios
- Recharts

### Backend
- FastAPI
- SQLAlchemy
- Celery (for async tasks)
- Python 3.9+

## Next Steps

To fully utilize the AI Agent:

1. **Configure Email Provider**: Set up SMTP or email service credentials in `.env`
2. **Add AI Providers**: Configure OpenAI or Anthropic API keys for advanced AI features
3. **Database Setup**: Ensure PostgreSQL/MySQL database is configured
4. **Customize Templates**: Modify message templates in the AI service
5. **Set Up Scheduling**: Configure meeting scheduling integration

## Support

For issues or questions, please refer to the main documentation or contact support.

---

**Version**: 2.0  
**Last Updated**: March 2026
