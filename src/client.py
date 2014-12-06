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

    menu_option = 'X'

    while menu_option.upper()!='F':
        menu = "Menu:\na) view all available slots\nb) delete slots\nc) view available time slots for another user\nd) book a meeting\ne) book a meeting for a list of attendees\nf) exit"

        print menu

        # get user input for menu choise
        menu_option = raw_input('Please select an option: ')
        
        # send the chosen menu option to the server
        clientSocket.send(menu_option)

        def list_availability():
            # receive and print dates for the next two weeks user can choose from
            choose_date = clientSocket.recv(1024)
            print choose_date

            # take in input for one of the dates in the next two weeks and send
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
            print user.upper() + "'s available slots on " + date + " are:\n" + availability
        elif menu_option.upper()=='D':
            list_availability()
            book_slot = raw_input('Enter one of the above time slots that you want to book: ')
            clientSocket.send(book_slot)
            acknowledgement = clientSocket.recv(1024)
            print acknowledgement
        elif menu_option.upper()=='E':
            attendees = raw_input('Enter names of attendees separated by commas (e.g. Ana, Bob, Joe): ')
            clientSocket.send(attendees)
            choose_date = clientSocket.recv(1024)
            print choose_date
            date = raw_input('Please select one of the above listed dates: ')
            clientSocket.send(date)
            time_frame = raw_input('Please enter a time frame on this date that you would like to schedule (e.g. 10:00 - 14:00): ')
            clientSocket.send(time_frame)
            print time_frame

            availability = clientSocket.recv(1024)
            if availability=="OK":
                print "The time slot " + time_frame + " is currently available for all attendees."
                book_slots = raw_input("Would you like to book this meeting for all listed attendees? (Y/N) ")
                clientSocket.send(book_slots.upper())
                acknowledgement = clientSocket.recv(1024)
                print acknowledgement
            else:
                print "The time slot " + time_frame + " is currently unavailable for at least one of the attendees."
        elif menu_option.upper()=='F':
            acknowledgement = clientSocket.recv(1024)
            print acknowledgement
        else:
            print "Invalid input."
            continue

# close client socket
clientSocket.close()
