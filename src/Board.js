import { useState, useEffect } from "react";
import { CalculateWinner, isBoardFull } from "./Winner.js";
import { io } from "socket.io-client";

const socket = io();
var turn = "X";
var player = " ";
var player_id;

export function Board(prop) {
  var winner;
  const [board, setBoard] = useState(Array(9).fill(null));
  const [playerBase, setPlayerBase] = useState([]);
  const [theScore, setTheScore] = useState({ player1: 100, player2: 100 });
  const [isShown, setIsShown] = useState(false);
  const [winState, setWinState] = useState(false);

  function Square({ value, onClick }) {
    //
    return (
      <div>
        <button class="box" onClick={onClick}>
          {value}
        </button>
      </div>
    );
  }

  function Restart() {
    return (
      <div>
        <button
          onClick={() => {
            setBoard(Array(9).fill(null));
            turn = "X";
            socket.emit("reset", { message: board, turn });
          }}
        >
          restart
        </button>
      </div>
    );
  }

  function Disconnect() {
    return (
      <div>
        <p>
          <button
            onClick={() => {
              socket.emit("goodbye", prop.message);
            }}
          >
            Leave Game
          </button>

          <button
            onClick={() => {
              socket.emit("goodbye_all");
            }}
          >
            Reset Every player
          </button>
        </p>
      </div>
    );
  }

  function RenderSquare(props) {
    return (
      <div>
        <Square
          value={board[props.i]}
          onClick={() => {
            if (winState === false) {
              if (player_id < 3 && board[props.i] === null) {
                var index = props.i;
                const nextBoard = board.slice();
                console.log("WHO???: " + index + " Player: " + player);

                if (turn === "X") {
                  nextBoard[index] = "X";
                  turn = "O";
                } else if (turn === "O") {
                  nextBoard[index] = "O";
                  turn = "X";
                }
                setBoard(nextBoard);
                winner = CalculateWinner(nextBoard);
                if (winner) {
                  socket.emit("score", { message: winner, playerBase });
                }
                socket.emit("tic", { message: nextBoard, turn, index });
              }
            }
          }}
        />
      </div>
    );
  }

  function getStatus() {
    winner = CalculateWinner(board);
    if (winner) {
      console.log("wINNER");

      if (winner === "X") {
        console.log("wINNER IS x");
        return "Winner: " + playerBase[0];
      } else if (winner === "O") {
        console.log("wINNER IS O");

        return "Winner: " + playerBase[1];
      }
    } else if (isBoardFull(board)) {
      return "Draw!";
    } else {
      if (turn === "X") {
        return "Player 1's turn";
      } else {
        return "Player 2's turn";
      }
    }
  }

  useEffect(() => {
    socket.on("name", (data) => {
      setPlayerBase(data[0]);

      console.log("Data " + data[1]);
      console.log("PlayerBase = " + playerBase + " Score: " + theScore);
    });

    socket.on("score", (data) => {
      console.log("Score updated");

      if (data["winner"] === "X") {
        setTheScore((prevScore) => {
          const score = data[1];
          return Object.assign({}, prevScore, { player1: score });
        });

        setTheScore((prevScore) => {
          const score = data[2];
          return Object.assign({}, prevScore, { player2: score });
        });
      } else {
        setTheScore((prevScore) => {
          const score = data[2];
          return Object.assign({}, prevScore, { player2: score });
        });

        setTheScore((prevScore) => {
          const score = data[1];
          return Object.assign({}, prevScore, { player1: score });
        });
      }

      setWinState(!winState); //WinState = True
    });

    socket.on(prop.message, ([playerType, data]) => {
      console.log(prop.message);
      console.log("Player " + playerType + " is here");
      console.log(data, playerType);

      if (playerType === 1) {
        player_id = 1;
        player = "Player 1";
      } else if (playerType === 2) {
        player_id = 2;
        player = "Player 2";
      } else {
        player_id = 3;
        player = "Spectator";
      }
    });

    // Listening for a chat event emitted by the server. If received, we
    // run the code in the function that is passed in as the second arg
    socket.on("tic", (data) => {
      console.log(data);
      // If the server sends a message (on behalf of another client), then we
      // add it to the list of messages to render it on the UI.\\

      setBoard((prevBoard) => {
        const nextBoard = prevBoard.slice();

        if (data.turn === "O") {
          nextBoard[data.index] = "X";
          turn = "O";
        } else {
          nextBoard[data.index] = "O";
          turn = "X";
        }

        return nextBoard;
      });
    });

    socket.on("reset", (data) => {
      setBoard(Array(9).fill(null));
      turn = "X";
      setWinState(false); //Change WinState to false
      console.log("Thw winstate issssss: " + winState);
    });

    socket.on("disconnect", () => {
      setPlayerBase(Array().fill(null));
    });
  }, []);

  function show(isHidden) {
    if (isShown) {
      return <div></div>;
    } else {
      return (
        <table class="table">
          <tr>
            <th>Players</th>
            <th>Score</th>
          </tr>
          <tr>
            <th>{playerBase[0]}</th>
            <th>{theScore["player1"]}</th>
          </tr>
          <tr>
            <th>{playerBase[1]}</th>
            <th>{theScore["player2"]}</th>
          </tr>
        </table>
      );
    }
  }

  return (
    <div>
      <h1>
        Hello {player} {prop.message}!
      </h1>
      <button
        class="show"
        onClick={() => {
          setIsShown(!isShown);
        }}
      >
        hide/show
      </button>
      <div className="leader">
        Leaderboard
        <ul>
          <div>{show(isShown)}</div>
        </ul>
      </div>
      <h2 className="game-info">{getStatus()}</h2>
      <div className="board">
        <RenderSquare i="0" />
        <RenderSquare i="1" />
        <RenderSquare i="2" />
        <RenderSquare i="3" />
        <RenderSquare i="4" />
        <RenderSquare i="5" />
        <RenderSquare i="6" />
        <RenderSquare i="7" />
        <RenderSquare i="8" />
      </div>
      <div class="Restart">
        <Restart />
      </div>
      <div class="leave">
        <Disconnect />
      </div>
      <p1 class="lobby">
        Lobby:
        <ul class="list">
          {playerBase.map((item, index) => (
            <div>{playerBase[index]}</div>
          ))}
        </ul>
      </p1>
    </div>
  );
}

export default Board;
