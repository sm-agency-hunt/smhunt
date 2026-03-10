import React, { useState } from 'react';
import { 
  AppBar, Toolbar, Typography, IconButton, Drawer, List, ListItem, 
  ListItemIcon, ListItemText, Box, Chip, Avatar, Menu, MenuItem, Divider
} from '@mui/material';
import { 
  Dashboard, Search, People, Mail, Assessment, Settings, 
  Menu as MenuIcon, AccountCircle, Logout, SmartToy
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const [profileAnchorEl, setProfileAnchorEl] = useState(null);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleProfileMenuOpen = (event) => {
    setProfileAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setProfileAnchorEl(null);
  };

  const handleLogout = () => {
    // Clear any auth data (for future implementation)
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // Show logout message
    alert('Logged out successfully!');
    
    // Navigate to dashboard or login page
    navigate('/');
    handleProfileMenuClose();
  };

  const handleProfile = () => {
    alert('Profile feature coming soon!');
    handleProfileMenuClose();
  };

  const menuItems = [
    { text: 'Dashboard', icon: <Dashboard />, path: '/' },
    { text: 'Lead Search', icon: <Search />, path: '/leads/search' },
    { text: 'AI Agent', icon: <SmartToy />, path: '/ai-agent' },
    { text: 'Leads', icon: <People />, path: '/leads' },
    { text: 'Outreach', icon: <Mail />, path: '/outreach' },
    { text: 'Analytics', icon: <Assessment />, path: '/analytics' },
    { text: 'Settings', icon: <Settings />, path: '/settings' },
  ];

  const drawer = (
    <Box onClick={handleDrawerToggle} sx={{ bgcolor: '#1976d2', height: '100%' }}>
      <Toolbar>
        <Typography variant="h6" sx={{ color: 'white', flexGrow: 1 }}>
          SMHUNT
        </Typography>
      </Toolbar>
      <List>
        {menuItems.map((item) => (
          <ListItem 
            button 
            key={item.text}
            onClick={() => {
              navigate(item.path);
              if (mobileOpen) handleDrawerToggle();
            }}
            sx={{ 
              '&:hover': { 
                bgcolor: 'rgba(255, 255, 255, 0.1)',
                color: 'white'
              },
              color: 'white'
            }}
          >
            <ListItemIcon sx={{ color: 'white' }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}>
            SMHUNT - AI Lead Generation Platform
          </Typography>
          
          <Chip 
            label="Production" 
            size="small" 
            color="success" 
            sx={{ mr: 2, display: { xs: 'none', sm: 'block' } }}
          />
          
          <Box sx={{ flexGrow: 1 }} />
          
          <IconButton color="inherit" onClick={() => navigate('/ai-agent')}>
            <SmartToy />
          </IconButton>
          
          <IconButton color="inherit" onClick={handleProfileMenuOpen}>
            <Avatar sx={{ width: 32, height: 32, bgcolor: '#fff', color: '#1976d2' }}>
              A
            </Avatar>
          </IconButton>
          
          <Menu
            anchorEl={profileAnchorEl}
            open={Boolean(profileAnchorEl)}
            onClose={handleProfileMenuClose}
          >
            <MenuItem onClick={handleProfile}>
              <ListItemIcon>
                <AccountCircle />
              </ListItemIcon>
              Profile
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <Logout />
              </ListItemIcon>
              Logout
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>
      
      <Box component="nav">
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 240 },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 240 },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
    </>
  );
};

export default Navbar;
