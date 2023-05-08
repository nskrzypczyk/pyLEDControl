import React from 'react';
import logo from './logo.svg';
import './App.css';
import { Avatar, Box, Card, CardContent, CardHeader, Divider, Grid, List, ListItem, ListItemAvatar, ListItemText, Paper, Slider, Stack, Typography, Button, Chip, withStyles, ChipTypeMap, Fab, AppBar, Toolbar, MenuItem, Container } from '@mui/material';
import BrightnessHighIcon from '@mui/icons-material/BrightnessHigh';
import { BrightnessLowRounded, Navigation, SendTimeExtension } from '@mui/icons-material';
import { OverridableComponent } from '@mui/material/OverridableComponent';

const App: React.FC = () => {
  const [brightness, setBrightness] = React.useState<number>(50);

  const handleBrigthnessChange = (event: Event, newValue: number | number[]) => {
    setBrightness(newValue as number);
  };

  const increaseBrightness = () => {
    let newVal = brightness + 10
    if (newVal > 100) {
      newVal = 100
    }
    setBrightness(newVal)
  }
  const decreaseBrightness = () => {
    let newVal = brightness - 10
    if (newVal < 0) {
      newVal = 0
    }
    setBrightness(newVal)
  }

  return (
    <div>
      <Box>

        <AppBar component={"nav"} position='static' >
          <Toolbar>
            <MenuItem>
              pyLEDControl
            </MenuItem>
          </Toolbar>
        </AppBar>
      </Box>
      <Card sx={{
        backgroundColor: "lightgray",
        flexGrow: 1
      }} style={{ borderRadius: "12px" }}>
        <CardContent>
          <Grid container direction="row" justifyContent="center" alignItems="stretch" columns={{ xs: 1, sm: 2, md: 2 }} spacing={{ xs: 2, md: 2 }}>
            <Grid item xs={1}>
              <Box style={{ borderRadius: "12px", backgroundColor: "white", padding: "10px" }}>
                <Grid container columns={3} direction="row" alignItems="center">
                  <Grid container item xs={1} >
                    <BrightnessHighIcon />
                  </Grid>
                  <Grid item xs="auto">
                    <Typography variant='h5'>
                      Brightness
                    </Typography>
                  </Grid>
                </Grid>
                <Divider sx={{ mt: 1.5, mb: 1.5 }} />
                <Stack spacing={1} direction="row" sx={{ mb: 1 }} alignItems="center">
                  <Button onClick={decreaseBrightness}>
                    <BrightnessLowRounded />
                  </Button>
                  <Slider aria-label="Volume" value={brightness} onChange={handleBrigthnessChange} />
                  <Button onClick={increaseBrightness}>
                    <BrightnessHighIcon />
                  </Button>
                </Stack>
                <Stack direction={'row'} spacing={1} alignItems="center" justifyContent={'center'}>
                  <Typography variant="h6">
                    {brightness} %
                  </Typography>
                </Stack>
              </Box>
            </Grid>
            <Grid item xs={1} justifyContent="center">
              <Box style={{ borderRadius: "12px", backgroundColor: "white", padding: "10px" }}>
                <Grid container columns={8} direction="row" alignItems="center">
                  <Grid container item xs={1}>
                    <SendTimeExtension />
                  </Grid>
                  <Grid item xs="auto">
                    <Typography variant='h5'>
                      Effect
                    </Typography>
                  </Grid>
                </Grid >
                <Divider sx={{ mt: 1.5, mb: 1.5 }} />
                <Grid container item spacing={1}>
                  {["Spotify", "Wave", "RainbowWave", "DigiClock", "RandomDot"].map((e) => (
                    <Grid key={e} item>
                      <Chip key={e} label={e} />
                    </Grid>
                  ))}
                </Grid>
              </Box>
            </Grid>
          </Grid>
        </CardContent >
      </Card >
      <Grid container columns={1} sx={{ position: "fixed", bottom: 10, width: "100%" }} justifyContent="center">
        <Grid item>
          <Fab variant="extended" color="primary" aria-label="add">
            <Navigation sx={{ mr: 1 }} />
            Update
          </Fab>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
