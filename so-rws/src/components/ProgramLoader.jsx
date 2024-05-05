import React, { useState } from 'react';
import "./ProgramLoader.css";

function ProgramLoader({ sendJsonMessage }) {
  const [path, setPath] = useState('');
  const [priority, setPriority] = useState(0);
  const [instructions, setInstructions] = useState('');

  const handleSubmit = () => {
    console.log('Enviando programa', path, priority, instructions.split(',').map(instruction => instruction.trim()));
    sendJsonMessage({
      run: {
        path,
        priority,
        instructions: instructions.split(',').map(instruction => instruction.trim())
      }
    });
  };

  return (
    <div className="program-loader">
      <h2>Cargar programa</h2>
      <div className="path-priority-inputs">
        <label>
          Path:
          <input type="text" value={path} onChange={e => setPath(e.target.value)} />
        </label>
        <label>
          Prioridad:
          <input type="number" min="0" max="5" value={priority} onChange={e => setPriority(Number(e.target.value))} />
        </label>
      </div>
      <label>
        Instrucciones (separadas por comas):
        <textarea 
            style={{ fontFamily: "monospace" }}
            value={instructions} 
            onChange={e => setInstructions(e.target.value)} 
        />
      </label>
      <button onClick={handleSubmit}>Run</button>
    </div>
  );
}

export default ProgramLoader;