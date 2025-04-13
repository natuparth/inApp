import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  TextField,
  MenuItem,
  Card,
  CardMedia,
  CardContent,
  Typography,
  Select,
  InputLabel,
  FormControl,
  Button,
} from '@mui/material';

import { useNavigate } from 'react-router-dom';
import SearchOffIcon from '@mui/icons-material/SearchOff';

import axios from 'axios';

const genres = ['Documentary', 'Short', 'Romance'];
const types = ['short', 'movie',];
const years = Array.from({ length: 175 }, (_, i) => `${1850 + i}`);

const dummyResults = [

];

const MovieSearch = () => {
  const [search, setSearch] = useState('');
  const [year, setYear] = useState('');
  const [genre, setGenre] = useState('');
  const [type, setType] = useState('');
  const [results, setResults] = useState(dummyResults); // Replace this later with API results
  const navigate = useNavigate();

  useEffect(() => {
    //writing code for initial loading of data
    axios.get('http://localhost:8000/search_movie').then((response) => {
        console.log(response)
        setResults( response.data );
    }).catch((response) => {
        if(response.status === 404 ){
          setResults([]);
        }
      })
  }, [])
  const handleSearch = () => {
    // TODO: Add real API call here
    axios.get('http://localhost:8000/search_movie', { params: { 
        title: search,
        year,
        genre,
        type
    }}).then((response) => {
        setResults( response.data );
    }).catch((response) => {
        if(response.status === 404 ){
          setResults([]);
        } else if( response.status === 401){
           navigate('/login');
        }
      })
  };

  return (
    <Box p={3}>
      <Box display="flex" flexWrap="wrap" justifyContent={"center"} gap={2} mb={3}>
        <TextField
          label="Search"
          variant="outlined"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        //  onBlur={(e) => setSearch(e.target.value)}
        />
        <FormControl variant="outlined" sx={{ minWidth: 120 }}>
          <InputLabel>Year</InputLabel>
          <Select value={year} onChange={(e) => setYear(e.target.value)} label="Year">
            <MenuItem value="">
              <em>Any</em>
            </MenuItem>
            {years.map((y) => (
              <MenuItem key={y} value={y}>
                {y}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl variant="outlined" sx={{ minWidth: 140 }}>
          <InputLabel>Genre</InputLabel>
          <Select value={genre} onChange={(e) => setGenre(e.target.value)} label="Genre">
            <MenuItem value="">
              <em>Any</em>
            </MenuItem>
            {genres.map((g) => (
              <MenuItem key={g} value={g}>
                {g}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl variant="outlined" sx={{ minWidth: 160 }}>
          <InputLabel>Type</InputLabel>
          <Select value={type} onChange={(e) => setType(e.target.value)} label="Type">
            <MenuItem value="">
              <em>Any</em>
            </MenuItem>
            {types.map((t) => (
              <MenuItem key={t} value={t}>
                {t}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button variant="contained" onClick={handleSearch}>
          Search
        </Button>
      </Box>
      {results.length > 0 ? (
      <Grid container spacing={3} justifyContent={"space-evenly"}>
        {results.map((movie) => (
          <Grid item key={movie.id} xs={12} sm={6} md={4} lg={3}>
            <Card>
              <CardContent>
                <Typography variant="h6">{movie.title}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {movie.year_of_release} | {movie.genre} | {movie.type}
                </Typography>
                <Typography variant="body2" mt={1}>
                  {movie.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid> ): (<Box
          mt={6}
          textAlign="center"
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
        >
          <SearchOffIcon sx={{ fontSize: 64, color: 'gray' }} />
          <Typography variant="h6" color="text.secondary">
            No records found
          </Typography>
        </Box>) }
    </Box>
  );
};

export default MovieSearch;
