import logo from './logo.svg';
import { useState, useRef, useEffect} from 'react';
import io from 'socket.io-client';

const socket = io(); // Connects to socket connection
var count=0;

export function RenderSquare(props) {
  
  const [board, setBoard] = useState(Array(9).fill(null));
  const nextBoard = useRef(null);
    
  function Square({value, onClick}) {
  //
    return <div>
        <button class="box" onClick={onClick}>{value}</button>
      </div>;
  
  }
  
  useEffect(() => {
    // Listening for a chat event emitted by the server. If received, we
    // run the code in the function that is passed in as the second arg
    socket.on('tic', (data) => {
      console.log('Player event received!');
      console.log(data);
      // If the server sends a message (on behalf of another client), then we
      // add it to the list of messages to render it on the UI.\
       if(data.count % 2 === 0){
          data.nextBoard[data.index] = 'X';
        }else{
          data.nextBoard[data.index] = 'O';
        } 
      count++;
      setBoard(data.nextBoard, nextBoard);
    });
  }, []);
  
  return ( <div>
  
    <Square 
      value={board[props.i]}
      onClick={() => {
      if (nextBoard != null){
         var index = props.i;
         const nextBoard = board.slice();
        if(count % 2 === 0){
          nextBoard[index] = 'X';
        }else{
          nextBoard[index] = 'O';
        }
        setBoard(nextBoard);
        socket.emit('tic', { message: setBoard, nextBoard, count, index });
       
      }
       
      }}/>
      
      
  
  </div>
  
  
    
    );
  
}





