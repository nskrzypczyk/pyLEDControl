import { Circle, Close, Save } from "@mui/icons-material";
import { Alert, AlertColor, AppBar, Box, Button, Chip, Dialog, DialogContent, DialogContentText, DialogTitle, Grid, IconButton, List, ListItem, ListItemIcon, Skeleton, Slide, Tab, Tabs, TextField, Toolbar, Typography } from "@mui/material";
import React, { ChangeEvent, SyntheticEvent, useEffect, useRef, useState } from "react";
import { CustomSnackbar } from "../App";
import { TransitionProps } from "@mui/material/transitions";
import { addEffect, addEffectWithURL, deleteEffect, getUploadedEffects } from "../api/ApiManager";

export interface PropsAddCustomEffectDialog {
    handleClose: () => void;
    handleFileName: (file: File) => void;
    isOpen: boolean;
}

function TabPanel(props: Readonly<{
    children?: React.ReactNode;
    index: number;
    value: number;
}>) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`full-width-tabpanel-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ p: 3 }}>
                    <Typography>{children}</Typography>
                </Box>
            )}
        </div>
    );
}

const AddCustomEffectDialog: React.FC<PropsAddCustomEffectDialog> = (props: Readonly<PropsAddCustomEffectDialog>) => {
    // States
    const [tabValue, setTabValue] = useState<number>(0)
    const [selectedFile, setSelectedFile] = useState<File>()
    const [availableEffects, setAvailableEffects] = useState<string[]>([])
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
    })
    // --------------------------------------------------------------------------------
    // Refs
    const fileInputRef: any = useRef()
    const tfEffectNameRef: any = useRef()
    const tfURLRef: any = useRef()


    // --------------------------------------------------------------------------------
    // Effects
    const refreshAvailableEffects = async () => {
        try {
            setAvailableEffects(await getUploadedEffects())
        } catch (error) {
            setSnackState({ ...snackState, open: true, message: String(error), severity: "error" })
        }
    }
    useEffect(() => {
        if (tabValue === 2) { // If delete tab selected
            refreshAvailableEffects()
        }
    }, [tabValue])


    // --------------------------------------------------------------------------------
    // Handles
    const handleTabChange = (event: SyntheticEvent, idx: number) => setTabValue(idx)
    const handleSelectFileClick = () => (fileInputRef as any).current.click()
    const handleFileInput = (e: ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files) {
            return
        }
        props.handleFileName(e.target.files[0])
        setSelectedFile(e.target.files[0])
    }

    const getEffectName = () => tfEffectNameRef.current.value;
    const getEffectURL = () => tfURLRef.current.value;
    const handleSave = () => {
        const fn = async () => {
            let res;
            try {
                if (tabValue === 0) { // if uploaded 
                    res = await addEffect(selectedFile!, getEffectName())
                }
                else if (tabValue === 1) { // if URL
                    res = await addEffectWithURL(getEffectURL(), getEffectName())
                }
                setSnackState({ ...snackState, open: true, message: String(res), severity: "success" })
            }
            catch (error) {
                setSnackState({ ...snackState, open: true, message: String(error), severity: "error" })
            }
        }
        fn()
    }

    const handleDelete = (effectName: string) => {
        const fn = async () => {
            try {
                const res = await deleteEffect(effectName)
                setSnackState({ ...snackState, open: true, message: String(res), severity: "success" })
            } catch (error) {
                setSnackState({ ...snackState, open: true, message: String(error), severity: "error" })
            }
            await refreshAvailableEffects()
        }
        fn()
    }


    // --------------------------------------------------------------------------------
    // Elements

    return (
        <Dialog
            fullScreen
            id="mainDL_addCustomEffectDialog"
            open={props.isOpen}
            onClose={props.handleClose}
        >
            <AppBar position='static' color="primary" sx={{ marginBottom: "12px", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)" }}>
                <Toolbar>
                    <IconButton
                        edge="start"
                        color="inherit"
                        onClick={props.handleClose}
                        aria-label="close"
                    >
                        <Close />
                    </IconButton>
                    <DialogTitle sx={{ ml: 1, flex: 1 }}>Add custom effect</DialogTitle>
                    {tabValue !== 2 ? <IconButton size="large" edge="end" color="inherit" onClick={handleSave}>
                        <Save sx={{ mr: 1 }} />
                        <Typography>Save</Typography>
                    </IconButton> : null}
                </Toolbar>
            </AppBar>
            <DialogContent>
                <DialogContentText>
                    This dialog can be used to upload or delete a custom effect which is based on a provided
                    <List>
                        {["png file", "jpeg file", "gif file", "a URL that points to one of those file types"].map(e => (
                            <ListItem key={e}>
                                <ListItemIcon>
                                    <Circle sx={{ scale: '0.6' }} />
                                </ListItemIcon>
                                {e}
                            </ListItem>
                        ))}
                    </List>
                </DialogContentText>
                <Tabs
                    value={tabValue}
                    orientation="horizontal"
                    onChange={handleTabChange}
                >
                    <Tab label="Upload File" />
                    <Tab label="Provide Media URL" />
                    <Tab label="Delete Effect" />
                </Tabs>
                <TabPanel value={tabValue} index={1}>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="nameTF_addCustomEffectDialog"
                        label="Effect name"
                        type="text"
                        fullWidth
                        variant="outlined"
                        inputRef={tfEffectNameRef}
                    />
                    <TextField
                        margin="dense"
                        id="urlTF_addCustomEffectDialog"
                        label="Media URL"
                        type="url"
                        fullWidth
                        variant="outlined"
                        inputRef={tfURLRef}
                    />
                </TabPanel>
                <TabPanel value={tabValue} index={0}>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="nameTF_addCustomEffectDialog"
                        label="Effect name"
                        type="text"
                        fullWidth
                        variant="outlined"
                        inputRef={tfEffectNameRef}
                        sx={{mb:1.5}}
                    />
                    <Grid container spacing={selectedFile ? 1 : 0}>
                        <Grid item xs={selectedFile ? 3 : 12}>
                            <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                                <input type="file" accept=".png, .gif, .jpeg, .jpg" ref={fileInputRef} style={{ display: "none" }} onChange={handleFileInput as any} />
                                <Button onClick={handleSelectFileClick} sx={{ flex: "1", width: "100%", minHeight: "100%" }} variant="outlined">
                                    Select file
                                </Button>
                            </div>

                        </Grid>
                        <Grid item xs={9}>
                            {selectedFile
                                ?
                                <Alert variant="outlined">
                                    Selected file: {selectedFile.name}
                                </Alert>
                                : null}
                        </Grid>
                    </Grid>
                </TabPanel>
                <TabPanel value={tabValue} index={2}>
                    <Typography mb={1.5}>You can use this tab to delete an existing uploaded effect</Typography>
                    {
                        availableEffects.length === 0
                            ?
                            <Box sx={{ width: "50%" }}>
                                <Skeleton animation="wave" />
                                <Skeleton animation="wave" />
                                <Skeleton animation="wave" />
                            </Box>
                            :
                            <Grid container item spacing={1}>
                                {
                                    availableEffects.map(
                                        (e) => (
                                            <Grid key={e + "_uploaded_effect_grid_"} item>
                                                <Chip
                                                    sx={{ fontSize: "15pt", height: "30pt" }}
                                                    key={e + "_uploaded_effect_chip_"}
                                                    variant="outlined" label={e}
                                                    onDelete={() => handleDelete(e)}
                                                />
                                            </Grid>
                                        )
                                    )
                                }
                            </Grid>
                    }
                </TabPanel>
                {CustomSnackbar(snackState, setSnackState)}
            </DialogContent>
        </Dialog>
    )
}

export default AddCustomEffectDialog