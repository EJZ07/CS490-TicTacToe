import { render, screen, fireEvent } from "@testing-library/react";
import App from "./App";
import Board  from './Board'

test("Show and Hide Leaderboard", () => {
  const result = render(<Board />);
  
  const showLeaderBoard = screen.getByText('leader');
  expect(showLeaderBoard).toBeInTheDocument();
  
  fireEvent.click(showLeaderBoard)
  expect(showLeaderBoard).not.toBeInTheDocument();
});
