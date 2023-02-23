import React from 'react'
import questionmark from '../img/questionmark.png'
import './Home.css'
import '../App.css'
import { Link } from 'react-router-dom';

const Home = () => {
      return (
      <div className="Landing_pg">
        <div className='Heroimage'></div>
        <div className='Header'> Selamat</div>
        <div className='Header2'> Datang </div>
        <div className='subtitle-text'> 
          <span> Silakan pilih metode </span>
          <span className='purple-text'> liveness detection </span>
          <span> yang diinginkan:</span> 
        </div>
        <div className='button_primary'>
          <Link to='/aktif'>
          <button className='btn'>Aktif</button>
          </Link>
          </div>
          <div className='button_primary'>
          <Link to='/pasif'>
          <button className='btn'>Pasif</button>
          </Link>
        </div>
        <div className='text'> 
          <img src={questionmark} alt=" " className='img_question'/>
          <span className='text'>butuh bantuan</span> 
        </div>
      </div>
      );
}

export default Home;