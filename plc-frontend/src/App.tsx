import { BrightnessLowRounded, Navigation, SendTimeExtension } from '@mui/icons-material';
import BrightnessHighIcon from '@mui/icons-material/BrightnessHigh';
import { Alert, AlertColor, AppBar, Box, Button, Chip, Divider, Fab, Grid, MenuItem, Slide, Slider, Snackbar, Stack, Toolbar, Typography } from '@mui/material';
import { TransitionProps } from '@mui/material/transitions';
import React from 'react';
import { getStatus, setEffect } from './api/ApiManager';
import './App.css';
import { IEffectData } from './domainData/DomainData';


const App: React.FC = () => {
  const [brightness, setBrightness] = React.useState<number>(50);
  const [selectedEffect, setSelectedEffect] = React.useState<string>();
  const [effectList, setEffectList] = React.useState<string[]>(["Spotify", "Wave", "RainbowWave", "DigiClock", "RandomDot"]);
  const [sbState, setSbState] = React.useState<{
    open: boolean;
    Transition: React.ComponentType<
      TransitionProps & {
        children: React.ReactElement<any, any>;
      }
    >;
    message: string;
    severity: AlertColor
  }>({
    open: false,
    Transition: Slide,
    message: "",
    severity: 'info'
  });

  const handleBrigthnessChange = (event: Event, newValue: number | number[]) => {
    setBrightness(newValue as number);
  };

  const handleEffectChip = (chipName: string) => {
    setSelectedEffect(chipName)
  }

  const handleClickUpdate = async () => {
    try {
      await setEffect({ effect: selectedEffect!, brightness: brightness })
    } catch (error: any) {
      setSbState({ ...sbState, open: true, message: error.message, severity: "error" })
    }
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

  React.useEffect(() => {
    const fn = async () => {
      try {
        const res: IEffectData = await getStatus()
        setBrightness(res.brightness)
        setSelectedEffect(res.effect)
      } catch (error) {
        setSbState({ ...sbState, open: true, message: String(error), severity: "error" })
      }
    }
    fn()
  }, [])

  return (
    <>
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
                      variant={selectedEffect === e ? "filled" : "outlined"} label={e} onClick={() => handleEffectChip(e)}
                      color={selectedEffect === e ? "primary" : undefined}
                    />
                  </Grid>
                ))}
              </Grid>
            </Box>
          </Grid>
        </Grid>
        <Grid container columns={1} sx={{ position: "fixed", bottom: 15, width: "100%" }} justifyContent="center">
          <Grid item>
            <Fab variant="extended" color="primary" aria-label="add" onClick={handleClickUpdate}>
              <Navigation sx={{ mr: 1 }} />
              Update
            </Fab>
          </Grid>
        </Grid>
        <Snackbar
          open={sbState.open}
          onClick={() => setSbState({ ...sbState, open: false })}
          onClose={() => setSbState({ ...sbState, open: false })}
          TransitionComponent={sbState.Transition}
          message={sbState.message}
          key={sbState.Transition.name}
          autoHideDuration={6000}
          anchorOrigin={{ vertical: 'top', horizontal: "center" }}
        >
          <Alert severity={sbState.severity}>
            {sbState.message}
          </Alert>
        </Snackbar>
      </div>
    </ >
  );
}

export default App;
