import React, { useState, useEffect } from 'react';
import { 
  AppBar, Toolbar, Typography, Container, Grid, Paper, 
  Box, CircularProgress, Chip, Card, CardContent, CardHeader
} from '@mui/material';
import { 
  Business, People, Mail, TrendingUp, 
  CalendarToday, Assessment, Assignment
} from '@mui/icons-material';
import axios from 'axios';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

function App() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch dashboard data
    const fetchDashboardData = async () => {
      try {
        // Using mock data for now until backend is connected
        setDashboardData({
          totalBusinesses: 1242,
          totalLeads: 893,
          totalOutreach: 654,
          conversionRate: 24.3,
          businessesByIndustry: [
            { name: 'Healthcare', value: 320 },
            { name: 'Technology', value: 280 },
            { name: 'Finance', value: 150 },
            { name: 'Retail', value: 120 },
            { name: 'Education', value: 90 },
          ],
          outreachStatus: [
            { name: 'Sent', value: 654 },
            { name: 'Opened', value: 312 },
            { name: 'Replied', value: 89 },
            { name: 'Converted', value: 45 },
          ],
          weeklyActivity: [
            { day: 'Mon', outreach: 45, meetings: 12 },
            { day: 'Tue', outreach: 52, meetings: 15 },
            { day: 'Wed', outreach: 38, meetings: 10 },
            { day: 'Thu', outreach: 61, meetings: 18 },
            { day: 'Fri', outreach: 49, meetings: 14 },
            { day: 'Sat', outreach: 32, meetings: 8 },
            { day: 'Sun', outreach: 28, meetings: 6 },
          ]
        });
        setLoading(false);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const StatCard = ({ title, value, icon, color }) => (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center">
          <Box mr={2} color={color}>
            {icon}
          </Box>
          <Box>
            <Typography variant="h6" component="div">
              {value}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {title}
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <div className="App">
      <AppBar position="static">
        <Toolbar>
          <Business sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            SMHUNT Admin Dashboard
          </Typography>
          <Chip label="Production" size="small" color="success" />
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Grid container spacing={3}>
          {/* Stats Cards */}
          <Grid item xs={12} sm={6} md={3}>
            <StatCard 
              title="Total Businesses" 
              value={dashboardData?.totalBusinesses || 0} 
              icon={<Business fontSize="large" />}
              color="#1976d2"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard 
              title="Total Leads" 
              value={dashboardData?.totalLeads || 0} 
              icon={<People fontSize="large" />}
              color="#388e3c"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard 
              title="Outreach Sent" 
              value={dashboardData?.totalOutreach || 0} 
              icon={<Mail fontSize="large" />}
              color="#f57c00"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard 
              title="Conversion Rate" 
              value={`${dashboardData?.conversionRate || 0}%`} 
              icon={<TrendingUp fontSize="large" />}
              color="#c2185b"
            />
          </Grid>

          {/* Industry Distribution */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2, height: 300 }}>
              <Typography variant="h6" gutterBottom>
                Businesses by Industry
              </Typography>
              <ResponsiveContainer width="100%" height="85%">
                <PieChart>
                  <Pie
                    data={dashboardData?.businessesByIndustry || []}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {dashboardData?.businessesByIndustry?.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>

          {/* Outreach Status */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2, height: 300 }}>
              <Typography variant="h6" gutterBottom>
                Outreach Status
              </Typography>
              <ResponsiveContainer width="100%" height="85%">
                <BarChart
                  data={dashboardData?.outreachStatus || []}
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>

          {/* Weekly Activity */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Weekly Activity
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart
                  data={dashboardData?.weeklyActivity || []}
                  margin={{
                    top: 20,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="outreach" fill="#8884d8" name="Outreach Messages" />
                  <Bar dataKey="meetings" fill="#82ca9d" name="Scheduled Meetings" />
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
}

export default App;