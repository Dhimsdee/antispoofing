import React, { useState } from 'react';

function Aktif() {
  const [stream, setStream] = useState(null);

  const startStream = () => {
    setStream(new ReadableStream({
      start(controller) {
        fetch('http://localhost:5000/activenessnet', {
          method: 'POST'
        }).then(response => {
          const reader = response.body.getReader();
          function read() {
            reader.read().then(({ done, value }) => {
              if (done) {
                controller.close();
                return;
              }
              controller.enqueue(value);
              read();
            });
          }
          read();
        });
      }
    }));
  };

  return (
    <div>
      <button onClick={startStream}>Start Liveness Detection</button>
      {stream && <img src={URL.createObjectURL(stream)} alt="Stream" />}
    </div>
  );
}

export default Aktif;
