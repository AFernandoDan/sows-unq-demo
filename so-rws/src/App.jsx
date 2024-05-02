import useWebSocket, { ReadyState } from 'react-use-websocket';
import { useEffect, useState } from 'react';
import ProgramLoader from './components/ProgramLoader';

function App() {

  const [listaMensajes, setListaMensajes] = useState([])

  const {
    sendJsonMessage,
    lastMessage,
    readyState,
    getWebSocket
  } = useWebSocket('ws://localhost:8765'); // Reemplaza esto con tu URL de WebSocket

  // Run when the connection state (readyState) changes
  useEffect(() => {
    console.log("Connection state changed")
    if (readyState === ReadyState.OPEN) {
      // sendJsonMessage({
      //   run: {path: "prg1", priority: 1, instructions: ["CPU", "IO", "EXIT"]}
      // })
    }
  }, [readyState])

  useEffect(() => {
    if (lastMessage) {
      console.log("New message received: ", lastMessage.data)
      setListaMensajes([...listaMensajes, lastMessage.data])
    }
  }, [lastMessage])

  return <>
    <h1>Bienvenido al SISTEMA OPERATIVO</h1>
    <p>Estado de la conexión: {readyState}</p>
    <p>Último mensaje: {lastMessage ? lastMessage.data : 'Ninguno'}</p>
    <ProgramLoader sendJsonMessage={sendJsonMessage} />
    <h2>Consola</h2>
    {listaMensajes.map((mensaje, index) => (
      <p key={index}>{mensaje}</p>
    ))}
  </>
}

export default App