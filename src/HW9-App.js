import logo from './logo.svg';
import './App.css';
import { RenderSquare } from './Board.js';

function App() {

 return (
    <div class="board">
       <RenderSquare i="1" />
       <RenderSquare i="2" />
       <RenderSquare i="3" />
       <RenderSquare i="4" />
       <RenderSquare i="5" />
       <RenderSquare i="6" />
       <RenderSquare i="7" />
       <RenderSquare i="8" />
       <RenderSquare i="9" />
    </div>
    );
}


export default App;