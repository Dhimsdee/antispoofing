import React, { useState } from 'react';

function Aktif() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const startStream = () => {
    setLoading(true);
    fetch('http://localhost:5000/activenessnet', {
      method: 'POST'
    }).then(response => {
      const reader = response.body.getReader();
      function read() {
        reader.read().then(({ done, value }) => {
          if (done) {
            setLoading(false);
            return;
          }
          const decodedValue = new TextDecoder().decode(value);
          const resultObject = JSON.parse(decodedValue);
          setResult(resultObject.label);
          read();
        });
      }
      read();
    });
  };

  return (
    <div>
      <div className='button_primary'> 
      <button className='btn' onClick={startStream}>Detect Liveness</button>
      </div>
      <div className='button_primary'> 
      {loading && <p>Loading...</p>}
      </div>
      {result !== null && <p>{result}</p>}
    </div>
  );
}

export default Aktif;
