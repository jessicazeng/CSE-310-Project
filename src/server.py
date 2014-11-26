__author__ = 'Jessica'

# http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python

from socket import *
from string import rstrip
import os
import datetime

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

def checkAvailableSlots(timeSlot, file, day):
        #indexinDOW = daysOfWeek.index(day)
        indexinNTW = nextTwoWeeks.index(day)
        start_line = 0
        end_line = 0
        
        #for num, line in enumerate(file, 1):
        #        if day==line.rstrip():
        #                start_day = num
        #                break
        #        
        #for num, line in enumerate(file, 1):
        #        if daysOfWeek[indexinDOW+1]==line.rstrip():
        #                end_day = num
        #                break

        for num, line in enumerate(file, 1):
                if day==line.rstrip():
                        start_line = num
                        break
        for num, line in enumerate(file, 1):
                if nextTwoWeeks[indexinNTW+1]==line.rstrip():
                        end_line = num
                        break
        
        available = True
        for x in range(start_line, end_line):
                if timeSlot==file[x].rstrip():
                        available=False
                        break
        return available

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

        for x in range(0, 14):
                next_date = datetime.date.today() + datetime.timedelta(x)
                nextTwoWeeks.append(str(next_date.month) + "-" + str(next_date.day))                    

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

        def b(user_file):
                print "You chose B"

        def c(user_file):
                print "You chose C"
                
        def d(user_file):
                print "You chose D"

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
                client.close()
                continue
        else:
                print "invalid option"
                client.close()
                continue
        
	# close client connection socket
        user_list.close()
	client.close()
        	
#Close client connection socket
client.close()
