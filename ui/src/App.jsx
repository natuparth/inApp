import { Route, BrowserRouter, Routes } from 'react-router-dom';
import Login from './components/Login';
import Home from './components/Home';

export default function App() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', width: '100vw', flexDirection: 'column'}}>
      <BrowserRouter>
      <Routes>
      <Route exact path="/" element={<Login/>} />
      <Route exact path="/login" element={<Login/>} />
      <Route exact path="/home" element={<Home/>} />
      </Routes>
    </BrowserRouter>
    </div>
  );
}

