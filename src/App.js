import logo from './logo.svg';
import './App.css';
import { Board } from './Board.js';
import { useState, useRef, useEffect } from 'react';
import io from 'socket.io-client';


const socket = io();

function App() {
    const [isLogin, setIsLogin] = useState(false);
    const inputRef = useRef(null);
    function TicTacToe(){
       
        if(isLogin){
            return <TheGame />;
        }
        return <TheLogin />;
        
    }
    
    function TheLogin(){
        
        return (<div>
            <h1>Enter your username</h1>
            <input ref={inputRef} type="text" />
            <button onClick={ () => {
                    const message = inputRef.current.value; 
                    socket.emit("name", {message});
                               
                    setIsLogin(prevLogin => {
                        setIsLogin(!isLogin);
                    });
                   
                }}>Board</button>
            </div>
            );
    }
    
    function TheGame(){
        const message = inputRef.current.value; 
        return <Board message={message}/>;
    }
            
    
       
    return(<div>
    
       <TicTacToe />
       
       </div>
        );
   
}
export default App;
