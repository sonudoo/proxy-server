import socket,requests,_thread,request_parser,response_parser,json
requests.packages.urllib3.disable_warnings()
host = ''
port = 80
server_add = "http://localhost/"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

def handle_requests(conn, addr):
	print('Connected by', addr)
	data = conn.recv(65536)
	conn.sendall("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\nBitzoom is currently down.. Please stop connecting now".encode())
	conn.close()
	return

while True:
	conn, addr = s.accept()
	conn, addr = s.accept()
	try:
	   _thread.start_new_thread(handle_requests,(conn, addr))
	except:
	   pass
	
