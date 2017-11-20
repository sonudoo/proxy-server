import socket,requests,_thread,request_parser,response_parser,json
requests.packages.urllib3.disable_warnings()
host = ''
port = 80
server_addr = ""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

def handle_requests(conn, addr):
	print('Connected by', addr)
	data = conn.recv(65536)
	req = request_parser.parse(data)

	if(req['valid']==True and request_parser.validate(req['path'])==True):

		server_addr = "http://"+req['headers']['Host']+"/"
		url, host, absolute_path = request_parser.getUrlHostPath(req['path'])
		req['headers']['User-Agent'] = "ProxyServer/0.1"
		req['headers']['Host'] = host

		if(req['method']=="GET"):

			res = requests.get(url,headers=req['headers'],verify=False,allow_redirects=False)
			conn.sendall(response_parser.parse(res, server_addr, absolute_path))
			conn.close()

		elif(req['method']=="POST"):

			post_data = request_parser.getPostData(req['raw_content'])
			res = requests.post(url,headers=req['headers'],data=post_data,verify=False,allow_redirects=False)


			conn.sendall(response_parser.parse(res, server_addr, absolute_path))
			conn.close()


		elif(req['method']=="PUT"):
			conn.sendall("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\nFile upload is not supported".encode())
			conn.close()


		else:
			conn.sendall("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\nBitzoom is currently down.. Please stop connecting now".encode())
			conn.close()
	else:
		#It is a invalid URL that the user wants to send requests to
		conn.sendall("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\nBitzoom is currently down.. Please stop connecting now".encode())
		conn.close()
		return

while True:
	conn, addr = s.accept()
	try:
	   _thread.start_new_thread(handle_requests,(conn, addr))
	except e:
	   print(e)
	
