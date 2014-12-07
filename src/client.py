__author__ = 'Jessica'

import sys
from socket import *

# Get the server hostname as command line argument
argv = sys.argv
host = argv[1]

# the server port is 6190
port = 6191

# create client socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# establish TCP connect to server port 6189
clientSocket.connect((host,port))

# get user input for their email
requestEmail = raw_input('E-mail: ')

# get user input for their password
requestPass = raw_input('password: ')

# send the request email to the server
clientSocket.send(requestEmail)

# send the request password to the server
clientSocket.send(requestPass)

# get server ack for whether user was found.
server_reply = clientSocket.recv(1024)
if server_reply=="User not found.":
    print server_reply
else:
    print server_reply

    # initialize menu_option
    menu_option = 'X'
    while menu_option.upper()!='F': # loop while menu_option isn't F to exit
        # print menu
        menu = "Menu:\na) view all available slots\nb) delete slots\nc) view available time slots for another user\nd) book a meeting\ne) book a meeting for a list of attendees\nf) exit"
        print menu

        # get user input for menu choise
        menu_option = raw_input('Please select an option: ')

        try:
            # send the chosen menu option to the server
            clientSocket.send(menu_option)
            
            # function to print client's available time slots for a given date
            def list_availability():
                # receive and print dates for the next two weeks user can choose from
                choose_date = clientSocket.recv(1024)
                print "Please choose from one of the following dates:\n" + choose_date

                # take in input for one of the dates in the next two weeks and send
                date = raw_input('Enter one of the above dates: ')
                clientSocket.send(date)

                # get and print client's available time slots for date
                availability = clientSocket.recv(1024)
                print "\nYour available slots on " + date + " are:\n" + availability

            if menu_option.upper()=='A': # user chose menu option A
                # print client's available time slots for a given date
                list_availability()
            elif menu_option.upper()=='B':# user chose menu option B
                # get and print list of dates from server
                choose_date = clientSocket.recv(1024)
                print "Please choose from one of the following dates:\n" + choose_date

                # ask client to choose a date from list and send back to server
                date = raw_input('Enter one of the above dates: ')
                clientSocket.send(date)

                # this variable determines if the date has any booked time slots
                availability = clientSocket.recv(1024)
                
                if availability=="All slots open": # server doesn't return a list of time slots
                    print "\nAll the time slots on " + date + " are currently available.\n"
                else: # server returns a list of time slots
                    # print list of booked time slots
                    print "\nThe following time slots on " + date + " have been booked:\n" + availability
                    # ask user and get input for the time slot they want to delete and send to server
                    delete_slot = raw_input('Enter the time slot you would like to delete: ')
                    clientSocket.send(delete_slot)
                    # get acknowledgement from server whether slot was successfully deleted
                    acknowledgement = clientSocket.recv(1024)
                    print acknowledgement
            elif menu_option.upper()=='C': # user chose menu option C
                # ask and get client input for name of another user they would like to see availability for
                user = raw_input('Enter the name of the user: ')
                # send input to server
                clientSocket.send(user)

                # get list of dates from server and print it
                choose_date = clientSocket.recv(1024)
                print "Enter one of the following dates you would like to view the availability for:\n" + choose_date

                # client chooses one date to view availability for the user and send to server
                date = raw_input('Enter one of the above dates: ')
                clientSocket.send(date)

                # get list of availability for date for the user from server
                availability = clientSocket.recv(1024)
                print user.upper() + "'s available slots on " + date + " are:\n" + availability
            elif menu_option.upper()=='D': # user chose menu option D
                #  call function to print client's available time slots for a given date
                list_availability()

                # ask user to choose a time slot he/she wants to book and send to server
                book_slot = raw_input('Enter one of the above time slots that you want to book: ')
                clientSocket.send(book_slot)

                # get booking acknowledgement from server and print
                acknowledgement = clientSocket.recv(1024)
                print acknowledgement
            elif menu_option.upper()=='E': # user chose menu option E
                # get input of users client wants to attend a meeting with
                attendees = raw_input('Enter names of attendees separated by commas (e.g. Ana, Bob, Joe): ')
                clientSocket.send(attendees)

                # get list of dates within next two weeks from server 
                choose_date = clientSocket.recv(1024)
                print choose_date

                # get input for the date the client wants to book a meeting on and send to server
                date = raw_input('Please select one of the above listed dates: ')
                clientSocket.send(date)

                # get a time frame the client wants to book the meeting for
                time_frame = raw_input('Please enter a time frame on this date that you would like to schedule (e.g. 10:00 - 14:00): ')
                clientSocket.send(time_frame)

                # this response from server determines if all the attendees are available for the meeting time frame
                availability = clientSocket.recv(1024)
                if availability=="OK": # all attendees are available
                    print "The time slot " + time_frame + " is currently available for all attendees."
                    # confirm if client wants to book this time slot for all attendees
                    book_slots = raw_input("Would you like to book this meeting for all listed attendees? (Y/N) ")
                    clientSocket.send(book_slots.upper())
                    # get ack from server if the meeting was successfully booked and emails sent
                    acknowledgement = clientSocket.recv(1024)
                    print acknowledgement
                else:
                    print "The time slot " + time_frame + " is currently unavailable for at least one of the attendees."
            elif menu_option.upper()=='F': # user chose menu option F to exit
                # get the ok to exit session and print to client screen
                acknowledgement = clientSocket.recv(1024)
                print acknowledgement
            else: # user inputted invalid menu option
                print "Invalid input."
                # stop this loop and print menu again
                continue
        except:
            print "Request timed out."

# close client socket
clientSocket.close()
