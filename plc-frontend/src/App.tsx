import { AddCircle, Check, Checklist, CompareArrows, FileUpload, Navigation, RemoveCircle } from '@mui/icons-material';
import { Alert, AlertColor, AppBar, Box, Button, Chip, Divider, Fab, Grid, Grow, IconButton, Slide, Slider, Snackbar, Stack, Toolbar, Typography, createTheme } from '@mui/material';
import { TransitionProps } from '@mui/material/transitions';
import React, { useState } from 'react';
import './App.css';
import { getOptionDefinition, getStatus, setEffect } from './api/ApiManager';
import AddCustomEffectDialog from './components/AddCustomEffect.dialog';
import { IStatus } from './domainData/DomainData';
import { ThemeProvider } from '@emotion/react';
import { dark } from '@mui/material/styles/createPalette';

const App: React.FC = () => {
  const [effectOptionDefinition, setEffectOptionDefinition] = useState<any>();
  const [formData, setFormData] = useState<any>({});
  const [addCustomEffectDialogOpen, setAddCustomEffectDialogOpen] = React.useState<boolean>(false);
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
      const outData = formData
      // filter out unneeded fields
      Object.keys(outData).forEach((key: any) => {
        if (!effectOptionDefinition.hasOwnProperty(key)) {
          delete outData[key]
        }
      })
      for (const key of Object.keys(effectOptionDefinition)) {
        if (!outData.hasOwnProperty(key)) {
          setSnackState({ ...snackState, open: true, message: `Effect options for ${formData.effect} is missing the field ${key}`, severity: "error" })
          return
        }
      }
      await setEffect(formData);
    } catch (error: any) {
      setSnackState({ ...snackState, open: true, message: error.message, severity: "error" })
    }
  }

  const handleSliderChange = (event: Event, newValue: number | number[], fieldName: string) => {
    setFormData({ ...formData, [fieldName]: newValue as number });
  };

  const handleSingleSelectClick = (fieldName: string, chipName: string) => {
    setFormData({ ...formData, [fieldName]: chipName })
  }

  const handleMultiSelectChange = (fieldName: string, chipName: string): void => {
    const currentList: string[] = formData[fieldName] || []
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

    setFormData({ ...formData, [fieldName]: currentList })
  }

  const handleClickIncreaseSlider = (fieldName: string) => {
    let newVal = formData[fieldName] + 10
    if (newVal > effectOptionDefinition[fieldName].constraint.upper_bound) {
      newVal = effectOptionDefinition[fieldName].constraint.upper_bound
    }
    setFormData({ ...formData, [fieldName]: newVal })
  }
  const handleClickDecreaseSlider = (fieldName: string) => {
    let newVal = formData[fieldName] - 10
    if (newVal < effectOptionDefinition[fieldName].constraint.lower_bound) {
      newVal = effectOptionDefinition[fieldName].constraint.lower_bound
    }
    setFormData({ ...formData, [fieldName]: newVal })
  }

  const handleUploadFileClick = () => setAddCustomEffectDialogOpen(true)

  const handleUploadDialogOnSave = () => undefined;

  React.useEffect(() => {
    const fn = async () => {
      try {
        const res: IStatus = await getStatus()
        setFormData(res)
      } catch (error) {
        setSnackState({ ...snackState, open: true, message: String(error), severity: "error" })
      }
    }
    fn()
  }, [])

  React.useEffect(() => {
    const fn = async () => {
      try {
        if (formData.effect != undefined) {
          const res = await getOptionDefinition(formData.effect)
          setEffectOptionDefinition(res)
        }
      } catch (error) {
        setSnackState({ ...snackState, open: true, message: String(error), severity: "error" })
      }
    }
    fn()
  }, [formData.effect])

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
            <Typography variant="h4" sx={{ flexGrow: 2 }}>
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
              const type = field["constraint"]["type"]
              switch (type) {
                case "IntervalConstraint":
                  return makeTransition(key, getCustomSliderForm(key, field.constraint.display_name, handleClickDecreaseSlider, formData[key] as number, handleSliderChange, handleClickIncreaseSlider))
                case "MultiselectConstraint":
                  return makeTransition(key, getMultiselectForm(key, field.constraint.display_name, field.constraint.items, formData[key] || [], handleMultiSelectChange))
                case "SingleselectConstraint":
                  return makeTransition(key, getSingleSelectForm(key, field.constraint.display_name, field.constraint.items, formData[key] || 0, handleSingleSelectClick))
                default:
                  break
              }
              return <></>
            })
            : undefined
          }
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
        </Snackbar>
        <AddCustomEffectDialog
          isOpen={addCustomEffectDialogOpen}
          handleClose={() => setAddCustomEffectDialogOpen(false)}
          onSave={handleUploadDialogOnSave} />
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

const getMultiselectForm = (fieldName: string, displayName: string, optionList: string[], selectedElements: string[] | undefined, handleSelectionChange: any) => {
  return (
    <Grid key={fieldName} className='panel' item xs={1} justifyContent="center">
      <Box sx={{ borderRadius: "12px", backgroundColor: "white", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)", padding: "10px" }}>
        <Grid container columns={8} direction="row" alignItems="center">
          <Grid container item xs={1}>
            <Checklist />
          </Grid>
          <Grid item xs="auto">
            <Typography variant='h5' color="black">
              {displayName}
            </Typography>
          </Grid>
        </Grid>
        <Divider sx={{ mt: 1.5, mb: 1.5 }} />
        <Grid container item spacing={1}>
          {optionList.map((e) => (
            <Grid key={e + "_grid_" + fieldName} item>
              <Chip
                key={e + "_chip_" + fieldName}
                variant={selectedElements?.includes(e) ? "filled" : "outlined"} label={e}
                onClick={() => handleSelectionChange(fieldName, e)}
                color={selectedElements?.includes(e) ? "primary" : undefined} />
            </Grid>
          ))}
        </Grid>
      </Box>
    </Grid>
  )
}

const getSingleSelectForm = (fieldName: string, displayName: string, optionList: string[], selectedElement: string | undefined, handleChipChange: (fieldName: string, chipName: string) => void) => {
  return <Grid key={fieldName} className='panel' item xs={1} justifyContent="center">
    <Box sx={{ borderRadius: "12px", backgroundColor: "white", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)", padding: "10px" }}>
      <Grid container columns={8} direction="row" alignItems="center">
        <Grid container item xs={1}>
          <Check />
        </Grid>
        <Grid item xs="auto">
          <Typography variant='h5' color="black">
            {displayName}
          </Typography>
        </Grid>
      </Grid>
      <Divider sx={{ mt: 1.5, mb: 1.5 }} />
      <Grid container item spacing={1}>
        {optionList.map((e) => (
          <Grid key={e + "_grid"} item>
            <Chip
              key={e + "_chip"}
              variant={selectedElement === e ? "filled" : "outlined"} label={e} onClick={() => handleChipChange(fieldName, e)}
              color={selectedElement === e ? "primary" : undefined} />
          </Grid>
        ))}
      </Grid>
    </Box>
  </Grid>;
}

const getCustomSliderForm = (fieldName: string, displayName: string, decreaseFunc: (fieldName: string) => void, value: number, handleSliderChange: (event: Event, newValue: number | number[], fieldName: string) => void, increaseFunc: (fieldName: string) => void) => {
  return <Grid key={fieldName} className='panel' item xs={1}>
    <Box sx={{ borderRadius: "12px", padding: "10px", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)" }}>
      <Grid container columns={3} direction="row" alignItems="center">
        <Grid container item xs={1}>
          <CompareArrows />
        </Grid>
        <Grid item xs="auto">
          <Typography variant='h5' color="black">
            {displayName}
          </Typography>
        </Grid>
      </Grid>
      <Divider sx={{ mt: 1.5, mb: 1.5 }} />
      <Stack spacing={1} direction="row" sx={{ mb: 1 }} alignItems="center">
        <Button onClick={() => decreaseFunc(fieldName)}>
          <RemoveCircle />
        </Button>
        <Slider aria-label="Volume" value={value} onChange={(event, value) => handleSliderChange(event, value, fieldName)} />
        <Button onClick={() => increaseFunc(fieldName)}>
          <AddCircle />
        </Button>
      </Stack>
      <Stack direction={'row'} spacing={1} alignItems="center" justifyContent={'center'}>
        <Typography variant="h6" color="black">
          {value} %
        </Typography>
      </Stack>
    </Box>
  </Grid>;
}

export default App;
