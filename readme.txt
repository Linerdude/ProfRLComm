Setting up client server to text some of the code I am writing. The server will get the suggestions from a central computer and communicate it to one of two players on separate computers via websocket

Client receives a message, in the following format:
    Text:
    Block to suggest:

Server will send that message and translate it from a text file with the following;
    Valid ind:
    Ind that score high enough:
    Suggested gen:
    Suggested block:
    Block opp picked:

and client will send back which block was selected