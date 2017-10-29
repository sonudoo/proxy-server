import socket
while True:
	host = '192.168.117.12'
	port = 8000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(1)
	conn, addr = s.accept()
	print('Connected by', addr)
	data = conn.recv(1024)
	req = str(data.decode('ascii',errors='ignore'))
	print(req)
	res = '''
	HTTP/1.1 200 OK
	Date: Mon, 27 Jul 2009 12:28:53 GMT
	Server: Apache/2.2.14 (Win32)
	Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
	Content-Length: 88
	Content-Type: text/html
	Connection: Closed
	<html>
	   <body>

	   <h1>Hello, Bot!</h1>

	   </body>
	</html>
	'''
	conn.send(res.encode(errors='ignore'))
	conn.close()