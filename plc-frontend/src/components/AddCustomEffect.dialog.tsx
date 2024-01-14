import { Circle, Close, Save } from "@mui/icons-material";
import { Alert, AppBar, Box, Button, Dialog, DialogContent, DialogContentText, DialogTitle, Grid, IconButton, List, ListItem, ListItemIcon, Tab, Tabs, TextField, Toolbar, Typography } from "@mui/material";
import React, { ChangeEvent, SyntheticEvent, useRef, useState } from "react";

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
    const [tabValue, setTabValue] = useState<number>(0)
    const [selectedFile, setSelectedFile] = useState<File>()
    const handleTabChange = (event: SyntheticEvent, idx: number) => setTabValue(idx)
    const handleSelectFileClick = () => (ref as any).current.click()
    const handleFileInput = (e: ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files) {
            return
        }
        props.handleFileName(e.target.files[0])
        setSelectedFile(e.target.files[0])
    }

    const handleSave = () =>{
        // FIXME: Implement
    }
    
    const handleDelete = () => {
        // FIXME: Implement
    }

    const ref = useRef()
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
                    <IconButton size="large" edge="end" color="inherit" onClick={handleSave}>
                        <Save sx={{ mr: 1 }} />
                        <Typography>Save</Typography>
                    </IconButton>
                </Toolbar>
            </AppBar>
            <DialogContent>
                <DialogContentText>
                    This dialog can be used to upload a custom effect which is based on a provided
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
                    <Tab label="Upload file" />
                    <Tab label="Provide URL" />
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
                    />
                    <TextField
                        margin="dense"
                        id="urlTF_addCustomEffectDialog"
                        label="Media URL"
                        type="url"
                        fullWidth
                        variant="outlined"
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
                    />
                    <Grid container spacing={selectedFile ? 1 : 0}>
                        <Grid item xs={selectedFile ? 3 : 12}>
                            <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                                <input type="file" accept=".png, .gif, .jpeg, .jpg" ref={ref as any} style={{ display: "none" }} onChange={handleFileInput as any} />
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

            </DialogContent>
        </Dialog>
    )
}

export default AddCustomEffectDialog