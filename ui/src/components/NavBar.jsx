import { Box, Button } from '@mui/material';


const Navbar = ({ setTab, tab }) => {
 

  const isActive = (path, label) => label.toLowerCase() === path

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        gap: 2,
        mt: 2,
      }}
    >
      {['Movies', 'Actors'].map((label) => {
        const path = tab;
        return (
          <Button
            key={label}
            variant={isActive(path, label) ? 'contained' : 'outlined'}
            onClick={() => setTab( label.toLowerCase())}
            sx={{
              borderRadius: '999px',
              px: 4,
              textTransform: 'none',
            }}
          >
            {label}
          </Button>
        );
      })}
    </Box>
  );
};

export default Navbar;
