import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  TextField,
  MenuItem,
  Card,
  CardMedia,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  Button,
} from '@mui/material';
import SearchOffIcon from '@mui/icons-material/SearchOff';
import axios from 'axios'
import { useNavigate } from 'react-router-dom';
const professions = ['Actor', 'Director', 'Writer', 'Producer'];


const ActorSearch = () => {
  const [search, setSearch] = useState('');
  const [movieTitle, setMovieTitle] = useState('');
  const [profession, setProfession] = useState('');
  const [results, setResults] = useState([]); // Replace with API results later
  const navigate = useNavigate();

  useEffect(() => {
    //writing code for initial loading of data
    axios.get('http://localhost:8000/search_actors').then((response) => {
        console.log(response)
        setResults( response.data );
    }).catch((response) => {
      if(response.status === 404 ){
        setResults([]);
      } else if( response.status === 401){
         navigate('/login');
      }
    })
  }, [])
  const handleSearch = () => {
    // TODO: Add real API call here
    axios.get('http://localhost:8000/search_actors', { params: { 
        name: search,
        profession,
        movie_title: movieTitle
    }}).then((response) => {
        setResults( response.data );
    }).catch((response) => {
      if(response.status === 404 ){
        setResults([]);
      }
    })
  };

  return (
    <Box p={3}>
      <Box display="flex" flexWrap="wrap" justifyContent={"center"} gap={2} mb={3}>
        <TextField
          label="Search Name"
          variant="outlined"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <TextField
          label="Movie Title"
          variant="outlined"
          value={movieTitle}
          onChange={(e) => setMovieTitle(e.target.value)}
        />
        <FormControl sx={{ minWidth: 160 }}>
          <InputLabel>Profession</InputLabel>
          <Select
            value={profession}
            onChange={(e) => setProfession(e.target.value)}
            label="Profession"
          >
            <MenuItem value="">
              <em>Any</em>
            </MenuItem>
            {professions.map((p) => (
              <MenuItem key={p} value={p}>
                {p}
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
        {results.map((person) => (
          <Grid item key={person.id} xs={12} sm={6} md={4} lg={3}>
            <Card>
              <CardContent>
                <Typography variant="h6">{person.name}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Profession: {person.profession}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Known For: {person.known_for_titles}
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

export default ActorSearch;
