__author__ = 'Jessica'

# http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python

from socket import *
from string import rstrip
import os
import datetime
import re

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

#Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)

#bind socket to local port number 6190
serverSocket.bind(('', 6190))

#server listens for incoming TCP connection requests - max number of queued
#clients - 1
serverSocket.listen(1)

#open and read the input file that contains user info
user_list = open('input.txt', 'r')

# initialize arrays to store lists of users, emails, and passwords
users = []
emails = []
passwords = []

# append users, emails, and passwords from user_list
for line in user_list:
        line_array = line.rstrip().split(' ')
        users.append(line_array[0].upper())
        emails.append(line_array[1])
        passwords.append(line_array[2])

#initialize array of dates for the next two weeks starting from today
nextTwoWeeks = []
# append dates for the next two weeks into nextTwoWeeks array
for x in range(0, 14):
        next_date = datetime.date.today() + datetime.timedelta(x)
        nextTwoWeeks.append(str(next_date.month) + "-" + str(next_date.day))            

# function that returns the line number given a line and file contents
def find_line(file_content, line):
        # initialize line_number to -1 so that we know line wasn't found
        line_number = -1
        # loop through all lines in file_content
        for num, l in enumerate(file_content, 1):
                # if line was found in file, break out of loop
                if line==l.rstrip():
                        line_number = num
                        break
        return line_number

# function that checks if a time slot has already been booked or not
# returns True if not booked
def checkAvailableSlots(timeSlot, file, day):
        # gets index of the date from nextTwoWeeks array
        indexinNTW = nextTwoWeeks.index(day)
        # find what line in the file the time slots for the given date starts at
        start_line = find_line(file, day)
        # find what line in the file the time slots for the given date ends at
        end_line = find_line(file, nextTwoWeeks[indexinNTW+1])

        # available variable determines if the time slot is available
        available = True
        # loop through lines that the time slots are in in the file
        for x in range(start_line, end_line):
                # if the time slot is found, set the slot to unavailable and break out of loop
                if timeSlot==file[x].rstrip():
                        available=False
                        break
        return available

while True:
        print "Ready to serve..."
	# creates client socket in server and gets address
	client, address = serverSocket.accept()

	try:
		# get client name
		name = client.recv(1024).upper()
	except:
		#Send error message
        	client.send('User not found.')
        	# close client socket
        	client.close()
        	# end current session and starts new loop
        	continue

        person_found = False;
		
	# check if name is in user_list
	if any(name in s for s in users):
                person_found = True;

        # if person is on user list server responds to client with acknowledgement
        if (person_found == True):
                response = "Hello, " + name
        else:
                response = "User not found."

        # send response whether the person was found or not
        client.send(response)

        if (person_found == False):
                # close client socket
                client.close()
                # end current session and starts new loop
                continue

        # name of the user's availability file
        fname = name + ".txt"

        if os.path.isfile(fname): # if file exists, open
                user_file = open(fname, "a+")
        else: # if file does not exist, create new file
                user_file = open(fname, "a+")
                # get today's date
                d = datetime.date.today()
                # write the dates for the next two weeks in file as a divider for time slots for each date
                for x in range(0, 14):
                        next_date = d + datetime.timedelta(x)
                        user_file.write(str(next_date.month) + "-" + str(next_date.day) + "\n")                      
                # set pointer to beginning of file
                user_file.seek(0)
                
        # store the lines in the file in file_content
        file_content = user_file.readlines()

        # for files that already exists, check and append dates for the next two weeks if it isn't in there
        for y in nextTwoWeeks:
                if find_line(file_content, y)==-1:
                        user_file.write(y + "\n")
        # close the file
        user_file.close()

        # open and read the updated lines back into file_content and close file
        user_file = open(fname, "r")
        file_content = user_file.readlines()
        user_file.close()

        # check if file contains past dates and time slots before today's date
        start_index = find_line(file_content, nextTwoWeeks[0])
        # if start_index is not equal to 1, then file_contents contains past dates and/or slots
        if start_index!=1:
                # overwrite user_file with only lines for next two weeks
                user_file = open(fname, "w")
                for x, line in enumerate(file_content, 1):
                        # skip over lines before the line for today's date
                        if x not in range(0, start_index):
                                user_file.write(line)
                # close file
                user_file.close()

        # initialize option variable
        option = 'X'
        # loops runs as long as user does not select 'F' menu option to exit
        while option!='F':
                try:
        		# get menu option chosen by user
        		option = client.recv(1024).upper()
        	except:
        		#Send error message
                	client.send('Transaction failed.')
                	# close client socket
                	client.close()
                	# end current session and starts new loop
                	continue

                # function to view all available slots for a user
                def a(file_content, day):
                        # initialize availability variable
                        availability = ""
                        # check all hours in a day if it is available
                        for hour in range(0, 24):
                                # first check first half hour of each hour (xx:00 - xx:30)
                                timeSlot = str(hour) + ":00 - " + str(hour) + ":30"
                                # use timeSlot in checkAvailableSlots to check if it is available
                                available_time = checkAvailableSlots(timeSlot, file_content, day)
                                #if it is, append to availability
                                if available_time==True:
                                        availability = availability + timeSlot + "\n"

                                # next check second half hour of each hour (xx:30 - xx:00)
                                # if the hour is 23:30, then instead of 24:00, change to 0:00
                                if hour==23:
                                        timeSlot2 = str(hour) + ":30 - " + str(0) + ":00"
                                        # use timeSlot in checkAvailableSlots to check if it is available
                                        available_time = checkAvailableSlots(timeSlot2, file_content, day)
                                        #if it is, append to availability
                                        if available_time==True:
                                                availability = availability + timeSlot2 + "\n"
                                else:
                                        timeSlot2= str(hour) + ":30 - " + str(hour+1) + ":00"
                                        # use timeSlot in checkAvailableSlots to check if it is available
                                        available_time = checkAvailableSlots(timeSlot2, file_content, day)
                                        #if it is, append to availability
                                        if available_time==True:
                                                availability = availability + timeSlot2 + "\n"
                        # send availability to client
                        client.send(availability)

                # function checks if a specified user is available given a time slot
                # returns false if not available
                def person_available(user, time_slots, day):
                        # open file
                        # name of the user's availability file
                        fname2 = user + ".txt"
                        if os.path.isfile(fname2): # if file exists, open
                                user_file2 = open(fname2, "r")
                        else: # if file does not exist, create new file
                                user_file2 = open(fname2, "a+")
                                # get today's date
                                d = datetime.date.today()
                                # write dates for next two weeks into new user's file
                                for x in range(0, 14):
                                        next_date = d + datetime.timedelta(x)
                                        user_file2.write(str(next_date.month) + "-" + str(next_date.day) + "\n")                      
                                # set pointer to beginning of file
                                user_file2.seek(0)

                        # read file content into file_content2 variable
                        file_content2 = user_file2.readlines()
                        # close the user's file
                        user_file2.close()

                        # loop through time slots and check if user is available
                        # if not available for one slot, return false
                        for slot in time_slots:
                                if checkAvailableSlots(slot, file_content2, day)==False:
                                        return False
                        return True                                

                # user selected menu option A
                if option=='A':
                        try:
                                # create a string of date for the next two weeks for client to choose from
                                choose_date = "Please choose from one of the following dates:\n"
                                for date in nextTwoWeeks:
                                        if date==nextTwoWeeks[13]:
                                                choose_date += date
                                        else:
                                                choose_date += date + ", "
                                # send the list of dates for client to choose from to client
                                client.send(choose_date)
                                # get chosen date from client
                                day = client.recv(1024)
                                # call function to send client their available time slots for chosen date
                                a(file_content, day)
                        except:
                                #Send error message
                                client.send('Transaction failed.')
                                # close client socket
                                client.close()
                                # end current session and starts new loop
                                continue
                elif option=='B': # user selected menu option B
                        try:
                                # create a string of date for the next two weeks for client to choose from
                                choose_date = "Please choose from one of the following dates you would like to delete a time slot from:\n"
                                for date in nextTwoWeeks:
                                        if date==nextTwoWeeks[13]:
                                                choose_date += date
                                        else:
                                                choose_date += date + ", "
                                # send the list of dates for client to choose from to client
                                client.send(choose_date)
                                # get chosen date from client
                                day = client.recv(1024)

                                # open user file to overwrite
                                user_file = open(fname, "w")

                                # create string of client's currently booked time slots
                                availability = ""
                                # check availability of all hours in specified date
                                for hour in range(0, 24):
                                        # first check first half hour in each hour (xx:00 - xx:30)
                                        timeSlot = str(hour) + ":00 - " + str(hour) + ":30"
                                        # call checkAvailableSlots function to determine if this time slot is available
                                        available_time = checkAvailableSlots(timeSlot, file_content, day)
                                        # if it isn't, append to availability
                                        if available_time==False:
                                                availability = availability + timeSlot + "\n"

                                        #check second half hour in each hour (xx:30 - xx:00)
                                        if hour==23: # if time is 23:30, set to 23:30 - 0:00
                                                timeSlot2 = str(hour) + ":30 - " + str(0) + ":00"
                                                # call checkAvailableSlots function to determine if this time
                                                available_time = checkAvailableSlots(timeSlot2, file_content, day)
                                                if available_time==False:
                                                        availability = availability + timeSlot2 + "\n"
                                        else:
                                                timeSlot2= str(hour) + ":30 - " + str(hour+1) + ":00"
                                                # call checkAvailableSlots function to determine if this time
                                                available_time = checkAvailableSlots(timeSlot2, file_content, day)
                                                # if it isn't, append to availability
                                                if available_time==False:
                                                        availability = availability + timeSlot2 + "\n"
                                # if not slots are booked for the specified date, send message that all slots are open
                                if availability=="":
                                        availability = "All slots open"
                                        client.send(availability)
                                else: 
                                        # else send list of booked slots for the specified date
                                        client.send(availability)

                                        # get slot user wants to delete
                                        delete_slot = client.recv(1024)
                                        # loop through file_content, overwrite, and write all lines besides the deleted time slots
                                        for line in file_content:
                                                if line.rstrip()!=delete_slot.rstrip():
                                                        user_file.write(line)

                                        # send acknowledgement that the slot was successfully deleted
                                        acknowledgement = "The time slot " + delete_slot + " has been successfully deleted, and and is currently available to be booked.\n"
                                        client.send(acknowledgement)
                                # close the user's file
                                user_file.close()

                                # open user file again to update file_content to accommodate the deleted time slots
                                user_file = open(fname, "r")
                                file_content = user_file.readlines()
                                user_file.close()
                        except:
                                #Send error message
                                client.send('Transaction failed.')
                                # close client socket
                                client.close()
                                # end current session and starts new loop
                                continue
                elif option=='C': # user selected menu option C
                        try:
                                # get the name of another user the client wants to see availability for
                                user = client.recv(1024).upper()
                                # name of the user's availability file
                                fname2 = user + ".txt"
                                if os.path.isfile(fname2): # if file exists, open
                                        user_file2 = open(fname2, "r")
                                else: # if file does not exist, create new file
                                        user_file2 = open(fname2, "a+")
                                        # get today's date
                                        d = datetime.date.today()
                                        # write dates for the next two weeks into the new user's file
                                        for x in range(0, 14):
                                                next_date = d + datetime.timedelta(x)
                                                user_file2.write(str(next_date.month) + "-" + str(next_date.day) + "\n")                      
                                        # set pointer to beginning of the file
                                        user_file2.seek(0)

                                # store lines in the user file to file_content2 and close the file
                                file_content2 = user_file2.readlines()
                                user_file2.close()

                                # create string of dates for the next two weeks for client to choose from
                                choose_date = "Enter one of the following dates you would like to view the availability for:\n"
                                for date in nextTwoWeeks:
                                        if date==nextTwoWeeks[13]:
                                                choose_date += date
                                        else:
                                                choose_date += date + ", "
                                client.send(choose_date)
                                # get client's chosen date
                                day = client.recv(1024)
                                # call function a to send client the availability for the selected user
                                a(file_content2, day)
                        except:
                                #Send error message
                                client.send('Transaction failed.')
                                # close client socket
                                client.close()
                                # end current session and starts new loop
                                continue
                elif option=='D': # user selected menu option D to book a meeting
                        try:
                                # message stating what time slots are available
                                choose_date = "Please choose from one of the following dates:\n"

                                # append dates for the next two weeks available to be chosen
                                for date in nextTwoWeeks:
                                        if date==nextTwoWeeks[13]:
                                                choose_date += date
                                        else:
                                                choose_date += date + ", "

                                # send choose_date to client
                                client.send(choose_date)
                                # receive the chosen date
                                day = client.recv(1024).upper()
                                # call function to function to send all available slots for a user
                                a(file_content, day)

                                # get the time slot the client wants to book
                                book_slot = client.recv(1024)
                                # if the slot is available
                                if checkAvailableSlots(book_slot, file_content, day)==True:
                                        # get the index of the start of the date in the file
                                        index = nextTwoWeeks.index(day)
                                        insert_index = find_line(file_content, nextTwoWeeks[index])
                                        # inser the time slot into file_content
                                        file_content.insert(insert_index, book_slot+"\n")
                                # overwrite the user file with the new file_content with the inserted slot
                                user_file = open(fname, "w")
                                file_content = "".join(file_content)
                                user_file.write(file_content)
                                user_file.close()

                                # get the user's email from the user_email array
                                # same index as the user's name in the users array
                                email_index = users.index(name)
                                user_email = emails[email_index]
                                
                                # Open a plain text file for reading.
                                textfile = "textfile.txt"
                                fp = open(textfile, 'w')
                                # write confirmation into the email body
                                body = "You have successfully booked the time slot from " + book_slot + " on " + day + "."
                                fp.write(body)
                                fp.close()

                                fp = open(textfile, 'rb')
                                # Create a text/plain message
                                msg = MIMEText(fp.read())
                                fp.close()

                                # me == the sender's email address
                                # you == the recipient's email address
                                msg['Subject'] = 'Meeting Scheduler Confirmation'
                                msg['From'] = 'jeszeng@cs.stonybrook.edu'
                                msg['To'] = user_email

                                # Send the message via our own SMTP server, but don't include the
                                # envelope header.
                                s = smtplib.SMTP('edge1.cs.stonybrook.edu')
                                s.sendmail('jeszeng@cs.stonybrook.edu', user_email, msg.as_string())
                                s.quit()

                                # send the client acknowledgement that the time slot was successfully booked
                                acknowledgement = "\nYou have successfully booked the time slot " + book_slot + " on " + day + ". You will receive an email confirmation shortly.\n"
                                client.send(acknowledgement)

                                # update file_content to accommodate for the inserted time slot
                                user_file = open(fname, "r")
                                file_content = user_file.readlines()
                                user_file.close()
                        except:
                                #Send error message
                                client.send('Transaction failed.')
                                # close client socket
                                client.close()
                                # end current session and starts new loop
                                continue
                elif option=='E': # user selected menu option E
                        # get the list of attendees for the meeting
                        attendees = client.recv(1024).upper().split(', ')
                        # include the client's name in the list
                        attendees.append(name)

                        # ask client to choose a date within the next two weeks
                        choose_date = "Please choose from one of the following dates:\n"
                        for date in nextTwoWeeks:
                                if date==nextTwoWeeks[13]:
                                        choose_date += date
                                else:
                                        choose_date += date + ", "
                        client.send(choose_date)
                        # get chosen date from client and put into uppercase
                        day = client.recv(1024).upper()
                        # get time frame client wants to book
                        time_frame = client.recv(1024).split(' - ')

                        # separate the time frame into slots
                        # get the start and end hour
                        start_hour = time_frame[0].split(':')[0]
                        end_hour = time_frame[1].split(':')[0]

                        # if the first time is in xx:00 format, make the start time hh:00 - hh:30
                        if time_frame[0].split(':')[1]=='00':
                                start_time = time_frame[0] + " - " + start_hour + ":30"
                        else: # else, make the start time hh:30 - (hh+1):00
                                start_time = time_frame[0] + " - " + str(int(start_hour)+1) + ":00"

                        # do the same thing for the end time
                        if time_frame[1].split(':')[1]=='00':
                                end_time = time_frame[1] + " - " + end_hour + ":30"
                        else:
                                end_time = time_frame[1] + " - " + str(int(end_hour)+1) + ":00"

                        # based on the start and end times, split the time frame into slots and store in time_slots
                        time_slots = []

                        # put all time slots for a day into time slots
                        for hour in range(0, 24):
                                timeSlot = str(hour) + ":00 - " + str(hour) + ":30"
                                time_slots.append(timeSlot)

                                if hour==23:
                                        timeSlot2 = str(hour) + ":30 - " + str(0) + ":00"
                                        time_slots.append(timeSlot2)
                                else:
                                        timeSlot2= str(hour) + ":30 - " + str(hour+1) + ":00"
                                        time_slots.append(timeSlot2)

                        # find indices for the start and end times
                        start_index = time_slots.index(start_time)
                        end_index = time_slots.index(end_time) - start_index

                        # eliminate all time indices in time_slots that is before start_index and after end_index
                        time_slots = time_slots[start_index:]
                        time_slots = time_slots[:end_index]

                        # for each attendee, if even one person is not available for one time slot, can't book
                        timeSlotAvailable = True
                        for person in attendees:
                                if person_available(person, time_slots, day)==False:
                                        timeSlotAvailable = False
                                        break

                        # if the time frame is available for all attendees
                        if timeSlotAvailable:
                                # tell client that the time frame is available
                                acknowledgement = "OK"
                                client.send(acknowledgement)
                                # confirm if client wants to book the times
                                book_slots = client.recv(1024)
                                # if yes
                                if book_slots.upper()=="Y":
                                        # for each attendee
                                        for person in attendees:
                                                # open the attendee's file and get his/her file's content
                                                fname2 = person + ".txt"
                                                file2 = open(fname2, "r")
                                                file_content2 = file2.readlines()
                                                file2.close()

                                                # find the line for the meeting date
                                                index = nextTwoWeeks.index(day)
                                                insert_index = find_line(file_content2, nextTwoWeeks[index])
                                                # insert each slot of time frame into the file
                                                for slot in time_slots:
                                                        file_content2.insert(insert_index, slot+"\n")
                                                # overwrite file_content2 and update it to have the inserted time slots
                                                file2 = open(fname2, "w")
                                                file_content2 = "".join(file_content2)
                                                file2.write(file_content2)
                                                # close the attendee's file
                                                file2.close()   

                                                # get the attendee's email from emails array
                                                email_index = users.index(person)
                                                user_email = emails[email_index]

                                                # Open a plain text file for reading.
                                                textfile = "textfile.txt"
                                                fp = open(textfile, 'w')
                                                # put confirmation into email body with list of attendees
                                                body = "You have booked the time slot from " + " - ".join(time_frame) + " on " + day + ". The attendees in this meeting are:\n" + "\n".join(attendees)
                                                fp.write(body)
                                                # close the text file
                                                fp.close()

                                                fp = open(textfile, 'rb')
                                                # Create a text/plain message
                                                msg = MIMEText(fp.read())
                                                fp.close()

                                                # me == the sender's email address
                                                # you == the recipient's email address
                                                msg['Subject'] = 'Meeting Scheduler Confirmation'
                                                msg['From'] = 'jeszeng@cs.stonybrook.edu'
                                                msg['To'] = user_email

                                                # Send the message via SMTP server
                                                s = smtplib.SMTP('edge1.cs.stonybrook.edu')
                                                s.sendmail('jeszeng@cs.stonybrook.edu', user_email, msg.as_string())
                                                s.quit()

                                        # send client acknowledgement that email was sent and time slots books for all users
                                        acknowledgement = "\nYou have successfully booked the time slot " + " - ".join(time_frame) + " on " + day + ". All attendees will receive an email confirmation shortly.\n"
                                        client.send(acknowledgement)

                                        # open the client file and read updated lines into file_content
                                        user_file = open(fname, "r")
                                        file_content = user_file.readlines()
                                        # close client file
                                        user_file.close()
                        else: # not all attendees are available within the time frame; send acknowledgement
                                acknowledgement = "Unavailable"
                                client.send(acknowledgement)
                elif option=='F': # user selected menu option F to exit
                        acknowledgement = "Goodbye."
                        # send acknowledgement that session has ended
                        client.send(acknowledgement)
                        # close client socket
                        client.close()

	# close client connection socket
	client.close()
        	
#Close the input file
user_list.close()
