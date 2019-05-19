import sys
try:
	sys.stdin = open("log.txt","r")
	sites = dict()
	hosts = dict()
	while 1==1:
		try:
			host_addr, site = input().split()
		except:
			break
		if(site in sites):
			sites[site] += 1
		else:
			sites[site] = 1

		if(host_addr in hosts):
			hosts[host_addr] += 1
		else:
			hosts[host_addr] = 1

	print("Top 10 sites are:-\n\nSitename\tHits\n\n")

	i = 10
	for key, value in sorted(sites.items(), key=lambda x: x[1], reverse=True):
		print(str(key)+"\t\t\t\t\t"+str(value))
		i -= 1
		if(i==0):
			break

	print("\n\nTop 10 hosts are:-\n\nHost\tHits\n\n")

	i = 10
	for key, value in sorted(hosts.items(), key=lambda x: x[1], reverse=True):
		print(str(key)+"\t\t\t\t\t"+str(value))
		i -= 1
		if(i==0):
			break

except:
	print("Log file was not found..")