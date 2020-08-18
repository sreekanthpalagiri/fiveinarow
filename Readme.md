Five-in-a-row
------------------------------

Starting The Game
-----------------------
1) Launch the Server -  python server.py

2) Launch Client twice - python client.py


Assumptions
------------------
1) At any point of time two players can connect to the server. If 3rd player connects it client will show message and end.
2) If any player terminates game, his client disconnects and also opponent clients disconnects showing the message Oppononent Disconnected.
3) Client disconnects after game completes. A new game can be launched again by launching client again.

Testing - Code coverage
----------------------------------------------
Run Below: 

    1) coverage run test.py
    
    2) coverage report -m 
    
    3) coverage html  - For HTML report

Coverage Report of my testing is present in htmlcov folder. Please refer index.html
