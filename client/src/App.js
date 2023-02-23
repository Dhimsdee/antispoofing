import React from 'react'
//import { BrowserRouter as Router} from "react-router-dom";
import Navbar from './Components/Navbar.jsx'
import Home from './Components/Home.jsx'
import Pasif from './Components/Pasif.jsx'
import Aktif from './Components/Aktif.jsx'
import { Routes, Route } from 'react-router-dom'

const App = () => {
    return (
    <div>
    <Navbar />
    <Routes>
    <Route path='/' element={<Home/>} />
    <Route path='/aktif' element={<Aktif/>} />
    <Route path='/pasif' element={<Pasif/>} />
    </Routes>
    </div>
    );
}

export default App;