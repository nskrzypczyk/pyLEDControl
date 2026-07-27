import { Checklist } from "@mui/icons-material";
import { Box, Chip, Divider, FormControlLabel, Grid, Switch, TextField, Typography } from "@mui/material";
import { TimerDataComponent } from "../domainData/DomainData";

export const getTimerForm = (
    fieldName: string,
    displayName: string,
    value: TimerDataComponent,
    setValue: (value: TimerDataComponent) => void,
) => {
    const weekdays = {
        "Mo": 0,
        "Tu": 1,
        "We": 2,
        "Th": 3,
        "Fr": 4,
        "Sa": 5,
        "Su": 6
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
                    <Grid item sx={{ ml: "auto" }}>
                        <FormControlLabel control={<Switch checked={value.enabled} onChange={(e) => setValue({ ...value, enabled: e.target.checked })} />}
                            label="Enabled"
                        />
                    </Grid>
                </Grid>
                <Divider sx={{ mt: 1, mb: 1 }} />
                <Grid container columns={24} spacing={2} alignItems={"center"}>
                    {/* Zeiten */}
                    <Grid item xs={10}>
                        <TextField
                            label="On"
                            type="time"
                            value={secondsToHHMM(value.start)}
                            onChange={(e) => setValue({ ...value, start: hhmmToSeconds(e.target.value) })}
                            fullWidth
                            InputLabelProps={{ shrink: true }}
                        />
                    </Grid>
                    <Grid item xs={10}>
                        <TextField
                            label="Off"
                            type="time"
                            value={secondsToHHMM(value.end)}
                            onChange={(e) => setValue({ ...value, end: hhmmToSeconds(e.target.value) })}
                            fullWidth
                            InputLabelProps={{ shrink: true }}
                        />
                    </Grid>

                    {/* Tage */}
                    <Grid item xs={12}>
                        <Typography variant="body2" sx={{ mb: 1 }}>
                            Days
                        </Typography>
                        <Grid container spacing={1}>
                            {Object.entries(weekdays).map(([day, dayNo]) => (
                                <Grid item key={dayNo}>
                                    <Chip
                                        label={day}
                                        clickable
                                        color={
                                            value.days.includes(dayNo) ? "primary" : "default"
                                        }
                                        onClick={handleDayChange(dayNo)}
                                    />
                                </Grid>
                            ))}
                        </Grid>
                    </Grid>

                </Grid>
            </Box>
        </Grid>
    )

    function handleDayChange(day: number): import("react").MouseEventHandler<HTMLDivElement> | undefined {
        return () => setValue({
            ...value,
            days: value.days.includes(day)
                ? value.days.filter((d) => d !== day)
                : [...value.days, day],
        });
    }

    function secondsToHHMM(seconds: number): string {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);

        return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
    }

    function hhmmToSeconds(hhmm: string): number {
        const [hours, minutes] = hhmm.split(':').map(Number);
        return hours * 3600 + minutes * 60;
    }
}