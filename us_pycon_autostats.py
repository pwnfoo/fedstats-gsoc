import os

def main():

	f = open('users.txt')
	lines = [line.rstrip('\n') for line in open('users.txt')]
	print lines

	for user in lines:
		os.system('python main.py -u ' + user + ' -s 05/28/2016 -e 06/05/2016 -m csv')
main()
