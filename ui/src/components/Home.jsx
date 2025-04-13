import { useEffect, useState } from 'react';
import MovieSearch from './Movies';
import ActorSearch from './ActorSearch';
import Header from './Header';
import Navbar from './NavBar';

export default function Home() {
const [ tab, setTab ] = useState( 'movies' );
  return (
    <div style={{ display: 'flex', justifyContent: 'center', width: '100vw', flexDirection: 'column'}}>
    
      <Header/>
      <Navbar setTab={setTab} tab={tab}/>


        { tab === 'movies' && <MovieSearch/> }
        { tab === 'actors' && <ActorSearch/> }
    
    
    </div>
  );
}