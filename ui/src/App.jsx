import { Route, BrowserRouter, Routes } from 'react-router-dom';
import Login from './components/Login';
import MovieSearch from './components/Movies';


export default function App() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', width: '100vw'}}>
    <BrowserRouter>
      <Routes>
      <Route exact path="/" element={<Login/>} />
      <Route exact path="/movies" element={<MovieSearch/>} />
      </Routes>
    </BrowserRouter>
    </div>
  );
}

