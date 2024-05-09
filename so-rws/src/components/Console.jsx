import React, { useEffect, useRef } from 'react'
import { ScrollView, WindowHeader, Window, WindowContent } from 'react95'

const Console = ({ listaMensajes }) => {

  const scrollViewRef = useRef(null)

  useEffect(() => {
    if (scrollViewRef.current) {
      // set scroll to bottom
      if (scrollViewRef.current.firstChild) {
        scrollViewRef.current.firstChild.scrollTop = 
          scrollViewRef.current.firstChild.scrollHeight
      }
    }
  }, [listaMensajes])

  return (
    <div>
        <Window>
          <WindowHeader>Command Prompt: running remote OS.exe</WindowHeader>
          <WindowContent>
            <ScrollView style={{ height: '200px', width: '600px' }} ref={scrollViewRef}>
              <div className="messages">
                  {listaMensajes.map((mensaje, index) => (
                      <p key={index}>{mensaje}</p>
                  ))}
              </div>
            </ScrollView>
          </WindowContent>
        </Window>
    </div>
  )
}

export default Console