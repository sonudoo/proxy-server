import time,re

'''
This script prepares the response in proper format to be sent

'''


def parse(res, server_addr, absolute_path):

	# Set the Server header to your own server

	res.headers['Server'] = "ProxyServer/0.1"

	try:
		'''
		!Important
		The requests library automatically decompresses the response data. So remove the "Content-Encoding" headers as we would be sending data uncompressed.
		Also the content will no longer be chunked (divided) as we would send the complete data at once so remove the "Transfer-Encoding" as well
		'''

		del res.headers['Content-Encoding']
		del res.headers['Transfer-Encoding']
	except:
		pass

	#Check the response code and return response bytes accordingly.

	if(res.status_code==404):
		ret = "HTTP/1.1 404 NOT_FOUND\r\nDate: "+str(time.asctime(time.localtime(time.time())))+"\r\nServer: ProxyServer/0.1\r\nContent-Type: text/html\r\n\r\n<title>Not Found</title><h1 align='center'>Not Found</h1><center>The file you are looking for was not found. Please recheck the URL</center>"
		return ret.encode(errors='ignore')


	elif(res.status_code==301 or res.status_code==302):

		'''
		This (Redirections) is a tricky part.
		If the redirect location starts with http or https then it already a absolute address, so we just attach server_addr at the beginning.
		Else it is a relative address and so we attach server_addr+absolute_path at the beginning.

		Ex: Suppose the rediect location is 'judge/index.php' after requesting http://proxyserver/https://www.tansyoj.com/ 
		Then the new redirect location will be http://proxyserver/https://www.tansyoj.com/judge/index.php

		Alternatively Suppose the rediect location is 'https://www.google.com' after requesting http://proxyserver/https://www.tansyoj.com/ 
		Then the new redirect location will be http://proxyserver/https://www.google.com
		'''
		res.headers['Content-Length'] = len(res.content) # Get the new length of the Content as it has been decompressed by requests

		#Prepare the return headers

		ret = "HTTP/1.1 "+str(res.status_code)+" OK\r\n"

		for x in res.headers:

			# Rest of the headers will remain the same except for Location or location

			if(x=="Location" or x=="location"):
				loc = res.headers[x]
				if(loc[0:7]=="http://" or loc[0:8]=="https://"):
					# Absolute address
					
					ret += str(x)+": "+str(server_addr+loc)+"\r\n"

				else:
					# Relative address

					host_name = absolute_path.split('/')
					host_name = host_name[0] + "//" + host_name[2] + "/"

					if(loc[0]=='/'):

						# Its a address relative home directory. 

						loc = server_addr + host_name + loc[1:]
					else:

						# Its a address relative to CWD

						loc = server_addr + absolute_path + loc

					ret += str(x)+": "+str(loc)+"\r\n"
			elif(x=="Set-Cookie"):

				#Replace the Set-Cookie domain to current server address

				rep = "" #Replacement string

				i = 0
				l = len(res.headers[x])

				while i<l:
					if(i+7<l and res.headers[x][i:i+7]=="domain="):
						rep += "domain="+server_addr.split('/')[2]
						i += 7
						while(i<l and res.headers[x][i]!=','):
							i += 1
					if(i==l):
						break
					rep += res.headers[x][i]
					i+=1

				ret += str(x)+": "+str(rep)+"\r\n"
			else:
				ret += str(x)+": "+str(res.headers[x])+"\r\n"
		ret += "\r\n"

		#Return the encoded response with the decompressed content attached at the end

		return ret.encode(errors='ignore')+res.content



	elif(res.status_code==304):
		# I still don't know what to do with this error code.
		ret = "HTTP/1.1 304 OK\r\n"
		return ret.encode(errors='ignore')


	elif(res.status_code==200):

		#Probably the most simple response

		content = res.content

		if(res.headers['Content-Type'].split(";")[0]=="text/html"):

			'''
			If the content type is text/html then parse it to replace all 'address' to 'server_addr+address'.
			This will help to load all page contents properly. 
			I need to do something similar for Javascripts and CSS and HTTP forms. I will do it in next version.
			'''
			content = parseHTML(res, server_addr)

		res.headers['Content-Length'] = len(content) # Get the new length of the Content as it has been decompressed by requests

		ret = "HTTP/1.1 200 OK\r\n"
		for x in res.headers:
			ret += str(x)+": "+str(res.headers[x])+"\r\n"
		ret += "\r\n"

		return ret.encode(errors='ignore')+content

	else:

		# Some unknown error occured
		
		ret = "HTTP/1.1 500 INTERNAL_SERVER_ERROR\r\nDate: "+str(time.asctime(time.localtime(time.time())))+"\r\nServer: ProxyServer/0.1\r\nContent-Type: text/html\r\n\r\n<title>Proxy Error</title><h1 align='center'>Proxy Error</h1><center>An error occured that the proxy server is not configured to handle.</center>"
		return ret.encode(errors='ignore')


def parseHTML(res, server_addr):

	'''
	I can't exaplin what I did here. I did a lot of things here but the basic thing was to replace

	href="https://www.google.com/"

	to

	href="http://proxyserver/https://www.google.com"

	'''

	data = res.content.decode(errors='ignore')

	url = res.url.split("/")

	cwd = ""

	for i in range(0,len(url)-1):
		cwd += url[i]+"/"


	data = data.replace("href='//","href='http://")
	data = data.replace("src='//","src='http://")
	data = data.replace("action='//","action='http://")
	data = data.replace("href=\"//","href=\"http://")
	data = data.replace("src=\"//","src=\"http://")
	data = data.replace("action=\"//","action=\"http://")

	data = data.replace("href='/","href='")
	data = data.replace("src='/","src='")
	data = data.replace("action='/","action='")
	data = data.replace("href=\"/","href=\"")
	data = data.replace("src=\"/","src=\"")
	data = data.replace("action=\"/","action=\"")

	data = data.replace("href='","href='"+server_addr+cwd)
	data = data.replace("src='","src='"+server_addr+cwd)
	data = data.replace("action='","action='"+server_addr+cwd)
	data = data.replace("href=\"","href=\""+server_addr+cwd)
	data = data.replace("src=\"","src=\""+server_addr+cwd)
	data = data.replace("action=\"","action=\""+server_addr+cwd)

	data = data.replace("href='"+server_addr+cwd+"h","href='"+server_addr+"h")
	data = data.replace("href=\""+server_addr+cwd+"h","href=\""+server_addr+"h")
	data = data.replace("src='"+server_addr+cwd+"h","src='"+server_addr+"h")
	data = data.replace("src=\""+server_addr+cwd+"h","src=\""+server_addr+"h")
	data = data.replace("action='"+server_addr+cwd+"h","action='"+server_addr+"h")
	data = data.replace("action=\""+server_addr+cwd+"h","action=\""+server_addr+"h")

	return data.encode(errors='ignore')
