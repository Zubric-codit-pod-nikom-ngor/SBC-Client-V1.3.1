import logging
import os

poo_poo_on_a_stick = "\\"
filepath1 = fr'{__file__[::-1][__file__[::-1].find(poo_poo_on_a_stick):][::-1]}_internal'
if os.access(filepath1, os.R_OK) == True:
    if os.access(filepath1, os.W_OK) == True:
        if os.access(filepath1, os.F_OK) == True:
            pass
        else:
            exit()
    else: exit()

def get(filename):
	this_file = os.path.abspath(__file__)
	this_dir = os.path.dirname(this_file)
	wanted_file = os.path.join(this_dir, filename)
	return wanted_file

logger = logging.getLogger(__name__)
with open(get('logs\counter'), 'r') as file:
	name = file.read()
with open(get('logs\counter'), 'w') as file:
	file.write(str(int(name)+1))
logging.basicConfig(filename=get(f'logs\session{name}.log'),level=logging.INFO)

def printl(*items):
	string = ''
	for item in items:
		string+=str(item)
		string+=' '
	string = string[:-1]
	logger.info(string)
	print(*items)

def reset_logs():
	with open(get('logs\counter'), 'w') as file:
		file.write('1')
	for el in os.listdir(get('logs')):
		try:
			if el != 'counter':
				os.remove(get(f'logs\{el}'))
		except:
			pass