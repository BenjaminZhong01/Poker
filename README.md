# f22_team_20
The Product Backlog
1. User Information actions
    Register - Create a new user on the website.
    Login - Authenticated user website login action.
    Logout - Authenticated user website logout action.
    Access user profile - See the user’s profile with the user’s information on it.
2. Room Logics
    Enter the game room - The current user can enter any existing game room.
    Exit the game room - The current user can exit the game room that he/she is in.
3. Game Logics
    Preparation for the game - Each player that’s in the game room could be prepared for a game. Once all players in the game room are prepared, the application would start a new game.
    Create a new game - When all players in one room are prepared, start a game.
    Play game - Synchronous interaction among players, includes many functions such as win/lose judgment, tokens distribution, and credits calculation
4. Global Info
    Leader Board - A board that demonstrates current users' credit ranking, from highest to lowest.

Optional Function
**Payment Function - Users could pay for tokens to start a game.

The First Sprint Backlog - Product Owner: Yunshan Zhang
1. User Information actions - Junhui Li
    Register
    Login
    Logout
2. Room Logics - Yunshan Zhang
    Enter the game room - Working HTML pages
    Exit the game room - Working HTML pages
3. Global Info - Yunshan Zhang
    Leader Board - Working HTML pages. Demonstrate database user data, currently without AJAX approach
4. Game Logics - Haoxuan Yuan, Renjie Zhong
    Preparation for the game - Working HTML pages
    Create a new game - Working HTML pages
    Play game - Working HTML pages

The Second Sprint Backlog - Product Owner: Benjamin Zhong (renjiez)
1. Payment Research - Junhui Li
    Research about 3rd-party payment methods   
2. Room Logics - Yunshan Zhang
    Ajax updating room page
    Delete room in db if no one in the room
    Update room model design based on game needs
3. Game Functions - Haoxuan Yuan
    Game Operation: Deal/Call/Fold
4. Game Logics - Benjamin Zhong
    Continue work on game logics design, specific in the flop/turn/river round of betting
    Test the accoutability, stability and accuracy of the backend game logics