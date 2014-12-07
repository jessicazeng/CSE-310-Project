1. 	Necessary Files
	To run this application, the following files must be present: 

	client.py - This is the client server file

	server.py - This is the server file

	input.txt - This file includes user names, emails and passwords, respectively separated by spaces.

	textfile.txt - A blank text file.

2. 	Running the Program
	This meeting scheduler program runs on Linux machines using the command-line. The server and text files must be transfered to the SSH machine before running it. To start the program, two machines must be running at the same time. For example, use the allv24.all.cs.stonybrook.edu linux machine to run the server and the allv25.all.cs.stonybrook.edu linux machine to run the client server. To run the server, input the command: python server.py. To run the client, input the command: python client.py [server hostname]. Following the example, the client command would be: python client.py allv24.all.cs.stonybrook.edu. 