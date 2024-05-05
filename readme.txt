Website: https://cachemoney.me/

Part 3 Obj 3 Description: Betting
    In an attempt to promote gambling and encourage addicts to play we have included betting. 
    The player is allowed to bet on their hand and the possibility to get closer than the dealer to 21 without going over.
    If the player bets & wins their balance increases allowing them to bet more in the next game they play.
    If the player bets & loses the credits are removed from their balance allowing them to bet fewer credits in the next game they play.


Part 3 Obj 3 Testing Procedure:
    1. Go to localhost after doing docker compose up or go to cachemoney.me.
    2. Register an account with a valid username & password. You receive 100 credits upon registration.
    3. Click on the PLAY button.
    4. Create a table.
    5. Press the Start Now button.
    6. The + and - buttons increase or decrease your bet amount. Increase your bet to 5 credits and play the game. (Optional) Press stand to end your turn.
    7. There are six possible endings. The output is shown to you in a popup modal when a game ends. Press the X to return to the main menu and repeat steps 3-6 to test all of them and ensure betting is handled correctly:
        a. Player & dealer are the same distance from 21 - Credits are refunded (+-0).
        b. Player & dealer both go over 21 - Credits are refunded (+-0).
        c. Only player busts - You lose your bet (-5).
        d. Only dealer busts - Your bet is refunded and you receive an additional bet amount (+5).
        e. Dealer is closer to 21 - You lose your bet (-5).
        f. Player is closer to 21 - Your bet is refunded and you receive an additional bet amount (+5).
    
