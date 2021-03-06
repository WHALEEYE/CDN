LINKTYPE ?= sharelink
ALPHA ?= 0.1
DEBUG = True
DNSPORT = 5533
SERVERNUM = 2
PROXYPORT ?= 8999

netsim_simple:
	python3 docker_setup/netsim/netsim.py servers start -s /home/CDN/docker_setup/netsim/servers/$(SERVERNUM)servers

netsim_simple_stop:
	python3 docker_setup/netsim/netsim.py servers stop -s /home/CDN/docker_setup/netsim/servers/$(SERVERNUM)servers

netsim_start:
	python3 docker_setup/netsim/netsim.py $(LINKTYPE) start

netsim_run:
	python3 docker_setup/netsim/netsim.py $(LINKTYPE) run -e /home/CDN/docker_setup/netsim/topology/$(LINKTYPE)/$(LINKTYPE).events -l logs/$(LINKTYPE)/$(ALPHA)/netsim.log

netsim_stop:
	python3 docker_setup/netsim/netsim.py $(LINKTYPE) stop

proxy_simple:
	python3 proxy.py logs/proxy_simple.log 0.125 $(PROXYPORT) $(DNSPORT)

proxy_onelink:
	python3 proxy.py logs/proxy_onelink.log 0.125 8999 $(DNSPORT) 15641 $(DEBUG)

proxy1:
	python3 proxy.py logs/$(LINKTYPE)/$(ALPHA)/proxy1.log $(ALPHA) 8999 $(DNSPORT) 15640 $(DEBUG)

proxy2:
	python3 proxy.py logs/$(LINKTYPE)/$(ALPHA)/proxy2.log $(ALPHA) 8998 $(DNSPORT) 15641 $(DEBUG)

graph:
	cd graphs/$(LINKTYPE)/$(ALPHA) && ../../../grapher.py ../../../logs/$(LINKTYPE)/$(ALPHA)/netsim.log ../../../logs/$(LINKTYPE)/$(ALPHA)/proxy1.log ../../../logs/$(LINKTYPE)/$(ALPHA)/proxy2.log

DNS_simple:
	python3 dns.py /home/CDN/docker_setup/netsim/servers/$(SERVERNUM)servers $(DNSPORT)