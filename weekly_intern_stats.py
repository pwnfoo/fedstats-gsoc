import os


def main():
	fp = open('interns.txt')
	interns = [user.strip('\n') for user in open('interns.txt')]
	print interns

	for intern in interns:
		if not os.path.exists(intern):
			os.makedirs(intern)
		# CSV MAIN FILE 
		os.system('python main.py -u %s -s 05/23/2016 -e 06/21/2016 -m csv -o stats_main' %(
                                intern))
		# Category-wise and Pagure
		os.system('python main.py -u %s -s 05/23/2016 -e 06/21/2016 -m svg -o %s/%s -c pagure' %(
				intern, intern, intern))
		# Markdown Report
		os.system('python main.py -u %s -s 05/23/2016 -e 06/21/2016 -m markdown -o %s/README.md' %(
                                intern, intern))
		# User Specific
		if intern == 'dhanvi':
			os.system('python main.py -u %s -s 05/23/2016 -e 06/21/2016 -m svg -o %s/%s -c copr' %(
                                intern, intern, intern))

if __name__ == '__main__':
	main()
