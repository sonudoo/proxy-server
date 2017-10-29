import socket,requests,_thread
requests.packages.urllib3.disable_warnings()
host = ''
port = 80
server_add = "http://proxyserver/"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

def handle_requests(conn, addr):
	print('Connected by', addr)
	data = conn.recv(1024)
	req = str(data.decode('ascii',errors='ignore')).split()
	catch_next = False
	req_url = ''
	for i in req:
		if(catch_next==True):
			req_url = str(i)[1:]
			break
		if(i=='GET'):
			catch_next = True
	req_url_parts = req_url.split('/')
	host = req_url_parts[0]+"//"+req_url_parts[2]+"/"
	req_url_parts = req_url.split('.')
	ext = req_url_parts[len(req_url_parts)-1]
	data = ''
	try:
		data = requests.get(url=req_url,verify=False)
		data = data.text
	except:
		pass
	res = ''
	if(data==''):
		res = '''
		HTTP/1.1 404 NOT_FOUND
		Date: Mon, 27 Jul 2009 12:28:53 GMT
		Server: Python/3.4 (Win32)
		Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
		Content-Length: 88
		Content-Type: text/html
		Connection: Closed
		<html>
		   <body>

		   <h1>Not Found: </h1>'''+req_url+'''

		   </body>
		</html>
		'''
	else:
		'''
		try:
			print(data)
		except:
			print(req_url)
		'''
		data = data.replace("href='","href='"+server_add+host)
		data = data.replace("src='","src='"+server_add+host)
		data = data.replace("href=\"","href=\""+server_add+host)
		data = data.replace("src=\"","src=\""+server_add+host)
		data = data.replace("url('","url('"+server_add+host)
		data = data.replace("url(","url("+server_add+host)
		data = data.replace("url(\"","url(\""+server_add+host)
		content = ''
		if(ext=='js'):
			content = 'application/javascript'
		elif(ext=='css'):
			content = 'application/stylesheet'
		elif(ext=='jpeg' or ext=='jpg'):
			content = 'image/jpg'
		elif(ext=='png'):
			content = 'image/png'
		else:
			content = 'text/html'

		res = '''
		HTTP/1.1 200 OK
		Date: Mon, 27 Jul 2009 12:28:53 GMT
		Server: Python/3.4 (Win32)
		Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
		Content-Length: 
		Content-Type: '''+content+'''
		Connection: Closed

		'''+data+''''''
	conn.sendall(res.encode(errors='ignore'))
	conn.close()

while True:
	conn, addr = s.accept()
	try:
	   _thread.start_new_thread(handle_requests,(conn, addr))
	except:
	   pass
	
