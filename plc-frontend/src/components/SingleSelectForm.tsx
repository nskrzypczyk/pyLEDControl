import { Check } from "@mui/icons-material";
import { Grid, Box, Typography, Divider, Chip } from "@mui/material";

export const getSingleSelectForm = (fieldName: string, displayName: string, optionList: string[], selectedElement: string | undefined, handleChipChange: (fieldName: string, chipName: string) => void) => {
  return <Grid key={fieldName} className='panel' item xs={1} justifyContent="center">
    <Box sx={{ borderRadius: "12px", backgroundColor: "white", boxShadow: "0px 0px 12px rgba(0, 0, 0, 0.6)", padding: "10px" }}>
      <Grid container columns={8} direction="row" alignItems="center">
        <Grid container item xs={1}>
          <Check />
        </Grid>
        <Grid item xs="auto">
          <Typography variant='h6' color="black">
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
