import React from 'react';
import logo from './logo.svg';
import './App.css';
import { Avatar, Card, CardContent, CardHeader, Grid, List, ListItem, ListItemAvatar, ListItemText, Paper, Typography } from '@mui/material';
import BrightnessHighIcon from '@mui/icons-material/BrightnessHigh';

const App: React.FC = () => {
  return (
    <Grid container direction="row" justifyContent={'center'} alignItems="center" spacing={6}>
      <Grid item xs={8} />
      <Grid item xs={8}>

        <Card sx={{
          backgroundColor: "lightgray"
        }}>
          <CardHeader title={
            <Typography gutterBottom variant='h2' component="div">
              pyLEDControl
            </Typography>
          }>
          </CardHeader>
          <CardContent>
            <List sx={{ bgcolor: "background.paper" }}>
              <ListItem>
                <ListItemAvatar>
                  <Avatar>
                    <BrightnessHighIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText>
                  <Typography variant='h5'> Brightness</Typography>
                </ListItemText>
              </ListItem>
            </List>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={8} />
    </Grid>
  );
}

export default App;
