import time

def parse(res):

	res.headers['Server'] = "ProxyServer/0.1"
	try:
		del res.headers['Content-Encoding']
	except:
		pass
	if(res.status_code==404):
		ret = "HTTP/1.1 404 NOT_FOUND\r\nDate: "+str(time.asctime(time.localtime(time.time())))+"\r\nServer: ProxyServer/0.1\r\nContent-Type: text/html\r\n\r\n<title>Not Found</title><h1 align='center'>Not Found</h1><center>The file you are looking for was not found. Please recheck the URL</center>"
		return ret.encode(errors='ignore')

	elif(res.status_code==301 or res.status_code==302):

		res.headers['Content-Length'] = len(res.content)

		ret = "HTTP/1.1 "+str(res.status_code)+" OK\r\n"

		for x in res.headers:
			ret += str(x)+": "+str(res.headers[x])+"\r\n"
		ret += "\r\n"

		print(ret)

		return ret.encode(errors='ignore')+res.content



	elif(res.status_code==304):
		ret = "HTTP/1.1 304 OK\r\n"
		return ret.encode(errors='ignore')


	elif(res.status_code==200):

		content = res.content

		if(res.headers['Content-Type'].split(";")[0]=="text/html"):
			content = parseHTML(res)

		res.headers['Content-Length'] = len(content)

		ret = "HTTP/1.1 200 OK\r\n"
		for x in res.headers:
			ret += str(x)+": "+str(res.headers[x])+"\r\n"
		ret += "\r\n"
		print(ret)
		return ret.encode(errors='ignore')+content
	else:
		ret = "HTTP/1.1 500 INTERNAL_SERVER_ERROR\r\nDate: "+str(time.asctime(time.localtime(time.time())))+"\r\nServer: ProxyServer/0.1\r\nContent-Type: text/html\r\n\r\n<title>Proxy Error</title><h1 align='center'>Proxy Error</h1><center>An error occured that the proxy server is not configured to handle.</center>"
		return ret.encode(errors='ignore')


def parseHTML(res):
	data = res.content.decode(errors='ignore')

	url = res.url.split("/")

	cwd = ""

	for i in range(0,len(url)-1):
		cwd += url[i]+"/"

	server_add = "http://localhost:8000/"

	data = data.replace("href='//","href='http://")
	data = data.replace("src='//","src='http://")
	data = data.replace("href=\"//","href=\"http://")
	data = data.replace("src=\"//","src=\"http://")

	data = data.replace("href='/","href='")
	data = data.replace("src='/","src='")
	data = data.replace("href=\"/","href=\"")
	data = data.replace("src=\"/","src=\"")

	data = data.replace("href='","href='"+server_add+cwd)
	data = data.replace("src='","src='"+server_add+cwd)
	data = data.replace("href=\"","href=\""+server_add+cwd)
	data = data.replace("src=\"","src=\""+server_add+cwd)

	data = data.replace("href='"+server_add+cwd+"h","href='"+server_add+"h")
	data = data.replace("href=\""+server_add+cwd+"h","href=\""+server_add+"h")
	data = data.replace("src='"+server_add+cwd+"h","src='"+server_add+"h")
	data = data.replace("src=\""+server_add+cwd+"h","src=\""+server_add+"h")

	return data.encode(errors='ignore')
