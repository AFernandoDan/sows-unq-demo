import React from 'react';
import { Button, Frame, MenuList, MenuListItem, Monitor, Separator, styleReset, WindowHeader } from 'react95';
import { createGlobalStyle, ThemeProvider } from 'styled-components';

/* Pick a theme of your choice */
import original from 'react95/dist/themes/original';

/* Original Windows95 font (optional) */
import ms_sans_serif from 'react95/dist/fonts/ms_sans_serif.woff2';
import ms_sans_serif_bold from 'react95/dist/fonts/ms_sans_serif_bold.woff2';

import useWebSocket, { ReadyState } from 'react-use-websocket';
import { useEffect, useState } from 'react';
import ConnectionAndLoader from './components/ConnectionAndLoader';
import Console from './components/Console';

const GlobalStyles = createGlobalStyle`
  ${styleReset}
  @font-face {
    font-family: 'ms_sans_serif';
    src: url('${ms_sans_serif}') format('woff2');
    font-weight: 400;
    font-style: normal
  }
  @font-face {
    font-family: 'ms_sans_serif';
    src: url('${ms_sans_serif_bold}') format('woff2');
    font-weight: bold;
    font-style: normal
  }
  body, input, select, textarea {
    font-family: 'ms_sans_serif';
  }
`;

const App = () => {
    const [listaMensajes, setListaMensajes] = useState([])
    const [power, setPower] = useState(false)

    // connect to /post
    const { 
      sendJsonMessage: sendJsonMessagePost, 
      lastMessage: lastMessagePost,
      readyState: readyStatePost,
      getWebSocket: getWebSocketPost } = useWebSocket('ws://localhost:8000/POST');

    const {
      sendJsonMessage,
      lastMessage,
      readyState,
      getWebSocket
    } = useWebSocket('ws://localhost:8000/'); // Reemplaza esto con tu URL de WebSocket
  
    // Run when the connection state (readyState) changes
    useEffect(() => {
      if (readyState === ReadyState.OPEN) {
        // sendJsonMessage({
        //   run: {path: "prg1", priority: 1, instructions: ["CPU", "IO", "EXIT"]}
        // })
      }
    }, [readyState])
  
    useEffect(() => {
      if (lastMessage) {
        setListaMensajes(prev => [...prev, lastMessage.data])
      }
    }, [lastMessage])

    const handleSwitch = () => {
        if (readyStatePost === ReadyState.OPEN) {
            sendJsonMessagePost({
                event: 'switch',
            })
        }
    }

    return (
        <div>
            <GlobalStyles />
            <ThemeProvider theme={original}>
                    <Button onClick={handleSwitch}>ON/OFF</Button>
                    <WindowHeader>Bienvenido al SISTEMA OPERATIVO.exe</WindowHeader>
                    {/* <Monitor backgroundStyles={{ background: 'blue' }} /> */}
                    <ConnectionAndLoader sendJsonMessage={sendJsonMessagePost} lastMessage={lastMessage} readyState={readyState} />
                    <Console listaMensajes={listaMensajes} />
            </ThemeProvider>
        </div>
    );
}

export default App;