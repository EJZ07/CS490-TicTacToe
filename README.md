# Flask and create-react-app

## Requirements
1. `npm install`
2. `pip install -r requirements.txt`

## Setup
1. Run `echo "DANGEROUSLY_DISABLE_HOST_CHECK=true" > .env.development.local` in the project directory

## Run Application
1. Run command in terminal (in your project directory): `python app.py`
2. Run command in another terminal, `cd` into the project directory, and run `npm run start`
3. Preview web page in browser '/'

## Deploy to Heroku
*Don't do the Heroku step for assignments, you only need to deploy for Project 2*
1. Create a Heroku app: `heroku create --buildpack heroku/python`
2. Add nodejs buildpack: `heroku buildpacks:add --index 1 heroku/nodejs`
3. Push to Heroku: `git push heroku main`

## Problems I would fix 
1. Restricting each player to make a move when their turn. If there was more time I would 
address this by learning the proper way to use states and restricting the onclick function for each turn
2. If two users have the same name there's no way for the server to distinguish player 1 and player.
If I had more time I would address this by learning to proper way to send login information to the
server, possibly through a login id.

## Technical Issues
1. Directing the user to a different page was a big technical issue. I researched things such as `react-router-dom`
and `window.open()` but in the end simply rendering the page as a react component did the trick
2. The board information would run into issues when broadcasted to other clients. The issue was that the `socket.on`
function did not change the board state properly. To fix this I simply changed the `setBoard()` syntax to include the
previous board when updating the state.