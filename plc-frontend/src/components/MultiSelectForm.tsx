import { Checklist } from "@mui/icons-material"
import { Grid, Box, Typography, Divider, Chip } from "@mui/material"

export const getMultiselectForm = (fieldName: string, displayName: string, optionList: string[], selectedElements: string[] | undefined, handleSelectionChange: any) => {
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