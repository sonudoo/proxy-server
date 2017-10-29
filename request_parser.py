import urllib.parse

def parse(req):
	ret = dict()

	ret['valid'] = True

	ret['raw_request'] = req

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

	headers = s[0]+'\r\n\r\n'

	headers = headers.split('\r\n')

	top_headers = headers[0].split()

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

	ret['headers'] = dict()

	for i in range(1,len(headers)):
		header = headers[i].split(': ')
		if(len(header)!=2):
			continue
		else:
			ret['headers'][header[0]] = header[1]

	return ret


def validate(path):

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

def getUrl(path):

	return path[1:]

def getPostData(raw_content):

	data = raw_content.decode().split('&')

	post_data = dict()

	for i in data:
		key = i.split('=')[0]
		value = urllib.parse.unquote(urllib.parse.unquote_plus((i.split('=')[1])))
		post_data[key] = value

	return post_data