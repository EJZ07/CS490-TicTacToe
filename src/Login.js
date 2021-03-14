import React, { useState, useRef } from 'react';
import { io } from 'socket.io-client';
import { Board } from './Board';

const socket = io();

export function TheLogin() {
  const [isLogin, setIsLogin] = useState(false);
  const inputRef = useRef(null);

  if (!isLogin) {
    return (
      <div>
        <h1>Enter your username</h1>
        <input ref={inputRef} type="text" />
        <button
          className="loginButon"
          onClick={() => {
            const message = inputRef.current.value;
            socket.emit('name', { message });

            setIsLogin(!isLogin);
          }}
        >
          Login
        </button>
      </div>
    );
  }
  const message = inputRef.current.value;
  return <Board message={message} socket={socket} />;
}

export default TheLogin;
