import { BrightnessLowRounded, Navigation, SendTimeExtension } from '@mui/icons-material';
import BrightnessHighIcon from '@mui/icons-material/BrightnessHigh';
import { AppBar, Box, Button, Card, CardContent, Chip, createTheme, Divider, Fab, Grid, MenuItem, Slider, Stack, ThemeProvider, Toolbar, Typography } from '@mui/material';
import * as colors from '@mui/material/colors';
import React from 'react';
import './App.css';

const App: React.FC = () => {
  const [brightness, setBrightness] = React.useState<number>(50);
  const [selectedChip, setSelectedChip] = React.useState<string>();
  const [effectList, setEffectList] = React.useState<string[]>(["Spotify", "Wave", "RainbowWave", "DigiClock", "RandomDot"]);


  const handleBrigthnessChange = (event: Event, newValue: number | number[]) => {
    setBrightness(newValue as number);
  };

  const handleEffectChip = (chipName: string) => {
    setSelectedChip(chipName)
  }

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
      <div className='main'>
        <AppBar position='static' color="primary" sx={{ borderRadius: "12px", marginBottom: "12px", marginTop: "12px", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)" }}>
          <Toolbar>
            <MenuItem>
              <Typography variant="h4" component="div" sx={{ flexGrow: 1 }}>
                pyLEDControl
              </Typography>
            </MenuItem>
          </Toolbar>
        </AppBar>
        <Grid container direction="row" justifyContent="center" alignItems="stretch" columns={{ xs: 1, sm: 2, md: 2 }} spacing={{ xs: 2, md: 2 }}>
          <Grid item xs={1}>
            <Box sx={{ borderRadius: "12px", padding: "10px", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)" }}>
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
            <Box sx={{ borderRadius: "12px", backgroundColor: "white", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)", padding: "10px" }}>
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
                {effectList.map((e) => (
                  <Grid key={e} item>
                    <Chip
                      key={e}
                      variant={selectedChip === e ? "filled" : "outlined"} label={e} onClick={() => handleEffectChip(e)}
                      color={selectedChip === e ? "primary" : undefined}
                    />
                  </Grid>
                ))}
              </Grid>
            </Box>
          </Grid>
        </Grid>
        <Grid container columns={1} sx={{ position: "fixed", bottom: 15, width: "100%" }} justifyContent="center">
          <Grid item>
            <Fab variant="extended" color="primary" aria-label="add">
              <Navigation sx={{ mr: 1 }} />
              Update
            </Fab>
          </Grid>
        </Grid>
      </div>
    </div >
  );
}

export default App;
