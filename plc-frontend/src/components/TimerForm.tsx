import { Checklist } from "@mui/icons-material"
import { Grid, Box, Typography, Divider, Chip, TextField } from "@mui/material"
import { useState } from "react";
import { start } from "repl"
import { TimerDataComponent } from "../domainData/DomainData";

export const getTimerForm = (
    fieldName: string,
    value: TimerDataComponent,
    displayName: string,
    setValue: (value: TimerDataComponent) => void,
) => {
    const weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"];

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
                            onChange={(e) => setValue({ ...value, start: e.target.value })}
                            fullWidth
                            InputLabelProps={{ shrink: true }}
                        />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField
                            label="Aus"
                            type="time"
                            value={value.end}
                            onChange={(e) => setValue({ ...value, end: e.target.value })}
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
                                            value.selectedDays.includes(day) ? "primary" : "default"
                                        }
                                        onClick={handleDayChange(day)}
                                    />
                                </Grid>
                            ))}
                        </Grid>
                    </Grid>

                    {/* Vorschau */}
                    <Grid item xs={12}>
                        <Typography variant="body2">
                            Acitve between {value.start} – {value.end}
                        </Typography>
                    </Grid>
                </Grid>
            </Box>
        </Grid>
    )

    function handleDayChange(day: string): import("react").MouseEventHandler<HTMLDivElement> | undefined {
        return () => setValue({
            ...value,
            selectedDays: value.selectedDays.includes(day)
                ? value.selectedDays.filter((d) => d !== day)
                : [...value.selectedDays, day],
        });
    }
}