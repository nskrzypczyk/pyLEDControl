import { Checklist } from "@mui/icons-material"
import { Grid, Box, Typography, Divider, Chip, TextField } from "@mui/material"
import { useState } from "react";
import { start } from "repl"

export const getTimerForm = (fieldName: string, displayName: string, optionList: string[], selectedElements: string[] | undefined, handleSelectionChange: any) => {
    const weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"];
    const [enabled, setEnabled] = useState(false);
    const [start, setStart] = useState("08:00");
    const [end, setEnd] = useState("00:30");
    const [days, setdays] = useState<string[]>([]);

    const toggleDay = (day: string) => {
        setdays((prev) =>
            prev.includes(day)
                ? prev.filter((d) => d !== day)
                : [...prev, day]
        );
    };

    return (
        <Grid key={fieldName} className='panel' item xs={1} justifyContent="center">
            <Box sx={{ borderRadius: "12px", backgroundColor: "white", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)", padding: "10px" }}>
                <Grid container columns={8} direction="row" alignItems="center">
                    <Grid container item xs={1}>
                        <Checklist />
                    </Grid>
                    <Grid item xs="auto">
                        <Typography variant='h6' color="black">
                            {displayName}
                        </Typography>
                    </Grid>
                </Grid>
                <Divider sx={{ mt: 1, mb: 1 }} />
                <Grid container spacing={2}>
                    {/* Zeiten */}
                    <Grid item xs={6}>
                        <TextField
                            label="Ein"
                            type="time"
                            value={start}
                            onChange={(e) => setStart(e.target.value)}
                            fullWidth
                            InputLabelProps={{ shrink: true }}
                        />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField
                            label="Aus"
                            type="time"
                            value={end}
                            onChange={(e) => setEnd(e.target.value)}
                            fullWidth
                            InputLabelProps={{ shrink: true }}
                        />
                    </Grid>

                    {/* Tage */}
                    <Grid item xs={12}>
                        <Typography variant="body2" sx={{ mb: 1 }}>
                            Tage
                        </Typography>
                        <Grid container spacing={1}>
                            {weekdays.map((day) => (
                                <Grid item key={day}>
                                    <Chip
                                        label={day}
                                        clickable
                                        color={
                                            days.includes(day) ? "primary" : "default"
                                        }
                                        onClick={() => toggleDay(day)}
                                    />
                                </Grid>
                            ))}
                        </Grid>
                    </Grid>

                    {/* Vorschau */}
                    <Grid item xs={12}>
                        <Typography variant="body2">
                            Aktiv zwischen {start} – {end}
                        </Typography>
                    </Grid>
                </Grid>
            </Box>
        </Grid>
    )
}