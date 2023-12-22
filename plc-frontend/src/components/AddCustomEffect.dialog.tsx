import { Circle, Close, Save } from "@mui/icons-material";
import { AppBar, Dialog, DialogContent, DialogContentText, DialogTitle, IconButton, List, ListItem, ListItemIcon, Tab, Tabs, TextField, Toolbar, Typography, Box, Button } from "@mui/material";
import React, { SyntheticEvent, useState } from "react";

export interface PropsAddCustomEffectDialog {
    handleClose: () => void;
    isOpen: boolean;
    onSave: () => void;
}

function TabPanel(props: {
    children?: React.ReactNode;
    index:number;
    value: number;
}) {
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

const AddCustomEffectDialog: React.FC<PropsAddCustomEffectDialog> = (props: PropsAddCustomEffectDialog) => {
    const [tabValue, setTabValue] = useState<number>(0)
    const handleTabChange = (event: SyntheticEvent, idx: number) => setTabValue(idx);
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
                    <IconButton size="large" edge="end" color="inherit" onClick={props.handleClose}>
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
                    <Tab label="Provide URL" />
                    <Tab label="Upload file" />
                </Tabs>
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
                    <TextField
                        margin="dense"
                        id="urlTF_addCustomEffectDialog"
                        label="Media URL"
                        type="url"
                        fullWidth
                        variant="outlined"
                    />
                </TabPanel>
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
                    <Button sx={{width:"100%"}} variant="outlined">Select file</Button>
                </TabPanel>

            </DialogContent>
        </Dialog>
    )
}
export default AddCustomEffectDialog