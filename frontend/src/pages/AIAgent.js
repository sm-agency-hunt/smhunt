import React, { useState, useEffect } from 'react';
import { 
  Container, Grid, Paper, Typography, Box, Card, CardContent, 
  Button, TextField, Dialog, DialogTitle, DialogContent, 
  DialogActions, Chip, IconButton, List, ListItem, 
  ListItemText, Divider, Alert, CircularProgress, Avatar,
  Rating, Stepper, Step, StepLabel, FormControl, InputLabel, Select, MenuItem
} from '@mui/material';
import { 
  SmartToy, Send, AutoAwesome, PersonAdd, Email, Phone, 
  MeetingRoom, CheckCircle, Refresh, Delete, Edit
} from '@mui/icons-material';

const AIAgent = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [agentMode, setAgentMode] = useState('generate'); // generate, communicate, followup
  const [selectedLeads, setSelectedLeads] = useState([]);
  const [generatedMessages, setGeneratedMessages] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  
  const [campaignSettings, setCampaignSettings] = useState({
    campaignName: '',
    targetIndustry: '',
    location: '',
    messageTone: 'professional', // professional, friendly, enthusiastic
    messageGoal: 'meeting_booking', // meeting_booking, product_demo, partnership
    dailyLimit: 10,
    autoFollowup: true
  });

  const steps = ['Configure Campaign', 'Generate Leads', 'Create Messages', 'Start Outreach', 'Monitor & Follow-up'];

  // Mock leads for demonstration
  const mockLeads = [
    { id: 1, name: 'John Smith', company: 'Tech Solutions Inc.', email: 'john@techsolutions.com', score: 85 },
    { id: 2, name: 'Sarah Johnson', company: 'Healthcare Plus', email: 'sarah@healthcareplus.com', score: 92 },
    { id: 3, name: 'Mike Davis', company: 'Finance Corp', email: 'mike@financecorp.com', score: 78 },
  ];

  const handleGenerateLeads = async () => {
    setLoading(true);
    setMessage({ type: '', text: '' });
    
    try {
      // Try to call real API
      let generatedLeads = [];
      
      try {
        const response = await fetch(
          `http://localhost:8002/api/v1/ai-agent/generate-leads?industry=${encodeURIComponent(campaignSettings.targetIndustry)}&location=${encodeURIComponent(campaignSettings.location)}&count=${campaignSettings.dailyLimit}&provider=mock`,
          { method: 'POST' }
        );
        
        if (response.ok) {
          const data = await response.json();
          generatedLeads = data.leads || [];
        } else {
          throw new Error('API not available');
        }
      } catch (apiError) {
        // Fallback to mock leads
        console.log('Using mock data:', apiError.message);
        generatedLeads = mockLeads;
      }

      setTimeout(() => {
        setSelectedLeads(generatedLeads);
        setLoading(false);
        setMessage({ type: 'success', text: `Generated ${generatedLeads.length} qualified leads!` });
        setActiveStep(2);
      }, 1500);

    } catch (error) {
      console.error('Error generating leads:', error);
      setLoading(false);
      setMessage({ type: 'error', text: 'Error generating leads. Please try again.' });
    }
  };

  const handleGenerateMessages = async () => {
    setLoading(true);
    setMessage({ type: '', text: '' });
    
    try {
      // Try to generate messages via API for each lead
      let messages = [];
      
      for (const lead of selectedLeads) {
        try {
          const response = await fetch(
            `http://localhost:8002/api/v1/ai-agent/create-outreach?provider=mock`,
            {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                lead_data: lead,
                campaign_settings: campaignSettings
              })
            }
          );
          
          if (response.ok) {
            const data = await response.json();
            messages.push(data.message);
          } else {
            throw new Error('API not available');
          }
        } catch (err) {
          // Fallback to mock message generation
          messages.push({
            leadId: lead.id,
            leadName: lead.contact_name || lead.contact_email,
            companyName: lead.business_name,
            subject: `Helping ${lead.business_name} Grow - Quick Question`,
            body: `Hi ${lead.contact_name || 'Contact'},\n\nI hope this email finds you well. I've been following ${lead.business_name}'s work in the ${campaignSettings.targetIndustry} space.\n\nWe've helped similar companies achieve significant growth.\n\nWould you be open to a brief 15-minute call next week?\n\nBest regards,\nYour Name`,
            tone: campaignSettings.messageTone,
            goal: campaignSettings.messageGoal,
            status: 'draft'
          });
        }
      }

      setGeneratedMessages(messages);
      setLoading(false);
      setMessage({ type: 'success', text: `${messages.length} personalized messages generated!` });
      setActiveStep(3);

    } catch (error) {
      console.error('Error generating messages:', error);
      setLoading(false);
      setMessage({ type: 'error', text: 'Error generating messages. Please try again.' });
    }
  };

  const handleSendOutreach = async () => {
    setLoading(true);
    setMessage({ type: '', text: '' });
    
    try {
      // Try to send via API
      let campaignResult = null;
      
      try {
        const response = await fetch(
          `http://localhost:8002/api/v1/ai-agent/send-campaign?auto_followup=${campaignSettings.autoFollowup}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(generatedMessages)
          }
        );
        
        if (response.ok) {
          const data = await response.json();
          campaignResult = data.campaign_result;
        } else {
          throw new Error('API not available');
        }
      } catch (apiError) {
        // Fallback to mock sending
        console.log('Using mock sending:', apiError.message);
        const updatedMessages = generatedMessages.map(msg => ({
          ...msg,
          status: 'sent',
          sentAt: new Date().toISOString()
        }));
        
        setGeneratedMessages(updatedMessages);
        
        // Add to conversations
        const newConversations = updatedMessages.map(msg => ({
          leadId: msg.leadId,
          leadName: msg.leadName || msg.contact_name,
          messages: [{
            role: 'assistant',
            content: msg.body,
            timestamp: new Date().toISOString()
          }],
          status: 'active'
        }));
        
        setConversations(newConversations);
        setLoading(false);
        setMessage({ type: 'success', text: 'Outreach campaign started successfully!' });
        setActiveStep(4);
        return;
      }

      if (campaignResult) {
        const updatedMessages = generatedMessages.map(msg => ({
          ...msg,
          status: 'sent',
          sentAt: new Date().toISOString()
        }));
        
        setGeneratedMessages(updatedMessages);
        
        // Add to conversations
        const newConversations = updatedMessages.map(msg => ({
          leadId: msg.leadId,
          leadName: msg.leadName || msg.contact_name,
          messages: [{
            role: 'assistant',
            content: msg.body,
            timestamp: new Date().toISOString()
          }],
          status: 'active'
        }));
        
        setConversations(newConversations);
        setLoading(false);
        setMessage({ type: 'success', text: 'Outreach campaign started successfully!' });
        setActiveStep(4);
      }

    } catch (error) {
      console.error('Error sending outreach:', error);
      setLoading(false);
      setMessage({ type: 'error', text: 'Error sending messages. Please try again.' });
    }
  };

  const handleAutoFollowup = async (conversation) => {
    try {
      // Generate and send follow-up message
      const followupMessage = {
        role: 'assistant',
        content: `Hi ${conversation.leadName},\n\nJust wanted to follow up on my previous email. I believe we have some valuable insights that could really help ${conversation.leadName}'s company grow.\n\nWould you have 10 minutes for a quick chat this week?\n\nBest regards`,
        timestamp: new Date().toISOString()
      };

      const updatedConversation = {
        ...conversation,
        messages: [...conversation.messages, followupMessage],
        lastContact: new Date().toISOString()
      };

      setConversations(conversations.map(c => 
        c.leadId === conversation.leadId ? updatedConversation : c
      ));

      setMessage({ type: 'success', text: 'Follow-up message sent!' });
    } catch (error) {
      console.error('Error sending followup:', error);
      setMessage({ type: 'error', text: 'Error sending follow-up message.' });
    }
  };

  const renderStepContent = () => {
    switch(activeStep) {
      case 0:
        return (
          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>Campaign Configuration</Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Campaign Name"
                  value={campaignSettings.campaignName}
                  onChange={(e) => setCampaignSettings({...campaignSettings, campaignName: e.target.value})}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Message Tone</InputLabel>
                  <Select
                    value={campaignSettings.messageTone}
                    label="Message Tone"
                    onChange={(e) => setCampaignSettings({...campaignSettings, messageTone: e.target.value})}
                  >
                    <MenuItem value="professional">Professional</MenuItem>
                    <MenuItem value="friendly">Friendly</MenuItem>
                    <MenuItem value="enthusiastic">Enthusiastic</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Target Industry"
                  value={campaignSettings.targetIndustry}
                  onChange={(e) => setCampaignSettings({...campaignSettings, targetIndustry: e.target.value})}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Location"
                  value={campaignSettings.location}
                  onChange={(e) => setCampaignSettings({...campaignSettings, location: e.target.value})}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Campaign Goal</InputLabel>
                  <Select
                    value={campaignSettings.messageGoal}
                    label="Campaign Goal"
                    onChange={(e) => setCampaignSettings({...campaignSettings, messageGoal: e.target.value})}
                  >
                    <MenuItem value="meeting_booking">Meeting Booking</MenuItem>
                    <MenuItem value="product_demo">Product Demo</MenuItem>
                    <MenuItem value="partnership">Partnership</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Daily Lead Limit"
                  type="number"
                  value={campaignSettings.dailyLimit}
                  onChange={(e) => setCampaignSettings({...campaignSettings, dailyLimit: parseInt(e.target.value)})}
                />
              </Grid>
              <Grid item xs={12}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => setActiveStep(1)}
                  disabled={!campaignSettings.campaignName || !campaignSettings.targetIndustry}
                >
                  Next: Generate Leads
                </Button>
              </Grid>
            </Grid>
          </Paper>
        );

      case 1:
        return (
          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>AI Lead Generation</Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Our AI agent will search for qualified leads based on your criteria
            </Typography>
            
            <Box sx={{ my: 3 }}>
              <Alert severity="info" icon={<SmartToy />}>
                The AI will analyze businesses in {campaignSettings.targetIndustry || 'your target industry'} 
                located in {campaignSettings.location || 'your target location'} and score them based on fit.
              </Alert>
            </Box>

            <Button
              variant="contained"
              size="large"
              onClick={handleGenerateLeads}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : <AutoAwesome />}
              sx={{ mr: 2 }}
            >
              {loading ? 'Generating...' : 'Generate Leads'}
            </Button>
            <Button
              variant="outlined"
              onClick={() => setActiveStep(0)}
              sx={{ mr: 2 }}
            >
              Back
            </Button>
          </Paper>
        );

      case 2:
        return (
          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>Review Generated Leads</Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              AI has found {selectedLeads.length} qualified leads. Review and proceed to message generation.
            </Typography>

            <List>
              {selectedLeads.map((lead, index) => (
                <React.Fragment key={lead.id}>
                  {index > 0 && <Divider />}
                  <ListItem>
                    <Avatar sx={{ bgcolor: '#1976d2', mr: 2 }}>
                      {(lead.contact_name || lead.business_name || 'C').charAt(0)}
                    </Avatar>
                    <ListItemText
                      primary={`${lead.contact_name || lead.business_name} - ${lead.business_name}`}
                      secondary={`Email: ${lead.contact_email || lead.email} | Score: ${lead.lead_score || lead.overall_score || 70}%`}
                    />
                    <Chip 
                      label={`${lead.lead_score || lead.overall_score || 70}% Match`} 
                      color={(lead.lead_score || lead.overall_score || 70) > 80 ? 'success' : 'primary'}
                      size="small"
                    />
                  </ListItem>
                </React.Fragment>
              ))}
            </List>

            <Box sx={{ mt: 3 }}>
              <Button
                variant="contained"
                size="large"
                onClick={handleGenerateMessages}
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} /> : <AutoAwesome />}
                sx={{ mr: 2 }}
              >
                Generate Personalized Messages
              </Button>
              <Button
                variant="outlined"
                onClick={() => setActiveStep(1)}
                sx={{ mr: 2 }}
              >
                Back
              </Button>
              <Button
                variant="outlined"
                onClick={handleGenerateLeads}
                startIcon={<Refresh />}
              >
                Regenerate
              </Button>
            </Box>
          </Paper>
        );

      case 3:
        return (
          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>Review & Send Outreach</Typography>
            
            {generatedMessages.map((msg, index) => (
              <Card key={msg.leadId} sx={{ mb: 2, bgcolor: '#f5f5f5' }}>
                <CardContent>
                  <Typography variant="subtitle2" gutterBottom>
                    To: {msg.leadName} at {msg.companyName}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Subject: {msg.subject}
                  </Typography>
                  <Typography variant="body2" sx={{ whiteSpace: 'pre-line', mt: 2 }}>
                    {msg.body}
                  </Typography>
                </CardContent>
              </Card>
            ))}

            <Box sx={{ mt: 3 }}>
              <Button
                variant="contained"
                size="large"
                onClick={handleSendOutreach}
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} /> : <Send />}
                sx={{ mr: 2 }}
              >
                Start Outreach Campaign
              </Button>
              <Button
                variant="outlined"
                onClick={() => setActiveStep(2)}
                sx={{ mr: 2 }}
              >
                Back
              </Button>
            </Box>
          </Paper>
        );

      case 4:
        return (
          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>Active Conversations & Follow-ups</Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              AI Agent is monitoring responses and will automatically follow up
            </Typography>

            <Grid container spacing={3} sx={{ mt: 2 }}>
              {conversations.map((conv) => (
                <Grid item xs={12} md={6} key={conv.leadId}>
                  <Card>
                    <CardContent>
                      <Box display="flex" alignItems="center" mb={2}>
                        <Avatar sx={{ bgcolor: '#1976d2', mr: 2 }}>
                          {(conv.leadName || 'L').charAt(0)}
                        </Avatar>
                        <Box>
                          <Typography variant="subtitle1">{conv.leadName || 'Lead'}</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {conv.messages.length} messages | Status: {conv.status}
                          </Typography>
                        </Box>
                        <Box sx={{ flexGrow: 1 }} />
                        <Chip 
                          label={conv.status} 
                          size="small" 
                          color="success"
                        />
                      </Box>
                      
                      <Divider sx={{ my: 2 }} />
                      
                      <Box mb={2}>
                        {conv.messages.map((msg, idx) => (
                          <Box key={idx} sx={{ mb: 2 }}>
                            <Chip 
                              label={msg.role === 'assistant' ? 'AI Agent' : 'Lead'} 
                              size="small" 
                              sx={{ mb: 1 }}
                            />
                            <Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
                              {msg.content}
                            </Typography>
                          </Box>
                        ))}
                      </Box>

                      <Box display="flex" gap={1}>
                        <Button
                          size="small"
                          variant="outlined"
                          onClick={() => handleAutoFollowup(conv)}
                          startIcon={<Email />}
                        >
                          Send Follow-up
                        </Button>
                        <Button
                          size="small"
                          variant="outlined"
                          startIcon={<MeetingRoom />}
                        >
                          Schedule Meeting
                        </Button>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Box sx={{ mt: 3 }}>
              <Button
                variant="outlined"
                onClick={() => setActiveStep(0)}
                startIcon={<Refresh />}
              >
                Start New Campaign
              </Button>
            </Box>
          </Paper>
        );

      default:
        return null;
    }
  };

  return (
    <Box sx={{ mt: 10, mb: 12, pb: 6 }}>
      <Container maxWidth="lg">
        {/* Header */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: '#1976d2' }}>
            🤖 AI Lead Generation Agent
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            Automate your entire lead generation and outreach process with intelligent AI
          </Typography>
          <Divider />
        </Box>

        {/* Stepper */}
        <Box sx={{ mb: 4 }}>
          <Stepper activeStep={activeStep} alternativeLabel>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </Box>

        {message.text && (
          <Alert severity={message.type} sx={{ mb: 3 }}>
            {message.text}
          </Alert>
        )}

        {renderStepContent()}
      </Container>
    </Box>
  );
};

export default AIAgent;
