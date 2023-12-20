import { Close, Save } from "@mui/icons-material";
import { AppBar, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, IconButton, TextField, Toolbar, Typography } from "@mui/material"

export interface PropsAddCustomEffectDialog {
    handleClose: () => void;
    isOpen: boolean;
    onSave: () => void;
}

const AddCustomEffectDialog: React.FC<PropsAddCustomEffectDialog> = (props: PropsAddCustomEffectDialog) => {
    return (
        <Dialog
            fullScreen
            id="mainDL_addCustomEffectDialog"
            open={props.isOpen}
            onClose={props.handleClose}
        >
            <AppBar position='static' color="primary" sx={{ borderRadius: "12px", marginBottom: "12px", marginTop: "12px", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)" }}>
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
                    This dialog can be used to upload a custom effect which can be a file or URL leading to a png, jpeg or gif.
                </DialogContentText>
                <TextField
                    autoFocus
                    margin="dense"
                    id="nameTF_addCustomEffectDialog"
                    label="Effect name"
                    type="text"
                    fullWidth
                    variant="standard"
                />
                <TextField
                    margin="dense"
                    id="urlTF_addCustomEffectDialog"
                    label="Media URL"
                    type="url"
                    fullWidth
                    variant="standard"
                />
            </DialogContent>
        </Dialog>
    )
}
export default AddCustomEffectDialog