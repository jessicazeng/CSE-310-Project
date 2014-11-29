__author__ = 'Jessica'

import sys
from socket import *

# Get the server hostname as command line argument
argv = sys.argv
host = argv[1]

# the server port is 6190
port = 6190

# create client socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# establish TCP connect to server port 6189
clientSocket.connect((host,port))

# get user input for their name
requestName = raw_input('Enter name: ')

# send the request name to the server
clientSocket.send(requestName)

server_reply = clientSocket.recv(1024)

if server_reply=="User not found.":
    print server_reply
else:
    print server_reply

    menu = "a) view all available slots\nb) delete slots\nc) view available time slots for another user\nd) book a meeting\ne) book a meeting for a list of attendees\nf) exit"

    print menu

    # get user input for menu choise
    menu_option = raw_input('Please select an option: ')
    
    # send the chosen menu option to the server
    clientSocket.send(menu_option)

    def list_availability():
        choose_date = clientSocket.recv(1024)
        print choose_date
        date = raw_input('Enter one of the above dates: ')
        clientSocket.send(date)
        availability = clientSocket.recv(1024)
        print "\nYour available slots on " + date + " are:\n" + availability

    if menu_option.upper()=='A':
        list_availability()
    elif menu_option.upper()=='B':
        choose_date = clientSocket.recv(1024)
        print choose_date
        date = raw_input('Enter one of the above dates: ')
        clientSocket.send(date)
        availability = clientSocket.recv(1024)
        
        if availability=="All slots open":
            print "\nAll the time slots on " + date + " are currently available."
        else:
            print "\nThe following time slots on " + date + " have been booked:\n" + availability
            delete_slot = raw_input('Enter the time slot you would like to delete: ')
            clientSocket.send(delete_slot)
            acknowledgement = clientSocket.recv(1024)
            print acknowledgement
    elif menu_option.upper()=='C':
        user = raw_input('Enter the name of the user: ')
        clientSocket.send(user)
        choose_date = clientSocket.recv(1024)
        print choose_date
        date = raw_input('Enter one of the above dates: ')
        clientSocket.send(date)
        availability = clientSocket.recv(1024)
        print user.upper + "'s available slots on " + date + " are:\n" + availability
    elif menu_option.upper()=='D':
        list_availability()
        book_slot = raw_input('Enter one of the above time slots that you want to book: ')
        clientSocket.send(book_slot)
        acknowledgement = clientSocket.recv(1024)
        print acknowledgement

# close client socket
clientSocket.close()
