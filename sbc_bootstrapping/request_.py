import socket
import json
import threading
import time
import sbc

file = '.\\sbc_bootstrapping\\sources.json'
conns = []
crtable = {'open_blockchain': []}

def pull_request():
	with open(file,'r') as fl:
		table = json.load(fl)
	allowed_sources = []
	for ip in table['prev_sources']:
		connection = socket.socket()
		connection.settimeout(1)
		is_allowed = connection.connect_ex((ip,6007))
		if is_allowed == 0:
			allowed_sources.append(ip)
			break
	if len(table['prev_sources']) == 0:
		for el in table['base_source'].split("/"):
			connection = socket.socket()
			connection.settimeout(1)
			is_allowed = connection.connect_ex((el, 6007))
			if is_allowed == 0:
				allowed_sources.append(el)
	pipe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	pipe.settimeout(1)
	try:
		pipe.connect((allowed_sources[0],6007))
	except: return []
	for el in range(10):
		pipe.send('GET\n'.encode())
	req_data = None
	try:
		req_data = pipe.recv(512).decode()
	except:
		pass
	if req_data in [None, '']:
		while req_data in [None, '']:
			try:
				req_data = pipe.recv(512).decode()
			except:
				pass
	return eval(req_data.split('\n')[-2])

def push_request(state):
	local_ip = sbc.BlockChain().get_local_ip()
	with open(file,'r') as fl:
		table = json.load(fl)
	allowed_sources = []
	for ip in table['prev_sources']:
		connection = socket.socket()
		connection.settimeout(1)
		is_allowed = connection.connect_ex((ip,6007))
		if is_allowed == 0:
			allowed_sources.append(ip)
			break
	if len(table['prev_sources']) == 0:
		for el in table['base_source'].split("/"):
			connection = socket.socket()
			connection.settimeout(1)
			is_allowed = connection.connect_ex((el, 6007))
			if is_allowed == 0:
				allowed_sources.append(el)
	pipe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	pipe.settimeout(1)
	try:
		pipe.connect((allowed_sources[0],6007))
		for el in range(10):
			pipe.send(f'PUSH{local_ip}#{state}\n'.encode())
		req_data = None
		try:
			req_data = pipe.recv(512).decode()
		except:
			pass
		while req_data in [None, '']:
			try:
				req_data = pipe.recv(512).decode()
				break
			except:
				pass

		return req_data.split('\n')[-2]
	except: print('no source was provided please try later')

def process_commands():
	global crtable,conns
	while True:
		recvs = []
		for conn in conns:
			conn.setblocking(False)
			try:
				recvs.append([conn.recv(512).decode(),
				              conn])
			except Exception as err:
				# print(err)
				pass
		for el in recvs:
			data = el[0]
			conn = el[1]
			# print(data.encode(),data.split('\n')[0].encode())
			data = data.split('\n')[0]
			if data == 'GET':
				for el1 in range(3):
					try:
						conn.send(f'{crtable}\n'.encode())
					except:
						conns.remove(conn)
			if 'PUSH' in data:
				ip = data[4:data.find('#')]
				try:
					ipns = list(map(lambda item:int(item),ip.split('.')))
					invalid = 0
					for el in ipns:
						if el > 255 or el < 0:
							invalid+=1
					if invalid >= 1:
						raise SyntaxError
					state = int(data[-1])
					if state == 0:
						crtable['open_blockchain'].remove(ip)
					else:
						crtable['open_blockchain'].append(ip)
					crtable['open_blockchain'] = [*set(crtable['open_blockchain'])]
					conn.send(f'200\n'.encode())
				except:
					conn.send(f'400\n'.encode())

def open_source(table = None):
	if table == None:
		table = set()
	else:
		table: set
	global conns
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serv.bind(('0.0.0.0',6007))
	serv.setblocking(False)
	serv.listen()
	threading.Thread(target=process_commands).start()
	while True:
		try:
			conn, addr = serv.accept()
			conns.append(conn)
		except:
			pass