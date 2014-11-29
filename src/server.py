__author__ = 'Jessica'

# http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python

from socket import *
from string import rstrip
import os
import datetime
import re

#Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)

#bind socket to local port number 6190
serverSocket.bind(('', 6190))

#server listens for incoming TCP connection requests - max number of queued
#clients - 1
serverSocket.listen(1)

user_list = open('input.txt', 'r')

users = []
emails = []

for line in user_list:
        line_array = line.rstrip().split(' ')
        users.append(line_array[0].upper())
        emails.append(line_array[1])

print users
print emails

#daysOfWeek = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
nextTwoWeeks = []
for x in range(0, 14):
        next_date = datetime.date.today() + datetime.timedelta(x)
        nextTwoWeeks.append(str(next_date.month) + "-" + str(next_date.day))            

def find_line(file_content, line):
        line_number = -1
        for num, l in enumerate(file_content, 1):
                if line==l.rstrip():
                        line_number = num
                        break
        return line_number

def checkAvailableSlots(timeSlot, file, day):
        #indexinDOW = daysOfWeek.index(day)
        indexinNTW = nextTwoWeeks.index(day)
        start_line = find_line(file, day)
        end_line = find_line(file, nextTwoWeeks[indexinNTW+1])
        
        #for num, line in enumerate(file, 1):
        #        if day==line.rstrip():
        #                start_day = num
        #                break
        #        
        #for num, line in enumerate(file, 1):
        #        if daysOfWeek[indexinDOW+1]==line.rstrip():
        #                end_day = num
        #                break

        #for num, line in enumerate(file, 1):
        #        if day==line.rstrip():
        #                start_line = num
        #                break
        #for num, line in enumerate(file, 1):
        #        if nextTwoWeeks[indexinNTW+1]==line.rstrip():
        #                end_line = num
        #                break
        
        available = True
        for x in range(start_line, end_line):
                if timeSlot==file[x].rstrip():
                        available=False
                        break
        return available

def insertSlot(timeSlot, file, day):
        #indexinDOW = daysOfWeek.index(day)
        indexinNTW = nextTwoWeeks.index(day)
        start_line = 0
        end_line = 0

while True:
	# creates client socket in server and
	client, address = serverSocket.accept()

	try:
		# get client name
		name = client.recv(1024).upper()
		print name
	except:
		#Send error message
        	client.send('User not found.')
        	client.close()
        	continue

        person_found = False;
		
	# check if name is in user_list
	if any(name in s for s in users):
                person_found = True;

        print person_found

        # if person is on user list server responds to client with acknowledgement
        if (person_found == True):
                response = "Hello, " + name
        else:
                response = "User not found."

        # send response whether the person was found or not
        client.send(response)

        if (person_found == False):
                client.close()
                continue

        # name of the user's availability file
        fname = name + ".txt"

        if os.path.isfile(fname): # if file exists, open
                user_file = open(fname, "a+")
        else: # if file does not exist, create new file
                user_file = open(fname, "a+")
                #user_file.write("MONDAY\nTUESDAY\nWEDNESDAY\nTHURSDAY\nFRIDAY\nSATURDAY\nSUNDAY\n")
                d = datetime.date.today()
                for x in range(0, 14):
                        next_date = d + datetime.timedelta(x)
                        user_file.write(str(next_date.month) + "-" + str(next_date.day) + "\n")                      
                user_file.seek(0)
                
        file_content = user_file.readlines()

        for y in nextTwoWeeks:
                if find_line(file_content, y)==-1:
                        user_file.write(y + "\n")

        user_file.close()

        user_file = open(fname, "r")

        file_content = user_file.readlines()
        
        user_file.close()

        start_index = find_line(file_content, nextTwoWeeks[0])

        if start_index!=1:
                user_file = open(fname, "w")
                for x, line in enumerate(file_content, 1):
                        if x not in range(0, start_index):
                                user_file.write(line)
                user_file.close()
        
        try:
		# get menu option chosen by user
		option = client.recv(1024).upper()
	except:
		#Send error message
        	client.send('Transaction failed.')
        	client.close()
        	continue

        # function to view all available slots for a user
        def a(file_content, day):
                #d = datetime.date.today()
                #print str(d.month) + "-" + str(d.day)
                print day
                availability = ""
                for hour in range(0, 24):
                        timeSlot = str(hour) + ":00 - " + str(hour) + ":30"
                        available_time = checkAvailableSlots(timeSlot, file_content, day)
                        if available_time==True:
                                availability = availability + timeSlot + "\n"

                        if hour==23:
                                timeSlot2 = str(hour) + ":30 - " + str(0) + ":00"
                                available_time = checkAvailableSlots(timeSlot2, file_content, day)
                                if available_time==True:
                                        availability = availability + timeSlot2 + "\n"
                        else:
                                timeSlot2= str(hour) + ":30 - " + str(hour+1) + ":00"
                                available_time = checkAvailableSlots(timeSlot2, file_content, day)
                                if available_time==True:
                                        availability = availability + timeSlot2 + "\n"

                client.send(availability)

        def d(user_file):
                print "You chose D"

        def e(user_file):
                print "You chose E"

        if option=='A':
                try:
                        choose_date = "Please choose from one of the following dates:\n"
                        for date in nextTwoWeeks:
                                if date==nextTwoWeeks[13]:
                                        choose_date += date
                                else:
                                        choose_date += date + ", "
                        client.send(choose_date)
                        day = client.recv(1024).upper()
                        a(file_content, day)
                except:
                        #Send error message
                        client.send('Transaction failed.')
                        client.close()
                        continue
        elif option=='B':
                try:
                        choose_date = "Please choose from one of the following dates you would like to delete a time slot from:\n"
                        for date in nextTwoWeeks:
                                if date==nextTwoWeeks[13]:
                                        choose_date += date
                                else:
                                        choose_date += date + ", "
                        client.send(choose_date)
                        day = client.recv(1024)
                        user_file = open(fname, "w")
                        #b(user_file, day)
                        
                        print day
                        availability = ""
                        for hour in range(0, 24):
                                timeSlot = str(hour) + ":00 - " + str(hour) + ":30"
                                available_time = checkAvailableSlots(timeSlot, file_content, day)
                                if available_time==False:
                                        availability = availability + timeSlot + "\n"

                                if hour==23:
                                        timeSlot2 = str(hour) + ":30 - " + str(0) + ":00"
                                        available_time = checkAvailableSlots(timeSlot2, file_content, day)
                                        if available_time==False:
                                                availability = availability + timeSlot2 + "\n"
                                else:
                                        timeSlot2= str(hour) + ":30 - " + str(hour+1) + ":00"
                                        available_time = checkAvailableSlots(timeSlot2, file_content, day)
                                        if available_time==False:
                                                availability = availability + timeSlot2 + "\n"
                        if availability=="":
                                availability = "All slots open"
                        client.send(availability)

                        delete_slot = client.recv(1024)
                        for line in file_content:
                                if line.rstrip()!=delete_slot.rstrip():
                                        user_file.write(line)
                                        
                        user_file.close()
                        acknowledgement = "The time slot " + delete_slot + " has been successfully deleted, and and is currently available to be booked."
                        client.send(acknowledgement)
                except:
                        #Send error message
                        client.send('Transaction failed.')
                        client.close()
                        continue
        elif option=='C':
                try:
                        user = client.recv(1024).upper()
                        # name of the user's availability file
                        fname = user + ".txt"
                        if os.path.isfile(fname): # if file exists, open
                                user_file2 = open(fname, "r")
                        else: # if file does not exist, create new file
                                user_file2 = open(fname, "a+")
                                d = datetime.date.today()
                                for x in range(0, 14):
                                        next_date = d + datetime.timedelta(x)
                                        user_file2.write(str(next_date.month) + "-" + str(next_date.day) + "\n")                      
                                user_file2.seek(0)

                        file_content2 = user_file2.readlines()
                        user_file2.close()

                        choose_date = "Please choose from one of the following dates you would like to delete a time slot from:\n"
                        for date in nextTwoWeeks:
                                if date==nextTwoWeeks[13]:
                                        choose_date += date
                                else:
                                        choose_date += date + ", "
                        client.send(choose_date)
                        day = client.recv(1024)
                        a(file_content2, day)
                except:
                        #Send error message
                        client.send('Transaction failed.')
                        client.close()
                        continue
        elif option=='D':
                try:
                        choose_date = "Please choose from one of the following dates:\n"
                        for date in nextTwoWeeks:
                                if date==nextTwoWeeks[13]:
                                        choose_date += date
                                else:
                                        choose_date += date + ", "
                        client.send(choose_date)
                        day = client.recv(1024).upper()
                        a(file_content, day)

                        book_slot = client.recv(1024)
                        if checkAvailableSlots(book_slot, file_content, day)==True:
                                index = nextTwoWeeks.index(day)
                                insert_index = find_line(file_content, nextTwoWeeks[index])
                                file_content.insert(insert_index, book_slot+"\n")
                        user_file = open(fname, "w")
                        file_content = "".join(file_content)
                        user_file.write(file_content)
                        user_file.close()
                        
                        acknowledgement = "You have successfully booked the time slot " + book_slot + " on " + day + "."
                        client.send(acknowledgement)
                except:
                        #Send error message
                        client.send('Transaction failed.')
                        client.close()
                        continue
        elif option=='E':
                e(name)
        elif option=='F':
                client.close()
                continue
        else:
                print "invalid option"
                client.close()
                continue
        
	# close client connection socket
	client.close()
        	
#Close client connection socket
user_list.close()
client.close()
