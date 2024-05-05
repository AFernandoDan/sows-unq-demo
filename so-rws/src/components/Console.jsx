import React from 'react'

const Console = ({ listaMensajes }) => {
  return (
    <div>
        <h2>Consola</h2>
        <div className="messages">
            {listaMensajes.map((mensaje, index) => (
                <p key={index}>{mensaje}</p>
            ))}
        </div>
    </div>
  )
}

export default Console