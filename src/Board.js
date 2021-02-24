import logo from './logo.svg';
import { useState, useRef, useEffect} from 'react';
import io from 'socket.io-client';

const socket = io(); // Connects to socket connection
var turn = 'X';

export function RenderSquare(props) {
  
  const [board, setBoard] = useState(Array(9).fill(null));
  const [isNext, setIsNext] = useState(true);
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
      // add it to the list of messages to render it on the UI.\\
    
      setBoard(prevBoard => {
        const nextBoard = prevBoard.slice();
        
        if (data.turn === 'O'){
          nextBoard[data.index] = 'X';
          turn = 'O';
        }else{
          nextBoard[data.index] = 'O';
          turn = 'X';
        }
        console.log(isNext);
        return nextBoard;
      });
     
    });
  }, []);
  
  return ( <div>
  
    <Square 
      value={board[props.i]} 
      onClick={() => {
      
        var index = props.i;
        const nextBoard = board.slice();
        if (turn === 'X'){
          nextBoard[index] = 'X';
          turn = 'O';
        }else{
          nextBoard[index] = 'O';
          turn = 'X';
          
        }
        
        setBoard(nextBoard);
        console.log(board);
        socket.emit('tic', { message: isNext, turn, board, index });
       
      }}/>

  </div>

    );
  
}





