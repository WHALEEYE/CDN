LINKTYPE = sharelink
ALPHA = 0.1
DEBUG = True
DNSPORT = 8990

netsim_simple:
	python3 docker_setup/netsim/netsim.py servers start -s /home/CDN/docker_setup/netsim/servers/2servers

netsim_onelink_start:
	python3 docker_setup/netsim/netsim.py onelink start

netsim_onelink_run:
	python3 docker_setup/netsim/netsim.py onelink run -e /home/CDN/docker_setup/netsim/topology/onelink/onelink.events -l logs/onelink.log

netsim_onelink_stop:
	python3 docker_setup/netsim/netsim.py onelink stop

netsim_start:
	python3 docker_setup/netsim/netsim.py $(LINKTYPE) start

netsim_run:
	python3 docker_setup/netsim/netsim.py $(LINKTYPE) run -e /home/CDN/docker_setup/netsim/topology/$(LINKTYPE)/$(LINKTYPE).events -l logs/$(LINKTYPE)/$(ALPHA)/netsim.log

netsim_stop:
	python3 docker_setup/netsim/netsim.py $(LINKTYPE) stop

proxy_simple:
	python3 proxy.py logs/proxy_simple.log 0.125 8999 $(DNSPORT) 8080 $(DEBUG)

proxy_onelink:
	python3 proxy.py logs/proxy_onelink.log 0.125 8999 $(DNSPORT) 15641 $(DEBUG)

proxy1:
	python3 proxy.py logs/$(LINKTYPE)/$(ALPHA)/proxy1.log $(ALPHA) 8999 $(DNSPORT) 15640 $(DEBUG)

proxy2:
	python3 proxy.py logs/$(LINKTYPE)/$(ALPHA)/proxy2.log $(ALPHA) 8998 $(DNSPORT) 15641 $(DEBUG)

graph:
	cd graphs/$(LINKTYPE)/$(ALPHA) && python ../../../grapher.py ../../../logs/$(LINKTYPE)/$(ALPHA)/netsim.log ../../../logs/$(LINKTYPE)/$(ALPHA)/proxy1.log ../../../logs/$(LINKTYPE)/$(ALPHA)/proxy2.log