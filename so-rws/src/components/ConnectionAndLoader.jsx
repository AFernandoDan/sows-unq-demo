import ProgramLoader from './ProgramLoader';

const ConnectionAndLoader = ({ sendJsonMessage, lastMessage, readyState }) => {
  return (
    <div>
        <p>Estado de la conexión: {readyState}</p>
        <p>Último mensaje: {lastMessage ? lastMessage.data : 'Ninguno'}</p>
        <ProgramLoader sendJsonMessage={sendJsonMessage} />
    </div>
  )
}

export default ConnectionAndLoader