import { ThemeProvider } from '@emotion/react';
import { FileUpload, Navigation } from '@mui/icons-material';
import { Alert, AlertColor, AppBar, Fab, Grid, Grow, IconButton, Slide, Snackbar, Toolbar, Typography, createTheme } from '@mui/material';
import { TransitionProps } from '@mui/material/transitions';
import React, { useState } from 'react';
import { getOptionDefinition, getStatus, setEffect } from './api/ApiManager';
import AddCustomEffectDialog from './components/AddCustomEffect.dialog';
import { getCustomSliderForm } from './components/CustomSliderForm';
import { getMultiselectForm } from './components/MultiSelectForm';
import { getSingleSelectForm } from './components/SingleSelectForm';
import { getTimerForm } from './components/TimerForm';
import { IStatus, TimerDataComponent } from './domainData/DomainData';

const App: React.FC = () => {
  const [effectOptionDefinition, setEffectOptionDefinition] = useState<any>()
  const [mainFormData, setMainFormData] = useState<any>({})
  const [addCustomEffectDialogOpen, setAddCustomEffectDialogOpen] = React.useState<boolean>(false)
  const [snackState, setSnackState] = React.useState<{
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


  const handleClickUpdate = async () => {
    try {
      const outData = mainFormData
      // filter out unneeded fields
      Object.keys(outData).forEach((key: any) => {
        if (!effectOptionDefinition.hasOwnProperty(key)) {
          delete outData[key]
        }
      })
      for (const key of Object.keys(effectOptionDefinition)) {
        if (!outData.hasOwnProperty(key)) {
          setSnackState({ ...snackState, open: true, message: `Effect options for ${mainFormData.effect} is missing the field ${key}`, severity: "error" })
          return
        }
      }
      await setEffect(mainFormData);
    } catch (error: any) {
      setSnackState({ ...snackState, open: true, message: error.message, severity: "error" })
    }
  }

  const handleSliderChange = (event: Event, newValue: number | number[], fieldName: string) => {
    setMainFormData({ ...mainFormData, [fieldName]: newValue as number });
  };

  const handleSingleSelectClick = (fieldName: string, chipName: string) => {
    setMainFormData({ ...mainFormData, [fieldName]: chipName })
  }

  const handleMultiSelectChange = (fieldName: string, chipName: string): void => {
    const currentList: string[] = mainFormData[fieldName] || []
    if (currentList.includes(chipName)) {
      if (currentList.length === 1) {
        setSnackState({ ...snackState, open: true, message: "At least 1 effect must be set!", severity: "warning" })
        return
      }
      currentList.splice(currentList.indexOf(chipName), 1) // remove element from selection array
    }
    else {
      currentList.push(chipName)
    }

    setMainFormData({ ...mainFormData, [fieldName]: currentList })
  }

  const handleClickIncreaseSlider = (fieldName: string) => {
    let newVal = mainFormData[fieldName] + 10
    if (newVal > effectOptionDefinition[fieldName].dataComponent.upper_bound) {
      newVal = effectOptionDefinition[fieldName].dataComponent.upper_bound
    }
    setMainFormData({ ...mainFormData, [fieldName]: newVal })
  }
  const handleClickDecreaseSlider = (fieldName: string) => {
    let newVal = mainFormData[fieldName] - 10
    if (newVal < effectOptionDefinition[fieldName].dataComponent.lower_bound) {
      newVal = effectOptionDefinition[fieldName].dataComponent.lower_bound
    }
    setMainFormData({ ...mainFormData, [fieldName]: newVal })
  }

  const handleUploadFileClick = () => setAddCustomEffectDialogOpen(true)


  React.useEffect(() => {
    const fn = async () => {
      try {
        const res: IStatus = await getStatus()
        setMainFormData(res)
      } catch (error) {
        setSnackState({ ...snackState, open: true, message: String(error), severity: "error" })
      }
    }
    fn()
  }, [])

  React.useEffect(() => {
    const fn = async () => {
      try {
        if (mainFormData.effect != undefined) {
          const res = await getOptionDefinition(mainFormData.effect)
          setEffectOptionDefinition(res)
        }
      } catch (error) {
        setSnackState({ ...snackState, open: true, message: String(error), severity: "error" })
      }
    }
    fn()
  }, [mainFormData.effect])

  const theme = createTheme({
    typography: {
      allVariants: {
        fontFamily: "monospace"
      }
    },
  });


  return (
    <ThemeProvider theme={theme}>
      <div className='main'>
        <AppBar position='static' color="primary" sx={{ borderRadius: "12px", marginBottom: "12px", marginTop: "12px", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)" }}>
          <Toolbar>
            <Typography variant="h5" sx={{ flexGrow: 2 }}>
              pyLEDControl
            </Typography>
            <IconButton
              size="large"
              edge="end"
              onClick={handleUploadFileClick}
            >
              <FileUpload sx={{ mr: 1 }} style={{ color: "#fff" }} />
              <Typography variant="button" sx={{ flexGrow: 2 }} color="white">Upload</Typography>
            </IconButton>
          </Toolbar>
        </AppBar>
        <Grid container direction="row" justifyContent="center" alignItems="stretch" columns={{ xs: 1, sm: 2, md: 2 }} spacing={{ xs: 2, md: 2 }}>
          {effectOptionDefinition ?
            Object.keys(effectOptionDefinition).map((key) => {
              const field = effectOptionDefinition[key]
              const type = field["dataComponent"]["type"]
              switch (type) {
                case "IntervalDataComponent":
                  return makeTransition(key, getCustomSliderForm(key, field.dataComponent.display_name, handleClickDecreaseSlider, mainFormData[key] as number, handleSliderChange, handleClickIncreaseSlider))
                case "MultiselectDataComponent":
                  return makeTransition(key, getMultiselectForm(key, field.dataComponent.display_name, field.dataComponent.items, mainFormData[key] || [], handleMultiSelectChange))
                case "SingleselectDataComponent":
                  return makeTransition(key, getSingleSelectForm(key, field.dataComponent.display_name, field.dataComponent.items, mainFormData[key] || 0, handleSingleSelectClick))
                case "TimerDataComponent":
                  return makeTransition(key, getTimerForm(key, field.dataComponent.display_name, {} as any, (newVal) => setMainFormData({ ...mainFormData, [key]: newVal })))
                default: 
                  break
              }
              return <></>
            })
            : undefined
          }
        </Grid>
        <Grid container columns={1} sx={{ position: "sticky", bottom: 15, width: "100%", marginTop: "50px" }} justifyContent="center">
          <Grid item>
            <Fab variant="extended" color="primary" aria-label="add" onClick={handleClickUpdate}>
              <Navigation sx={{ mr: 1 }} />
              Update
            </Fab>
          </Grid>
        </Grid>
        {CustomSnackbar(snackState, setSnackState)}
        <AddCustomEffectDialog
          isOpen={addCustomEffectDialogOpen}
          handleClose={() => setAddCustomEffectDialogOpen(false)} />
      </div>
    </ThemeProvider>
  );
}

const makeTransition = (key: string, component: JSX.Element) => {
  return (
    <Grow in={true} unmountOnExit>
      {component}
    </Grow>
  )
}

export function CustomSnackbar(snackState: {
  open: boolean; Transition: React.ComponentType<
    TransitionProps & {
      children: React.ReactElement<any, any>;
    }
  >; message: string; severity: AlertColor;
}, setSnackState: React.Dispatch<React.SetStateAction<{
  open: boolean; Transition: React.ComponentType<
    TransitionProps & {
      children: React.ReactElement<any, any>;
    }
  >; message: string; severity: AlertColor;
}>>) {
  return <Snackbar
    open={snackState.open}
    onClick={() => setSnackState({ ...snackState, open: false })}
    onClose={() => setSnackState({ ...snackState, open: false })}
    TransitionComponent={snackState.Transition}
    message={snackState.message}
    key={snackState.Transition.name}
    autoHideDuration={6000}
    anchorOrigin={{ vertical: 'top', horizontal: "center" }}
  >
    <Alert severity={snackState.severity}>
      {snackState.message}
    </Alert>
  </Snackbar>;
}

export default App;
