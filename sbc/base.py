#!/usr/bin/env python
# -*- coding: utf8 -*-

# Мы живём в жестоком мире...

import copy
import datetime
import json
import ast
import sys
import re
import random
import time
import socket
import threading
import stun
import chardet
import sbc
import base64
from sbc.operation_logger import *
import sbc.hasher.aes256 as aes
from sbc.essential_files.essentials import Chain, initial_data
from sbc.essential_files.essentials import Block
from sbc.essential_files.essentials import compress,decompress
from sbc.essential_files.string_mergers import combine_strings, much_harder_changes, get_changes
from sbc.encoding_problem.deep_encoding import decode_by_conversion
from sbc.encoding_problem.deep_encoding import encode_by_conversion
import sbc.essential_files.string_mergers as string_mergers


# sys.stdin.reconfigure(encoding='windows-1251')
# sys.stdout.reconfigure(encoding='windows-1251')


genstart = False


password = aes.create_password()
plain_order = list(range(8))
directed_file_data = {}
directed_file = {}
filenames = {}
past_conts = {}
assigned_base = {}

CREATE_BLOCKS_AUTOMATICALLY = False


def decode_with_chardet(item):
	codec = chardet.detect_all(item,True)
	print(codec)
	return item.decode('latin-1')

def update_assigned():
	global assigned_base,CREATE_BLOCKS_AUTOMATICALLY
	while True:
		with open('settings.stng', 'r') as stngs:
			settings = json.loads(stngs.read())
			assigned_base = settings['assigned']
			CREATE_BLOCKS_AUTOMATICALLY = settings['automatic']
		time.sleep(2)
		# print('assigned:',assigned_base)


def dynamic_read():
	global directed_file_data
	global directed_file
	try:
		for el in filenames:
			true_nmn = el
			try:
				filepath = assigned_base[filenames[el]]
				filename = filenames[el]
				while '/' in filepath:
					filepath = filepath.replace('/', '\\')
				file_path = filepath + '\\' + filename[::-1][:filename[::-1].find("/")][::-1]
			except KeyError:
				file_path = el
			with open(file_path, 'rb') as file:
				directed_file[true_nmn] = file
				directed_file_data[true_nmn] = file.read().decode()
	except Exception as err:
		print(err)
	time.sleep(2)
	while True:
		while CREATE_BLOCKS_AUTOMATICALLY == 1:
			try:
				for el in filenames:
					true_nmn = el
					try:
						filepath = assigned_base[filenames[el]]
						filename = filenames[el]
						while '/' in filepath:
							filepath = filepath.replace('/','\\')
						file_path = filepath+'\\'+filename[::-1][:filename[::-1].find("/")][::-1]
					except KeyError:
						file_path = el
					with open(file_path,'rb') as file:
						directed_file[true_nmn] = file
						directed_file_data[true_nmn] = file.read().decode()
			except Exception as err:
				print(err)
			time.sleep(1.25)
		time.sleep(5)


def load_dict_with_bytes(s):
	bytes_pattern = re.compile(r"b(['\"])(.*?)(?<!\\)\1", re.DOTALL)
	replacements = {}
	def replace(match):
		key = f"__BYTES_{len(replacements)}__"
		quote = match.group(1)
		content = match.group(2)
		replacements[key] = f"b{quote}{content}{quote}"
		return f"'{key}'"
	processed_str = bytes_pattern.sub(replace, s)
	parsed = ast.literal_eval(processed_str)
	def restore(obj):
		if isinstance(obj, dict):
			return {k: restore(v) for k, v in obj.items()}
		if isinstance(obj, str) and obj.startswith('__BYTES_'):
			return ast.literal_eval(replacements[obj])
		return obj

	return restore(parsed)


class BlockChainProtocol:
	CREATE =       'CREATE===='
	CONNECT =      'CONNECT==='
	DELETE =       'DELETE===='
	DISCONNECT =   'DISCONNECT'
	RECONNECT =    'RECONNECT='
	GENERALSTART = 'GENSTART=='
	DATAPACK =     'DATAPACK=='
	REMEMBER =     'REMEMBER=='
	FEEDBACK =     'FEEDBACK=='
	FILEPRESET =   'FILEPRESET'
	REVIVE =       'REVIVE===='
	SETTING =      'SETTING==='
	DIVIDER =      '$!/'


class BlockChain:

	def __init__(self):
		nstun = stun.get_ip_info()
		self.external_ip = nstun[1]
		self.blocks = []
		self.server = None
		self.running = True
		self.connection_established = False
		self.port = 15009
		self.lock = threading.Lock()
		self.connections = []
		self.addresses = []
		self.prev_file_data = {}
		self.sharing_files = ['blockchain_data/test1.txt',
		                      'blockchain_data/test2.txt']
		self.joined = True
		self.chain_server = None
		self.chain_server: socket.socket
		self.password = password
		self.chain = Chain()
		printl(self.external_ip)
		self.block_buffer = []
		self.servers = []
		self.nodes = []
		self.__instructions = []
		self.instructions = []
		self.__presets = {}
		self.pres_f = []
		self.__buffer_size = 262144*1024

	def __is_alive(self, sock):
		try:
			sock.settimeout(0.5)
			data = sock.recv(1, socket.MSG_PEEK)
			if data:
				return True
			if data == b'':
				return False
			return True
		except socket.timeout:
			return True
		except (ConnectionResetError, ConnectionAbortedError,
				BrokenPipeError, ConnectionRefusedError):
			return False
		except OSError as e:
			if e.errno in (9, 10038, 10057, 10053, 10054):
				return False
			return True
		except Exception:
			return False

	def get_local_ip(self):
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
				s.connect(("8.8.8.8", 80))
				return s.getsockname()[0]
		except Exception:
			return self.external_ip

	def __check_members(self):
		for i, el in enumerate(self.connections):
			el: socket.socket
			alive = self.__is_alive(el)
			# print(f'member {el} alive? {alive}')
			if alive != True:
				self.connections.pop(i)
				self.addresses.pop(i)
				if el in self.servers:
					self.servers.remove(el)
				self.nodes = []
				for el in self.addresses:
					self.nodes.append(self.Node())
					self.nodes[-1].ip = el[0]
				self.update_nodes()
				self.redirect()

	def __checking_cycle(self):
		while self.running == True:
			self.__check_members()
			time.sleep(3)

	def create(self):
		local_ip = self.get_local_ip()
		printl(f"Локальный IP: {local_ip}")
		local_ip = '0.0.0.0'
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server.bind((local_ip, self.port))
			self.server.setblocking(False)
			self.server.listen()
			self.server.settimeout(1)

			printl(f"Сервер запущен на {local_ip}:{self.port}")

			threading.Thread(target=self.__checking_cycle, daemon=True).start()
			for file in self.sharing_files:
				filenames[get(file)] = file
			threading.Thread(target=dynamic_read,daemon=True).start()
			# threading.Thread(target=update_assigned, daemon=True).start()

			while self.running:
				try:
					client, address = self.server.accept()
					self.connections.append(client)
					self.addresses.append(address)
					time.sleep(1.5)  # Уменьшаем задержку с 5 до 0.5 секунд
					print('testing members')
					self.__check_members()
					print(self.connections)
					print(self.addresses)
					if len(self.addresses) == 0:
						raise IndexError
					ip = self.addresses[-1][0]
					printl(f'подключение от {ip}')
					self.nodes = []
					for el in self.addresses:
						self.nodes.append(self.Node())
						self.nodes[-1].ip = el[0]
						print(self.nodes[-1])
					self.nodes = self.update_nodes()
					print(f'nodes: {self.nodes}')
					printl('====================================')
					for el in self.nodes[::-1]:
						printl(f'промпт от: {el.ip}')
						printl(f'сзади на цепи: {el.connected_prev}')
						printl(f'спереди на цепи: {el.connected_aftr}')
					printl('Переадресация портов...')
					self.redirect()
					time.sleep(0.5)  # Уменьшаем задержку с 3 до 0.5 секунд
				except socket.timeout:
					continue
				except IndexError:
					continue
		finally:
			self.stop_server()

	def update_nodes(self):
		count = 0
		for el in self.nodes:
			last_ip = self.nodes[count - 1].ip
			self.nodes[count].connected_prev = last_ip
			self.nodes[count - 1].connected_aftr = self.nodes[count].ip
			count += 1
		# self.nodes[0].connected_prev = self.nodes[0].connected_aftr
		# self.nodes[0].connected_prev = self.nodes[0].connected_aftr
		return self.nodes

	def stop_server(self):
		if hasattr(self, 'server') and self.server:
			self.server.close()
		self.running = False
		printl("Сервер остановлен")

	def redirect(self):
		def redir(nc, el):
			c = nc
			block = self.nodes[c]
			printl(el, c, 'completed')
			try:
				self.__send(el, f'{BlockChainProtocol.FEEDBACK}server\n'.encode())
				feedback = self.__listen_command(el).decode()
				print('feedback:', feedback)
				time.sleep(1)
				if block.ip in self.servers:
					self.__send(el, f'{BlockChainProtocol.DISCONNECT}\n'.encode())
					self.__send(el, f'{BlockChainProtocol.DELETE}\n'.encode())
					time.sleep(1)
					self.__send(el, f'{BlockChainProtocol.CREATE}{block.ip}\n'.encode())
					time.sleep(5)
				self.__send(el, f'{BlockChainProtocol.DATAPACK}global password\n'.encode())
				self.__send(el, f'{BlockChainProtocol.DATAPACK}self.password={password.encode()}\n'.encode())
				self.__send(el, f'{BlockChainProtocol.DATAPACK}self.password=self.password.decode()\n'.encode())
				self.__send(el, f'{BlockChainProtocol.DATAPACK}print(self.password)\n'.encode())
				self.servers.append(block.ip)
				if feedback == '0':
					raise Exception
			except:
				self.__send(el, f'{BlockChainProtocol.CREATE}{block.ip}\n'.encode())
				self.__send(el, f'{BlockChainProtocol.REMEMBER}{self.get_local_ip()}\n'.encode())
				for filename in filenames:
					inst = f'{BlockChainProtocol.FILEPRESET}{filenames[filename]}{BlockChainProtocol.DIVIDER}{directed_file_data[filename]}\n'
					self.__send(el, f'{BlockChainProtocol.FILEPRESET}{len(inst)}\n'.encode())
					time.sleep(0.3)
					self.__send(el, inst.encode())
			self.__send(el, f'{BlockChainProtocol.RECONNECT}{self.nodes[c].connected_aftr}\n'.encode())
			for file in self.sharing_files:
				self.__send(el, f'{BlockChainProtocol.GENERALSTART}{file}\n'.encode())
			if nc != len(self.connections) - 1:
				self.__send(el, f'{BlockChainProtocol.REVIVE}\n'.encode())

		for nc, el in enumerate(self.connections):
			threading.Thread(target=redir,args=(nc,el,),daemon=True).start()
			time.sleep(0.1)

	def join(self, ip):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(1)
		try:
			sock.connect((ip, self.port))
		except:
			print('left with error')
			return None

		self.client_sock = sock
		def loop():
			threading.Thread(target=update_assigned,daemon=True).start()
			while self.joined == True:
				try:
					answ = None
					# sock.settimeout(1)  # Устанавливаем таймаут для неблокирующего чтения
					try:
						answ = self.__custom_buffer_listen(sock, self.__buffer_size)
					except socket.timeout:
						# time.sleep(0.1)  # Небольшая задержка при отсутствии данных
						continue
					except Exception:
						# time.sleep(0.5)  # Задержка при ошибке соединения
						continue
					if answ:
						answ = answ.decode()
						mcoms = answ.split('\n')[:-1]
						printl("получены новые инструкции:")
						printl(mcoms)
						for command in mcoms:
							printl(f'Получена инструкция: {command}')
							printl('Разбор инструкции...')
							function = command[:10]
							related = command[10:]
							printl(f'Функция: {function}')
							printl(f'Аргумент: {related}')
							threading.Thread(target=self.__execute_instruction,daemon=True,args=(function,related,)).start()
							time.sleep(0.25)
				except Exception as e:
					printl(f"Ошибка в loop: {e}")
					# time.sleep(1)  # Задержка при ошибке
			sock.shutdown(socket.SHUT_RDWR)
			sock.close()
			print(sock)
			print('socket closed')
		loop()

	def __listen_command(self, conn):
		current_timeout = conn.gettimeout()
		if current_timeout is None:
			conn.settimeout(1)
		try:
			return conn.recv(262144*1024)
		except socket.timeout:
			raise
		except Exception as e:
			raise

	def __custom_buffer_listen(self, conn, buffsize=262144*1024):
		current_timeout = conn.gettimeout()
		if current_timeout is None:
			conn.settimeout(1)
		try:
			return conn.recv(buffsize)
		except socket.timeout:
			raise
		except Exception as e:
			raise

	def conn_myself(self):
		self.join(self.get_local_ip())

	def __accept(self):
		self.conn_data = []
		while True:
			try:
				self.dummy_accconn, self.dummy_accaddr = self.chain_server.accept()
				self.conn_data.append(self.dummy_accconn)
				self.accconn = self.conn_data[-1]
				print('conn accepted')
				print(self.accaddr)
				self.connection_established = True
				# self.chain_client = self.accconn
			except:
				pass

	def general_start(self):
		printl("итерация GENSTART==")
		global genstart
		genstart = True
		raw = ''
		while True:
			# while True:
			# 	try:
			# 		self.chain_client = self.conn_data[-1]
			# 		break
			# 	except:
			# 		pass
			while '\n' not in raw:
				try:
					raw = raw+self.__custom_buffer_listen(self.accconn,4096).decode()
				except:
					pass
			spliter = raw.split('\n')
			if spliter[-1] == '':
				spliter = spliter[:-1]
			print(f'raw len: {len(raw)} | len of chains: {len(spliter)}')
			chains = []
			for got_data in spliter:
				try:
					processed = aes.decrypt(load_dict_with_bytes(got_data), self.password)
					print(raw)
					raw = ''
				except:
					raw = raw[::-1][:raw[::-1].find('\n')][::-1]
					print(raw)
					break
				# processed = eval(f'str({processed[1:]})')
				try:
					print('prc', type(processed),processed)
					processed = eval(processed)
					print('prc', type(processed), processed)
					processed = base64.b64decode(decode_by_conversion(processed).encode('ascii'))
					print('prc', type(processed), processed)
					# item = sbc.encoding_problem.deep_encoding.deep_encoding(decode_by_conversion(processed.encode()))
					chain = Chain().import_(processed)
				except Exception as err:
					print(err)
					processed = eval(processed)
					chain = Chain().import_(base64.b64decode(processed.encode('ascii')))
				chains.append(chain)
			for chain in chains:
				verified = self.chain.verify(chain)
				if verified == True:
					self.chain = chain.copy()
					if self.external_ip not in self.chain.fetched_by:
						self.chain.fetched_by.append(self.get_local_ip())
						sndd = encode_by_conversion(base64.b64encode(self.chain.export_()).decode('ascii'))
						sndd = aes.encrypt(sndd, self.password)
						sndd = str(sndd) + '\n'
						for el in range(len(sndd) // 1024 + 1):
							self.__send(self.chain_client,
										sndd[el * 1024:(el + 1) * 1024].encode())
					else:
						self.chain.fetched_by = [self.get_local_ip()]
			try:
				ver = self.chain.fetch_current()
			except: print('not enough blocks')

	def __fill_buffer(self):
		def cpt(full_path):
			dir_path = os.path.dirname(full_path)
			file_name = os.path.basename(full_path)
			dir_name = os.path.basename(dir_path) if dir_path else ""
			return dir_name + '/' + file_name
		time.sleep(5)
		self.prev_file_data = directed_file_data.copy()
		time.sleep(1)
		while True:
			try:
				for file in directed_file_data:
					changes_ = much_harder_changes(self.prev_file_data[file],
					                      directed_file_data[file])
					if changes_ == []:
						pass
					else:
						for change in changes_:
							new_block = Block()
							new_block.data = f'0{BlockChainProtocol.DIVIDER}{change}{BlockChainProtocol.DIVIDER}{cpt(filenames[file])}'
							new_block.sender = max(self.external_ip,self.get_local_ip())
							self.block_buffer.append(new_block)
							print(f'blocks in queue: {len(self.block_buffer)}')
					self.prev_file_data[file] = directed_file_data[file]
				time.sleep(3)
			except RuntimeError:
				pass
			except KeyError as err:
				for el in directed_file_data:
					self.prev_file_data[el] = directed_file_data[el]
			except IndexError as err:
				for el in directed_file_data:
					self.prev_file_data[el] = directed_file_data[el]

	def __flush_buffer(self):
		time.sleep(3)
		self.block_buffer = []
		while True:
			if len(self.block_buffer) >= 1:
				block = self.block_buffer[-1]
				block: Block

				print(block)

				prvc = self.chain.copy()
				self.chain.add_block(block)
				if prvc.blocks == self.chain.blocks:
					pass
				else:
					sndd = encode_by_conversion(base64.b64encode(self.chain.export_()).decode('ascii'))
					sndd = aes.encrypt(sndd, self.password)
					sndd = str(sndd)+'\n'
					for el in range(len(sndd)//1024+1):
						self.__send(self.chain_client,
									sndd[el*1024:(el+1)*1024].encode())
				self.block_buffer.pop(-1)
			else:
				time.sleep(1)  # Задержка когда буфер пуст, чтобы не нагружать CPU

	def __execute_instruction(self, instruction, obj):
		global genstart,password
		printl('=====ИНСТРУКЦИЯ=====')
		while '=' in instruction:
			instruction = instruction[:-1]
		instruction = instruction.lower()
		self.instructions.append(instruction)
		self.__instructions.append([instruction, obj])
		if instruction == 'create':
			self.chain_server = self.__open_server('0.0.0.0', 5)
			threading.Thread(target=
			                 self.__accept).start()
			printl('Открыт сервер')
			self.chain_server.setblocking(False)
		elif instruction == 'feedback':
			if obj == 'server':
				try:
					self.chain_server.type
					self.__send(self.client_sock, '1'.encode())
				except:
					self.__send(self.client_sock, '0'.encode())
			elif obj == 'genstart':
				if self.connection_established == False:
					fdd = '1'
				else:
					if self.connection_established == True:
						fdd = '0'
					else:
						fdd = '1'
				self.__send(self.client_sock, fdd.encode())
		elif instruction == 'disconnect':
			self.chain_client.close()
			printl('Server was shutdown')
		elif instruction == 'delete':
			self.chain_server.close()
			printl('Сервер был отключён')
		elif instruction == 'reconnect':
			try:
				self.chain_client.close()
			except:
				pass
			printl('Принудительный сброс подключений')
			try:
				self.chain_client = socket.socket()
				self.chain_client.connect((obj, 3333))
				print(self.chain_client)
				# self.accconn = self.chain_client
				# self.conn_data.append(self.chain_client)
				self.connection_established = True
				printl(f'Переподключено к {obj}')
			except Exception as err:
				self.connection_established = True
				self.chain_client = self.conn_data[-1]
				printl('no client found, wait for more connections')
				printl(err)
			# self.accconn = self.conn_data[-1]
		elif instruction == 'remember':
			self.creator_ip = obj
			printl('Запись серверных данных')
		elif instruction == 'datapack':
			printl('Выполнение содержимого пакета')
			printl(obj)
			exec(obj)
		elif instruction == 'genstart':
			filename = obj
			global filenames, past_conts
			file = get(filename)
			if file not in self.prev_file_data:
				self.prev_file_data[file] = self.__presets[file]
			if file not in directed_file_data:
				directed_file_data[file] = self.__presets[file]
			items = []
			for el in past_conts:
				items.append(el)
			if filename in items:
				pass
			else:
				past_conts[filename] = {}
			threading.Thread(target=dynamic_read).start()
			if genstart == False:
				threading.Thread(target=self.general_start).start()
				print('GENSTART!')
				threading.Thread(target=self.__flush_buffer).start()
				threading.Thread(target=self.__fill_buffer).start()
			filenames[file] = filename
		elif instruction == 'filepreset':
			num = False
			try:
				int(obj)
				num = True
			except: pass
			if num == False:
				def wait_till_assigned(filename, container):
					while True:
						try:
							filepath = assigned_base[filename]
							print(filepath+'\\'+filename[::-1][:filename[::-1].find("/")][::-1])
							with open(filepath+'\\'+filename[::-1][:filename[::-1].find("/")][::-1], 'w') as file:
								file.write(container)
							print(f'written: {container}')
							print(f'part {filename} stopped working')
							return None
						except Exception as err:
							print(err, assigned_base)
						time.sleep(3)
				filename = obj.split(BlockChainProtocol.DIVIDER)[0]
				contains = obj.split(BlockChainProtocol.DIVIDER)[1]
				self.__presets[filename] = contains
				threading.Thread(target=wait_till_assigned,args=(filename,contains,),daemon=True).start()
				self.__buffer_size = 262144*1024
				self.pres_f.append(filename)

				path = filename
				pathl = path[::-1][path[::-1].find('/'):][::-1][:-1]
				filename = path[::-1][:path[::-1].find('/')][::-1]
				pathn = pathl[::-1][:pathl[::-1].find('/')][::-1]
				text = pathn + '/' + filename

				sbc.initial_data[text] = contains
			else:
				self.__buffer_size = (int(obj)+30)*4
		elif instruction == 'revive':
			time.sleep(5)
			sndd = encode_by_conversion(base64.b64encode(self.chain.export_()).decode('ascii'))
			sndd = aes.encrypt(sndd, self.password)
			sndd = str(sndd) + '\n'
			for el in range(len(sndd) // 1024 + 1):
				self.__send(self.chain_client,
							sndd[el * 1024:(el + 1) * 1024].encode())

	def __open_server(self, ip, people):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server.bind((ip, 3333))
		server.setblocking(False)
		server.listen(people)
		server.settimeout(1)
		return server

	def __close_server(self, server):
		server.close()

	def __connect_side(self, ip, port=3333):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# sock.setblocking(False)
		while True:
			try:
				sock.connect((ip, port))
				break
			except Exception as err:
				print(err)
		return sock

	def __send(self, serv, data):
		printl(f'data: {data} was sent to {serv}')
		while True:
			try:
				serv.send(data)
				break
			except:
				break

	def __send_all(self, serv, data):
		printl(f'data: {data} was sent to {serv}')
		while True:
			try:
				serv: socket.socket
				serv.sendall(data)
				break
			except:
				break

	class Node:
		def __init__(self):
			self.ip = None
			self.connected_prev = None
			self.connected_aftr = None
