import React from 'react';
import logo from './logo.svg';
import './App.css';
import { Avatar, Box, Card, CardContent, CardHeader, Divider, Grid, List, ListItem, ListItemAvatar, ListItemText, Paper, Slider, Stack, Typography, Button, Chip } from '@mui/material';
import BrightnessHighIcon from '@mui/icons-material/BrightnessHigh';
import { BrightnessLowRounded, SendTimeExtension } from '@mui/icons-material';


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
            <Grid container direction="row" justifyContent={'space-evenly'} alignItems="stretch" xs={12} spacing={6}>
              <Grid item xs={6}>
                <Box style={{ borderRadius: "12px", backgroundColor: "white", padding: "10px" }}>
                  <Stack direction={'row'} spacing={2} alignItems="center" justifyContent={'center'}>
                    <BrightnessHighIcon />
                    <Typography variant='h5'>
                      Brightness
                    </Typography>
                  </Stack >
                  <Divider sx={{ mt: 1.5, mb: 1.5 }} />
                  <Stack spacing={2} direction="row" sx={{ mb: 1 }} alignItems="center">
                    <Button onClick={decreaseBrightness}>
                      <BrightnessLowRounded />
                    </Button>
                    <Slider aria-label="Volume" value={brightness} onChange={handleBrigthnessChange} />
                    <Button onClick={increaseBrightness}>
                      <BrightnessHighIcon />
                    </Button>
                  </Stack>
                  <Stack direction={'row'} spacing={2} alignItems="center" justifyContent={'center'}>
                    <Typography variant="h6">
                      {brightness} %
                    </Typography>
                  </Stack>
                </Box>
              </Grid>
              <Grid item xs={6}>
                <Box style={{ borderRadius: "12px", backgroundColor: "white", padding: "10px" }}>
                  <Stack direction={'row'} spacing={2} alignItems="center" justifyContent={'center'}>
                    <SendTimeExtension />
                    <Typography variant='h5'>
                      Effect
                    </Typography>
                  </Stack >
                  <Divider sx={{ mt: 1.5, mb: 1.5 }} />
                  <Stack direction="row" spacing={1} justifyContent="center">
                    <Chip label="Spotify" />
                    <Chip label="Wave" />
                    <Chip label="RainbowWave" />
                    <Chip label="RandomDot" />
                    <Chip label="DigiClock" />
                  </Stack>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={8} />
    </Grid>
  );
}

export default App;
