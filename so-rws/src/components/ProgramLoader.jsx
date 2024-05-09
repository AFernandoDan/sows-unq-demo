import React, { useState } from 'react';
import { Button, NumberInput, TextInput } from 'react95';

function ProgramLoader({ sendJsonMessage }) {
  const [path, setPath] = useState('');
  const [priority, setPriority] = useState(0);
  const [instructions, setInstructions] = useState('');

  const handleSubmit = () => {
    sendJsonMessage({
      event: 'run',
      data: {
        path,
        priority,
        instructions: instructions.split(',').map(instruction => instruction.trim())
      }
    });
  };

  return (
    <div>
      <h2>Cargar programa</h2>
      <div>
        <label>
          Path:
          <TextInput value={path} onChange={e => setPath(e.target.value)} placeholder="prg1" />
        </label>
        <label>
          Prioridad:
          <NumberInput defaultValue={0} min={0} max={5} onChange={n => setPriority(n)} />
        </label>
      </div>
      <label>
        Instrucciones (separadas por comas):
        <TextInput
          multiline 
          rows={4} 
          value={instructions} 
          onChange={e => setInstructions(e.target.value)} 
          placeholder='CPU, IO, EXIT' />
      </label>
      <Button fullWidth onClick={handleSubmit}>Run</Button>
    </div>
  );
}

export default ProgramLoader;