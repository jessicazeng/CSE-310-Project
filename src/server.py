__author__ = 'Jessica'

# http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python

from socket import *
from string import rstrip
import os

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

daysOfWeek = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

def checkAvailableSlots(timeSlot, file, day):
        indexinDOW = daysOfWeek.index(day)
        start_day = 0
        end_day = 0
        
        for num, line in enumerate(file, 1):
                if day==line.rstrip():
                        start_day = num
                        break
                
        for num, line in enumerate(file, 1):
                if daysOfWeek[indexinDOW+1]==line.rstrip():
                        end_day = num
                        break

        print str(start_day) + " " + str(end_day)
        
        found = True
        for line in file:
                if timeSlot==line.rstrip():
                        found = False
                        break
        return found

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
                user_file.write("MONDAY\nTUESDAY\nWEDNESDAY\nTHURSDAY\nFRIDAY\nSATURDAY\nSUNDAY\n")
                user_file.seek(0)

        file_content = user_file.readlines()
        try:
		# get menu option chosen by user
		option = client.recv(1024).upper()
	except:
		#Send error message
        	client.send('Transaction failed.')
        	client.close()
        	continue

        # function to view all available slots for a user, given their name
        def a(file_content, day):
                print day
                for hour in range(0, 24):
                        timeSlot = str(hour) + ":00 - " + str(hour) + ":30"
                        available_time = checkAvailableSlots(timeSlot, file_content, day)
                        if available_time==True:
                                print timeSlot

        def b(user_file):
                print "You chose B"

        def c(user_file):
                print "You chose C"
                
        def d(user_file):
                print "You chose D"
                
        def e(user_file):
                print "You chose E"

        if option=='A':
                try:
                        day = client.recv(1024).upper()
                except:
                        #Send error message
                        client.send('Transaction failed.')
                        client.close()
                        continue
        
                a(file_content, day)
        elif option=='B':
                b(name)
        elif option=='C':
                c(name)
        elif option=='D':
                d(name)
        elif option=='E':
                e(name)
        else:
                print "invalid option"
                client.close()
                continue
        
	# close client connection socket
        user_list.close()
	client.close()
        	
#Close client connection socket
client.close()
