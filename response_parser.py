import time

def parse(res, server_addr, absolute_path):

	res.headers['Server'] = "ProxyServer/0.1"
	try:
		del res.headers['Content-Encoding']
		del res.headers['Transfer-Encoding']
	except:
		pass
	if(res.status_code==404):
		ret = "HTTP/1.1 404 NOT_FOUND\r\nDate: "+str(time.asctime(time.localtime(time.time())))+"\r\nServer: ProxyServer/0.1\r\nContent-Type: text/html\r\n\r\n<title>Not Found</title><h1 align='center'>Not Found</h1><center>The file you are looking for was not found. Please recheck the URL</center>"
		return ret.encode(errors='ignore')

	elif(res.status_code==301 or res.status_code==302):

		res.headers['Content-Length'] = len(res.content)

		ret = "HTTP/1.1 "+str(res.status_code)+" OK\r\n"

		for x in res.headers:
			if(x=="Location" or x=="location"):
				loc = res.headers[x]
				if(loc[0:7]=="http://" or loc[0:8]=="https://"):
					pass
				else:
					loc = absolute_path + loc
				ret += str(x)+": "+str(server_addr+loc)+"\r\n"
			else:
				ret += str(x)+": "+str(res.headers[x])+"\r\n"
		ret += "\r\n"

		return ret.encode(errors='ignore')+res.content



	elif(res.status_code==304):

		ret = "HTTP/1.1 304 OK\r\n"
		return ret.encode(errors='ignore')


	elif(res.status_code==200):

		content = res.content

		if(res.headers['Content-Type'].split(";")[0]=="text/html"):
			content = parseHTML(res, server_addr)

		res.headers['Content-Length'] = len(content)

		ret = "HTTP/1.1 200 OK\r\n"
		for x in res.headers:
			ret += str(x)+": "+str(res.headers[x])+"\r\n"
		ret += "\r\n"

		return ret.encode(errors='ignore')+content

	else:
		ret = "HTTP/1.1 500 INTERNAL_SERVER_ERROR\r\nDate: "+str(time.asctime(time.localtime(time.time())))+"\r\nServer: ProxyServer/0.1\r\nContent-Type: text/html\r\n\r\n<title>Proxy Error</title><h1 align='center'>Proxy Error</h1><center>An error occured that the proxy server is not configured to handle.</center>"
		return ret.encode(errors='ignore')


def parseHTML(res, server_addr):
	data = res.content.decode(errors='ignore')

	url = res.url.split("/")

	cwd = ""

	for i in range(0,len(url)-1):
		cwd += url[i]+"/"


	data = data.replace("href='//","href='http://")
	data = data.replace("src='//","src='http://")
	data = data.replace("href=\"//","href=\"http://")
	data = data.replace("src=\"//","src=\"http://")

	data = data.replace("href='/","href='")
	data = data.replace("src='/","src='")
	data = data.replace("href=\"/","href=\"")
	data = data.replace("src=\"/","src=\"")

	data = data.replace("href='","href='"+server_addr+cwd)
	data = data.replace("src='","src='"+server_addr+cwd)
	data = data.replace("href=\"","href=\""+server_addr+cwd)
	data = data.replace("src=\"","src=\""+server_addr+cwd)

	data = data.replace("href='"+server_addr+cwd+"h","href='"+server_addr+"h")
	data = data.replace("href=\""+server_addr+cwd+"h","href=\""+server_addr+"h")
	data = data.replace("src='"+server_addr+cwd+"h","src='"+server_addr+"h")
	data = data.replace("src=\""+server_addr+cwd+"h","src=\""+server_addr+"h")

	return data.encode(errors='ignore')
