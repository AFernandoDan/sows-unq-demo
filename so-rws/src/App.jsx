import useWebSocket, { ReadyState } from 'react-use-websocket';
import { useEffect, useState } from 'react';
import './App.css';
import ConnectionAndLoader from './components/ConnectionAndLoader';
import Console from './components/Console';

function App() {

  const [listaMensajes, setListaMensajes] = useState([])

  const {
    sendJsonMessage,
    lastMessage,
    readyState,
    getWebSocket
  } = useWebSocket('ws://localhost:8000'); // Reemplaza esto con tu URL de WebSocket

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

  return <main>
    <h1>Bienvenido al SISTEMA OPERATIVO</h1>
    <div className="container">
      <ConnectionAndLoader sendJsonMessage={sendJsonMessage} lastMessage={lastMessage} readyState={readyState} />
      <Console listaMensajes={listaMensajes} />
    </div>
  </main>
}

export default App