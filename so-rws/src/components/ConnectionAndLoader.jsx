import ProgramLoader from './ProgramLoader';
import { Window, WindowHeader, WindowContent } from 'react95';
const ConnectionAndLoader = ({ sendJsonMessage, lastMessage, readyState }) => {
  return (
    <Window>
        <WindowHeader>ProgramLoader.exe</WindowHeader>
        <WindowContent>    
          <p>Estado de la conexión: {readyState}</p>
          <ProgramLoader sendJsonMessage={sendJsonMessage} />
        </WindowContent>
    </Window>
  )
}

export default ConnectionAndLoader