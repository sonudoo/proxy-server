'''

Developed by Sushant Kumar Gupta, BIT Mesra

This is a script for Proxy Server that 'proxifies' only HTTP requests

'''


import socket,requests,_thread,request_parser,response_parser,json
requests.packages.urllib3.disable_warnings() #This disables printing all SSL warnings
host = '' #This variable will store the host that the user wants to access.
port = 80 #The port at which the proxy server needs to be run. For HTTP use 80.
server_addr = "" #This is the proxy server name

'''
For example if the user requests http://proxyserver/https://www.imdb.com/

then server_addr = "http://proxyserver/" and host = "www.imdb.com" 

'''

# Bind to the port and keep listening.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port)) #Localhost
s.listen(100) #Queue upto 100 connections

def handle_requests(conn, addr):

	#Print the address and port of connected client.

	print('Connected by', addr)

	#Receive upto 65536 Bytes of data. I assume that all the HTTP headers are covered within a single recv()

	data = conn.recv(65536)

	#Parse the request using a library that I created. This will return a dictionary of request method, host name, url, headers etc.

	req = request_parser.parse(data)

	#Check if the request is a valid HTTP requests

	if(req['valid']==True and request_parser.validate(req['path'])==True):

		'''
		If it is valid then get the server_addr, URL, Hostname and absolute path

		For example if the client requests http://proxyserver/https://www.tansyoj.com/judge/index.php then
		server_addr = "http://proxyserver/"
		URL = "https://www.tansyoj.com/judge/index.php"
		Hostname = "www.tansyoj.com"
		absolute_path = "https://www.tansyoj.com/judge/"
		'''

		server_addr = "http://"+req['headers']['Host']+"/"
		url, host, absolute_path = request_parser.getUrlHostPath(req['path'])
		req['headers']['User-Agent'] = "ProxyServer/0.1" # Modify User-Agent header to your own name
		req['headers']['Host'] = host # Modify Host from proxyserver to whatever host the client actually wants to requests

		if(req['method']=="GET"):

			# Use requests to request the URL with forwarded (modified User-Agent and host) headers, without verifying SSL and not allowing redirects !Important

			res = requests.get(url,headers=req['headers'],verify=False,allow_redirects=False)

			conn.sendall(response_parser.parse(res, server_addr, absolute_path))
			conn.close()

			#Update counter to count the number of requests served successfully.
			f = open("counter.txt","r")
			curr = int(f.readline())
			f.close()
			f = open("counter.txt","w")
			f.write(str(curr+1))
			f.close()

			#Log the IP address of requestor and the requested website
			f = open("log.txt","a")
			f.write(str(addr[0])+" "+host+"\n")
			f.close()

		elif(req['method']=="POST"):

			# In case of POST, check the Content-Length that the user wants to POST. 

			'''
			Many browsers break the post data to packets and send them one by one. In such case try to recv()
			 till the length of content is equal to specified Content-Length in header

			'''
			post_data_length = int(req['headers']['Content-Length'])

			if(req['raw_content'] is None):
				req['raw_content'] = b''

			while(len(req['raw_content']) < post_data_length):
				data = conn.recv(65536)
				req['raw_content'] += data

			post_data = request_parser.getPostData(req['raw_content'])

			# Send POST requests. Allowing redirect is False because we want to handle 302 and 301 manually.

			print(post_data)
			res = requests.post(url,headers=req['headers'],data=post_data,verify=False,allow_redirects=False)
			print(res.headers)

			conn.sendall(response_parser.parse(res, server_addr, absolute_path))
			conn.close()


		elif(req['method']=="PUT"):

			conn.sendall("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\nFile upload is not supported".encode())
			conn.close()


		else:
			conn.sendall(("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\nInvalid request.. Please make sure that your request format is correct. For example if you want to visit www.yahoo.com then enter <b>http://ip_address/http://www.yahoo.com/</b> into your browser and NOT just <b>http://proxyserver/www.yahoo.com/</b><br><br>Total requests served: "+str(curr)+"").encode())
			conn.close()
	else:

		#It is a invalid request
		f = open("counter.txt","r")
		curr = int(f.readline())
		f.close()
		conn.sendall(("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\nInvalid request.. Please make sure that your request format is correct. For example if you want to visit www.yahoo.com then enter <b>http://ip_address/http://www.yahoo.com/</b> into your browser and NOT just <b>http://proxyserver/www.yahoo.com/</b><br><br>Total requests served: "+str(curr)+"").encode())
		conn.close()

	return

while True:

	#Go on accepting new connection. Whenever a new connection is made, create a new thread to handle it.
	conn, addr = s.accept()
	try:
		_thread.start_new_thread(handle_requests,(conn, addr))
	except e:
		conn.sendall("HTTP/1.1 500 INTERNAL_SERVER_ERROR\r\nContent-type: text/html\r\n\r\nError occured. Please try again later".encode())
		conn.close()
	
