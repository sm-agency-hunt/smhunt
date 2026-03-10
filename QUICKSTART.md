# 🚀 Quick Start Guide - SMHUNT AI Lead Generation Platform

## Installation (5 Minutes)

### Step 1: Install Frontend Dependencies
```bash
cd frontend
npm install
```

### Step 2: Start Frontend
```bash
npm start
```
✅ Opens at http://localhost:3000

### Step 3: Start Backend (New Terminal)
```bash
# In project root directory
python main.py
```
✅ API runs at http://localhost:8000

---

## First Campaign (2 Minutes)

### 1. Navigate to AI Agent
- Click **"AI Agent"** in left sidebar
- You'll see the 5-step wizard

### 2. Configure Campaign
Fill in the form:
```
Campaign Name: My First Campaign
Target Industry: Healthcare
Location: New York
Message Tone: Professional
Goal: Meeting Booking
Daily Limit: 10
```
Click **"Next: Generate Leads"**

### 3. Generate Leads
- Wait for AI to find businesses (~2 seconds)
- Review the qualified leads
- Each lead shows:
  - Business name
  - Contact person
  - Email & phone
  - Match score %
  
Click **"Generate Personalized Messages"**

### 4. Review Messages
- AI creates custom message for each lead
- Subject lines are personalized
- Content references specific business
- Tone matches your selection

Click **"Start Outreach Campaign"**

### 5. Launch!
- Messages are sent automatically
- Watch real-time statistics
- Track sent/failed/delivered

### 6. Monitor Responses
- View active conversations
- AI analyzes sentiment
- See recommended actions
- Send follow-ups with one click

---

## Search Specific Leads (1 Minute)

### Use Lead Search Page:
1. Click **"Lead Search"** in sidebar
2. Enter criteria:
   ```
   Niche: Technology Companies
   Location: San Francisco
   Count: 20
   ```
3. Click **"Search"**
4. Browse results
5. Click any card to view details
6. Save or generate outreach instantly

---

## Dashboard Overview

Your dashboard shows:
- 📊 **Total Businesses**: All companies in database
- 👥 **Total Leads**: Qualified prospects
- 📧 **Outreach Sent**: Messages delivered
- 📈 **Conversion Rate**: Success percentage
- 🥧 **Industry Chart**: Distribution by sector
- 📊 **Activity Chart**: Weekly performance

---

## Keyboard Shortcuts

- `Ctrl + K` - Quick search (coming soon)
- `Ctrl + /` - Open help
- `Esc` - Close dialogs

---

## Common Tasks

### Add Single Lead Manually:
1. Go to "Leads" section
2. Click "+ Add Lead"
3. Fill form
4. Save

### Create Quick Outreach:
1. Search for a lead
2. Click the robot icon 🤖
3. AI generates message
4. Review and send

### Check Campaign Status:
1. Go to "AI Agent"
2. View active campaigns
3. Click campaign name for details

---

## Tips for Best Results

### ✅ Do's:
- Be specific with industry targeting
- Use professional tone for B2B
- Set reasonable daily limits (10-20)
- Review AI messages before sending
- Enable auto follow-up
- Monitor sentiment scores

### ❌ Don'ts:
- Don't spam (respect daily limits)
- Don't use overly casual tone for corporate
- Don't ignore negative responses
- Don't send without reviewing

---

## Understanding AI Scores

**Lead Score 80-100%** ⭐⭐⭐
- Highly qualified
- Complete information
- Priority contact

**Lead Score 60-79%** ⭐⭐
- Good potential
- Some info missing
- Worth pursuing

**Lead Score <60%** ⭐
- Early stage
- Limited data
- Nurture campaign

---

## Response Types

When leads respond, AI categorizes:

🟢 **Interested** → High priority
- Wants meeting
- Asking questions
- Positive sentiment

🔴 **Not Interested** → Low priority
- Explicitly declined
- Negative sentiment
- Mark unqualified

🟡 **More Info** → Medium priority
- Requesting details
- Neutral sentiment
- Send resources

⚪ **Out of Office** → Medium priority
- Auto-responder
- Follow up later
- Wait 3-5 days

---

## Troubleshooting

### Frontend won't start:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Backend errors:
```bash
# Check Python version (need 3.9+)
python --version

# Reinstall dependencies
pip install -r requirements.txt
```

### Can't access localhost:3000:
- Check if port is in use
- Try different browser
- Clear cache (Ctrl+Shift+Delete)

### API not responding:
- Verify backend is running
- Check terminal for errors
- Ensure port 8000 is free

---

## API Testing

Use Swagger UI to test endpoints:
1. Go to http://localhost:8000/docs
2. Authenticate (if needed)
3. Try any endpoint
4. See request/response formats

Example: Test lead generation
```
POST /api/v1/ai-agent/generate-leads
{
  "industry": "Technology",
  "location": "London",
  "count": 5
}
```

---

## Customization

### Change Brand Colors:
Edit `frontend/src/components/Navbar.js`
```javascript
sx={{ bgcolor: '#YOUR_COLOR' }}
```

### Modify Message Templates:
Edit `src/services/ai/ai_lead_agent.py`
Find `_create_body_prompt()` method

### Adjust Scoring:
Edit `src/services/ai/ai_lead_agent.py`
Modify `_score_lead()` method

---

## Data Export

Coming soon:
- CSV export for leads
- PDF campaign reports
- Email templates download

---

## Support Resources

📧 **Email**: support@smhunt.online  
📖 **Docs**: /FEATURES.md  
🐛 **Issues**: GitHub Issues  
💬 **Chat**: Coming soon  

---

## What's Next?

After mastering basics:
1. ✅ Set up email provider integration
2. ✅ Configure AI providers (OpenAI/Claude)
3. ✅ Connect calendar for meetings
4. ✅ Create custom message templates
5. ✅ Set up analytics tracking
6. ✅ Build email sequences

---

## Success Metrics

Track these KPIs:
- **Open Rate**: Target 40-60%
- **Reply Rate**: Target 10-20%
- **Meeting Rate**: Target 2-5%
- **Conversion Rate**: Target 1-3%

Dashboard updates in real-time as campaigns progress.

---

## Quick Reference Card

```
┌─────────────────────────────────────┐
│  SMHUNT Quick Commands              │
├─────────────────────────────────────┤
│  Dashboard     → /                  │
│  Lead Search   → /leads/search      │
│  AI Agent      → /ai-agent          │
│  Analytics     → /analytics         │
│                                     │
│  New Campaign  → AI Agent → Config  │
│  Search Leads  → Lead Search        │
│  View Reports  → Dashboard          │
└─────────────────────────────────────┘
```

---

## 🎉 You're Ready!

Your SMHUNT platform is fully configured and ready to generate leads!

**Start your first campaign now!** 🚀

---

**Need Help?**
- Check SUMMARY.md for detailed info
- Read FEATURES.md for complete documentation
- Visit /docs for API reference
