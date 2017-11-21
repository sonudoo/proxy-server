import urllib.parse

'''
This script is used to parse the request in proper format that the requests library can use.

'''
def parse(req):
	ret = dict() #The return object

	ret['valid'] = True

	ret['raw_request'] = req #The raw bytes that we got through client

	#Split the request at '\r\n\r\n' which will seperate the headers and the content. 
	s = req.decode('utf-8',errors='ignore')
	s = s.split('\r\n\r\n')

	try:
		ret['raw_headers'] = (s[0]+'\r\n\r\n').encode(encoding='utf-8',errors='ignore')
	except:
		ret['raw_headers'] = None

	try:
		ret['raw_content'] = s[1].encode()
	except:
		ret['raw_content'] = None


	#Now split the headers part at '\r\n'. The first split will be like "GET /path/ HTTP/1.1". Let this be top_headers
	headers = s[0]+'\r\n\r\n'

	headers = headers.split('\r\n')

	top_headers = headers[0].split()

	#Parse the top headers to validate the HTTP request and extract the request type, method, path and HTTP version
	if(len(top_headers)!=3):
		ret['valid'] = False
		return ret

	if(top_headers[0]!="GET" and top_headers[0]!="POST" and top_headers[0]!="PUT" and top_headers[0]!="DELETE"):
		ret['valid'] = False
		return ret

	http_version = top_headers[2].split('/')

	if(http_version[0]!="HTTP"):
		ret['valid'] = False
		return ret

	http_version_number = 1.1

	try:
		http_version_number = float(http_version[1])
	except:
		ret['valid'] = False
		return ret

	ret['method'] = top_headers[0]

	ret['http_version'] = http_version

	ret['http_version_number'] = http_version_number

	ret['path'] = top_headers[1]

	#Now extract rest of the headers by spliting at ': '

	ret['headers'] = dict()

	for i in range(1,len(headers)):
		header = headers[i].split(': ')
		if(len(header)!=2):
			continue
		else:
			ret['headers'][header[0]] = header[1]

	#Finally return the parsed request object.

	return ret


def validate(path):

	'''
	For a path (and hence a URL) to be valid, it must start with a protocol (http or https) and must contain host name.
	'''

	url = path[1:]

	protocol = url.split('://')[0]

	if(protocol!="http" and protocol!="https"):
		return False

	try:
		protocol_removed = url.split('://')[1]
	except:
		return False

	host = protocol_removed.split('/')[0]

	if(host==""):
		return False

	return True

def getUrlHostPath(path):

	'''
	This function returns the URL, absolute path and Host name
	'''

	s = path.split('/')

	host = s[3]

	absolute_path = s[1]+"//"+s[3]+"/" #Example: https: + "//" + www.imdb.com + "/" + <rest of the path>

	for i in range(4,len(s)-1): # This loop adds <rest of the path>
		absolute_path += s[i]+"/"

	return path[1:],host,absolute_path

def getPostData(raw_content):

	'''
	This function parses the post data and returns a equivalent dictionary that can be used for requests library
	'''

	data = raw_content.decode().split('&')

	post_data = dict()

	for i in data:
		key = i.split('=')[0]
		value = ""
		try:
			value = urllib.parse.unquote(urllib.parse.unquote_plus((i.split('=')[1]))) #Very important. First decode '+' symbol to spaces and then decode other URL characters.
		except:
			pass
		post_data[key] = value

	return post_data