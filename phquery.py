#!/usr/bin/python
# 
# phquery.py 0.4

# Complete rewrite for 0.4, John N. Laliberte <allanonjl@gentoo.org>

#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc., 59
# Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

#
# Currently, this only returns the first match. Therefore, it really
# only makes sense when query is "alias=" -- so we die if that's not the
# case.
#

import socket
import string
import sys

QIPORT=105
DEBUG=False

class ResultCode:
	NO_MATCHES="501:No matches to your query."
	NUM_MATCHES=102
	DATA=-200
	NO_MORE_DATA="200:Ok."

	property(NO_MATCHES)
	property(NUM_MATCHES)
	property(DATA)
	property(NO_MORE_DATA)

class LineObject:
	
	def __init__(self, line):
		self.raw_string = ""
		self.result_code = ""
		self.result_index = ""
		self.category = ""
		self.data = ""
		self.category_and_data = {}
		
		line = line.replace('\n',"")
		line_parts = string.split(line,':')
		# we really only care about the case with 4 segments
		if len(line_parts) == 4:
			self.result_code = string.strip(line_parts[0])
			self.result_index = string.strip(line_parts[1])
			self.category = string.strip(line_parts[2])
			self.data = string.strip(line_parts[3])
		else:
			self.category = "unhandled_data"
			self.data = string.join(line_parts,":")

		self.category_and_data = {self.category:self.data}

class Person:
	
	def __init__(self,line):
		if DEBUG: print "Creating a new person"
		self.information = {}
		self.add_data(line)
		
	def add_data(self, line):
		self.information.update(line)
	
def query(host='',field='alias',value='',timeout=15.0):

	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	
	sock.settimeout(timeout)
	
	try:
		sock.connect((host,QIPORT))
		if DEBUG: print "Connected!"
	
		# let's treat the socket like a file, for easy access.
		sock_out = sock.makefile('wb',0)
		sock_in = sock.makefile('r',0)
		sock.close()  # we can do this because we've duplicated it
	
		# send the query, get all possible info back
		query = "query %s=%s\r return all" % (field, value)
		print >> sock_out, query
		if DEBUG: print "Sent query: "+ query
	
		people = []
		last_index = 0
		for line in sock_in:
			if DEBUG: print line
			
			line_object = LineObject(line)
			
			# figure out if this is the same person, or a different one
			if DEBUG: print line_object.result_index,last_index
			if(line_object.result_index != "" and \
			string.atoi(line_object.result_index) == last_index):
	
				# add to the current person
				person = people[last_index-1]
				if DEBUG: print "Appending to person" + str(person.information)
				if DEBUG: print "New data to append" + str(line_object.category_and_data)
				person.add_data(line_object.category_and_data)
				
			elif(line_object.result_index != ""):
				# create a new one
				if DEBUG: print "New data to append" + str(line_object.category_and_data)
				new_person = Person(line_object.category_and_data)
				people.append(new_person)
				last_index += 1
			
			if line_object.data == ResultCode.NO_MORE_DATA or \
			line_object.data == ResultCode.NO_MATCHES:
				print >> sock_out, "quit\r"
				sock_out.close()
				sock_in.close()
				if DEBUG: print "Disconnected"
				break
		
		if DEBUG:
			print "Complete Results: " + "\n"
			print str(people)
			for person in people:
				print person.information
		
		return people


	except socket.timeout:
		sock.close()
		raise Exception, "phquery: Socket Timed Out!"
	except:
		raise Exception, "phquery: %s " % sys.exc_info()[0]

if __name__=="__main__":
	DEBUG=True
	query('ns8.bu.edu','alias','testuser')
