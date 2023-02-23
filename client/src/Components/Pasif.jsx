// ini dipake buat app.py

import React, { useState } from 'react';

function Pasif() {
  const [label, setLabel] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLivenessDetection = () => {
    setIsLoading(true);
    const data = {
      model_Path: 'livenessnet/LivenessNet.model',
      le_path: 'livenessnet/le.pickle',
      detector_folder: 'livenessnet/face_detector',
      confidence: 0.5,
    };

    fetch('http://localhost:5000/livenessnet', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        setLabel(data.label);
      })
      .catch((error) => console.error(error))
      .finally(() => setIsLoading(false));
  };

  return (
    <div>
      <div className='button_primary'> 
      <button className='btn' onClick={handleLivenessDetection}>
        Detect Liveness
      </button>
      </div>
      {isLoading ? (
        <div className='subtitle-text'>Loading...</div>
      ) : label === 'real' ? (
        <div className='subtitle-text'>Selamat Anda dinyatakan Real.</div>
      ) : label === 'fake' ? (
        <div className='subtitle-text'>Fake/Spoofed terdeteksi. Silakan coba lagi</div>
      ) : null}
    </div>
  );
}

export default Pasif;


/* // ini dipake buat app-1.py
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

function Pasif() {
  const [label, setLabel] = useState('');
  const [imageSrc, setImageSrc] = useState(null);

  useEffect(() => {
    const socket = io.connect('http://localhost:5000');

    socket.on('connect', () => {
      console.log('Connected to server');
    });

    socket.on('response_frame', (data) => {
      const imageStr = 'data:image/jpeg;base64,' + data.data;
      setImageSrc(imageStr);
      socket.emit('request_frame');
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from server');
      setImageSrc(null);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleLivenessDetection = () => {
    const data = {
      model_Path: 'LivenessNet.model',
      le_path: 'le.pickle',
      detector_folder: 'face_detector',
      confidence: 0.5,
    };

    fetch('http://localhost:5000/livenessnet', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        setLabel(data.label);
      })
      .catch((error) => console.error(error));
  };

  return (
    <div>
      <button onClick={handleLivenessDetection}>Detect Liveness</button>
      <p>{label}</p>
      {imageSrc && <img src={imageSrc} alt="Live video stream" />}
    </div>
  );
}

export default Pasif; */