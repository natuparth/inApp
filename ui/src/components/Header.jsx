import { Box, Typography } from '@mui/material';

const Header = () => (
  <Box
    sx={{
      backgroundColor: '#000',
      color: '#fff',
      padding: '2rem',
      textAlign: 'center',
    }}
  >
    <Typography variant="h2" fontWeight="bold">
      IMDB
    </Typography>
  </Box>
);

export default Header;