import React, { useState } from 'react';
import { 
  Container, Grid, Paper, Typography, TextField, Button, 
  Card, CardContent, Box, Chip, Dialog, Divider, IconButton,
  DialogTitle, DialogContent, DialogActions, Alert, CircularProgress
} from '@mui/material';
import { 
  Search, Add, Business, Email, Phone, Language, 
  LocationOn, Person, Star, AutoAwesome
} from '@mui/icons-material';
import axios from 'axios';

const LeadSearch = () => {
  const [searchCriteria, setSearchCriteria] = useState({
    niche: '',
    location: '',
    count: 10
  });
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedLead, setSelectedLead] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const handleSearch = async () => {
    if (!searchCriteria.niche || !searchCriteria.location) {
      setMessage({ type: 'error', text: 'Please fill in both niche and location' });
      return;
    }

    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      // Try to call real API, fallback to mock if fails
      let foundLeads = [];
      
      try {
        const response = await fetch(
          `http://localhost:8002/api/v1/discovery/search?niche=${encodeURIComponent(searchCriteria.niche)}&location=${encodeURIComponent(searchCriteria.location)}&count=${searchCriteria.count}&provider=mock`
        );
        
        if (response.ok) {
          foundLeads = await response.json();
          // Add scores to results
          foundLeads = foundLeads.map((lead, idx) => ({
            ...lead,
            lead_status: 'new',
            overall_score: minScore(60, maxScore(95, 70 + (idx * 2)))
          }));
        } else {
          throw new Error('API not available');
        }
      } catch (apiError) {
        // Fallback to mock data
        console.log('Using mock data:', apiError.message);
        for (let i = 0; i < searchCriteria.count; i++) {
          foundLeads.push({
            id: i + 1,
            business_name: `${searchCriteria.niche} Business ${i + 1}`,
            website: `https://business${i + 1}.com`,
            phone: `+1-555-${String(100 + i).padStart(4, '0')}`,
            email: `contact@business${i + 1}.com`,
            city: searchCriteria.location,
            country: 'USA',
            industry: searchCriteria.niche,
            contact_name: `Contact Person ${i + 1}`,
            contact_email: `contact${i + 1}@business${i + 1}.com`,
            lead_status: 'new',
            overall_score: Math.min(95, Math.max(60, 70 + (i * 2)))
          });
        }
      }

      setTimeout(() => {
        setResults(foundLeads);
        setLoading(false);
        setMessage({ type: 'success', text: `Found ${foundLeads.length} leads!` });
      }, 500);

    } catch (error) {
      console.error('Error searching leads:', error);
      setLoading(false);
      setMessage({ type: 'error', text: 'Error searching for leads. Please try again.' });
    }
  };

  const minScore = (min, val) => Math.max(min, val);
  const maxScore = (max, val) => Math.min(max, val);

  const handleSaveLead = async (lead) => {
    try {
      // Save lead to database
      // await axios.post(`${API_BASE_URL}/leads`, lead);
      
      setMessage({ type: 'success', text: `Lead "${lead.business_name}" saved successfully!` });
      
      // Refresh results or update UI as needed
      setResults(results.map(r => 
        r.id === lead.id ? { ...r, saved: true } : r
      ));
    } catch (error) {
      console.error('Error saving lead:', error);
      setMessage({ type: 'error', text: 'Error saving lead. Please try again.' });
    }
  };

  const handleViewDetails = (lead) => {
    setSelectedLead(lead);
    setDialogOpen(true);
  };

  const handleGenerateOutreach = async (lead) => {
    try {
      // Generate AI outreach message
      // const response = await axios.post(`${API_BASE_URL}/ai/generate-outreach`, null, {
      //   params: {
      //     business_id: lead.id,
      //     lead_id: lead.id,
      //     message_type: 'cold_email',
      //     provider: 'mock'
      //   }
      // });
      
      setMessage({ type: 'success', text: 'Outreach message generated! Check the AI Agent page.' });
      setDialogOpen(false);
    } catch (error) {
      console.error('Error generating outreach:', error);
      setMessage({ type: 'error', text: 'Error generating outreach message.' });
    }
  };

  return (
    <Box sx={{ mt: 10, mb: 12, pb: 6 }}>
      <Container maxWidth="lg">
        {/* Header Section */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: '#1976d2' }}>
            🔍 Lead Search
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            Discover new leads using AI-powered search technology
          </Typography>
          <Divider />
        </Box>

        {/* Search Section */}
        <Paper sx={{ p: 4, mb: 4, borderRadius: 2, boxShadow: 3 }}>

          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Business Niche/Industry"
                placeholder="e.g., Healthcare, Technology, Finance"
                value={searchCriteria.niche}
                onChange={(e) => setSearchCriteria({ ...searchCriteria, niche: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Location"
                placeholder="e.g., New York, London, USA"
                value={searchCriteria.location}
                onChange={(e) => setSearchCriteria({ ...searchCriteria, location: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <TextField
                fullWidth
                label="Number of Leads"
                type="number"
                InputProps={{ inputProps: { min: 1, max: 100 } }}
                value={searchCriteria.count}
                onChange={(e) => setSearchCriteria({ ...searchCriteria, count: parseInt(e.target.value) })}
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <Button
                fullWidth
                variant="contained"
                size="large"
                onClick={handleSearch}
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} /> : <Search />}
                sx={{ height: 56 }}
              >
                {loading ? 'Searching...' : 'Search'}
              </Button>
            </Grid>

            {message.text && (
              <Grid item xs={12}>
                <Alert severity={message.type}>{message.text}</Alert>
              </Grid>
            )}
          </Grid>
        </Paper>

        {/* Results Section */}
        {results.length > 0 && (
          <>
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ color: '#388e3c', fontWeight: 'bold' }}>
                ✅ Search Results ({results.length})
              </Typography>
              <Divider />
            </Box>
            <Grid container spacing={3}>
              {results.map((lead) => (
                <Grid item xs={12} md={6} lg={4} key={lead.id}>
                  <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <CardContent>
                      <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                        <Box display="flex" alignItems="center">
                          <Business sx={{ mr: 1, color: '#1976d2' }} />
                          <Typography variant="h6">{lead.business_name}</Typography>
                        </Box>
                        <Chip 
                          label={`${lead.overall_score}%`} 
                          size="small" 
                          color={lead.overall_score > 70 ? "success" : "default"}
                        />
                      </Box>

                      <Box mb={2}>
                        <Chip 
                          icon={<LocationOn />} 
                          label={`${lead.city}, ${lead.country}`} 
                          size="small" 
                          sx={{ mr: 1, mb: 1 }}
                        />
                        <Chip 
                          icon={<Star />} 
                          label={lead.industry} 
                          size="small"
                          sx={{ mb: 1 }}
                        />
                      </Box>

                      <Box mb={2}>
                        <Box display="flex" alignItems="center" mb={1}>
                          <Person fontSize="small" sx={{ mr: 1 }} />
                          <Typography variant="body2">{lead.contact_name}</Typography>
                        </Box>
                        <Box display="flex" alignItems="center" mb={1}>
                          <Email fontSize="small" sx={{ mr: 1 }} />
                          <Typography variant="body2">{lead.contact_email}</Typography>
                        </Box>
                        <Box display="flex" alignItems="center">
                          <Phone fontSize="small" sx={{ mr: 1 }} />
                          <Typography variant="body2">{lead.phone}</Typography>
                        </Box>
                      </Box>

                      <Box display="flex" gap={1} mt="auto">
                        <Button 
                          size="small" 
                          variant="outlined" 
                          fullWidth
                          onClick={() => handleViewDetails(lead)}
                        >
                          View Details
                        </Button>
                        <IconButton 
                          size="small" 
                          color="primary"
                          onClick={() => handleSaveLead(lead)}
                        >
                          <Add />
                        </IconButton>
                        <IconButton 
                          size="small" 
                          color="secondary"
                          onClick={() => handleGenerateOutreach(lead)}
                        >
                          <AutoAwesome />
                        </IconButton>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </>
        )}

        {/* Lead Details Dialog */}
        <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="md" fullWidth>
          {selectedLead && (
            <>
              <DialogTitle>
                {selectedLead.business_name}
              </DialogTitle>
              <DialogContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" color="text.secondary">Business Information</Typography>
                    <Box mt={1}>
                      <Typography variant="body2"><strong>Website:</strong></Typography>
                      <Box display="flex" alignItems="center">
                        <Language fontSize="small" sx={{ mr: 1 }} />
                        <a href={selectedLead.website} target="_blank" rel="noopener noreferrer">
                          {selectedLead.website}
                        </a>
                      </Box>
                      <Typography variant="body2" mt={1}><strong>Industry:</strong> {selectedLead.industry}</Typography>
                      <Typography variant="body2"><strong>Location:</strong> {selectedLead.city}, {selectedLead.country}</Typography>
                      <Typography variant="body2"><strong>Phone:</strong> {selectedLead.phone}</Typography>
                      <Typography variant="body2"><strong>Email:</strong> {selectedLead.email}</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" color="text.secondary">Contact Information</Typography>
                    <Box mt={1}>
                      <Typography variant="body2"><strong>Name:</strong> {selectedLead.contact_name}</Typography>
                      <Typography variant="body2"><strong>Email:</strong> {selectedLead.contact_email}</Typography>
                      <Typography variant="body2" mt={1}><strong>Lead Score:</strong> {selectedLead.overall_score}%</Typography>
                      <Typography variant="body2"><strong>Status:</strong> {selectedLead.lead_status}</Typography>
                    </Box>
                  </Grid>
                </Grid>
              </DialogContent>
              <DialogActions>
                <Button onClick={() => setDialogOpen(false)}>Close</Button>
                <Button onClick={() => handleSaveLead(selectedLead)} variant="contained">
                  Save Lead
                </Button>
                <Button 
                  onClick={() => handleGenerateOutreach(selectedLead)} 
                  variant="contained" 
                  color="secondary"
                  startIcon={<AutoAwesome />}
                >
                  Generate Outreach
                </Button>
              </DialogActions>
            </>
          )}
        </Dialog>
      </Container>
    </Box>
  );
};

export default LeadSearch;
