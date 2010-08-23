import getopt, sys, re
from libstatuses import add_profile

usage = """Usage: profiles.py [OPTIONS]
	-h, --help - print this help message
	-f FILE_NAME, --file=FILE_NAME - file where each string
		represents pair 'e-mail: password'
	-e E-MAIL, --email=E-MAIL - vk.com account e-mail
	-p PASSWORD, --password=PASSWORD - vk.com account password"""


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:],'f:e:p:',['file=','email=','password='])
	except getopt.GetoptError:
		print usage
		sys.exit(2)
	if len(sys.argv) == 1:
		print usage
		sys.exit(0)
	filename,email,password = None,None,None
	for opt, val in opts:
		if opt in ['-f','--file']:
			filename = val
		elif opt in ['-e','--email']:
			email = val
		elif opt in ['-p','--password']:
			password = val
		elif opt in ['-h','--help']:
			print usage
			sys.exit(0)
	if password and email:
		if re.match(r'^[\w.]+@[\w.]+\.\w+$',email):
			if add_profile(email,password):
				print 'profile successfully added'
			else:
				print 'profile already exists'
		else:
			print 'invalid email'
	if filename:
		try:
			f = open(filename,'r')
		except IOError:
			print 'no such file'
			sys.exit(2)
		number = 0
		strings_count = 1
		while 1:
			string = f.readline()
			strings_count = strings_count + 1
			if re.search(r'^\s*$',string):
				if not string:
					break
				continue
			match = re.search(r'^(?P<email>[\w.]+@[\w.]+\.\w+):\s*(?P<password>.+)$',string)
			if not match:
				print 'wrong file format in ' + str(strings_count) + ' line'
				break
			else:
				if add_profile(match.group('email'),match.group('password')):
					number = number + 1
		print str(number) + ' profiles added'
			
	
	
	
if __name__ == '__main__':
	main()

