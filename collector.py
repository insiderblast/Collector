print"This is simple Open Source program"
print"Coded by the dutchman"
print"[[]|_ |_ [= [ T [] R"
import requests
import shodan

SHODAN_API_KEY=str(raw_input("Enter your shodan api key:"))
api=shodan.Shodan(SHODAN_API_KEY)
target=str(raw_input("Enter target web url:"))
dnsResolve='https://api.shodan.io/dns/resolve?hostname='+target+'&key='+SHODAN_API_KEY
try:
  #FIRST we need to resolve targets domain to an IP
  resolved=requests.get(dnsResolve)
  hostIP=resolved.json()[target]
  #Then we need to do a shodan search on that IP
  host=api.host(hostIP)
  print "IP:%s" %host['ip_str']
  print "Organization:%s" %host.get('org','n/a')
  print "Operating system:%s" %host.get('os','n/a')
  #print banners
  for item in host['data']:
    print "Port:%s" %item['port']
    print "Banner:%s" %item['data']
  #print possible vulnerabilities information
  for item in host['vulns']:
    CVE=item.replace('!','')
    print 'Vulns:%s' %item
    exploits=api.exploits.search(CVE)
    for item in exploits['matches']:
      if item.get('cve')[0]==CVE:
         print item.get('description')
except:
     'An error occured'
