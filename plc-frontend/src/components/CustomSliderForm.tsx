import { CompareArrows, RemoveCircle, AddCircle } from "@mui/icons-material";
import { Grid, Box, Typography, Divider, Stack, Button, Slider } from "@mui/material";

export const getCustomSliderForm = (fieldName: string, displayName: string, decreaseFunc: (fieldName: string) => void, value: number, handleSliderChange: (event: Event, newValue: number | number[], fieldName: string) => void, increaseFunc: (fieldName: string) => void) => {
  return <Grid key={fieldName} className='panel' item xs={1}>
    <Box sx={{ borderRadius: "12px", padding: "10px", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)" }}>
      <Grid container columns={3} direction="row" alignItems="center">
        <Grid container item xs={1}>
          <CompareArrows />
        </Grid>
        <Grid item xs="auto">
          <Typography variant='h6' color="black">
            {displayName}
          </Typography>
        </Grid>
      </Grid>
      <Divider sx={{ mt: 1, mb: 1 }} />
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
        <Typography variant="body1" color="black">
          {value} %
        </Typography>
      </Stack>
    </Box>
  </Grid>;
}
