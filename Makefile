PORT = 8997
TIME = 1

netsim_simple:
	python3 docker_setup/netsim/netsim.py servers start -s /home/CDN/docker_setup/netsim/servers/2servers

netsim_onelink_start:
	python3 docker_setup/netsim/netsim.py onelink start

netsim_onelink_run:
	python3 docker_setup/netsim/netsim.py onelink run -e /home/CDN/docker_setup/netsim/topology/onelink/onelink.events -l logs/onelink.log

netsim_onelink_stop:
	python3 docker_setup/netsim/netsim.py onelink stop

netsim_sharelink_start:
	python3 docker_setup/netsim/netsim.py sharelink start

netsim_sharelink_run:
	python3 docker_setup/netsim/netsim.py onelink run -e /home/CDN/docker_setup/netsim/topology/onelink/onelink.events -l logs/sharelink/netsim.log

netsim_sharelink_stop:
	python3 docker_setup/netsim/netsim.py onelink stop

proxy_simple:
	python3 proxy.py logs/proxy_simple.log 0.125 8999 8990 8080 True

proxy_onelink:
	python3 proxy.py logs/proxy_onelink.log 0.125 8999 8990 15641 True

proxy_sharelink1:
	python3 proxy.py logs/sharelink/proxy1.log 0.125 8999 8990 15640 True

proxy_sharelink2:
	python3 proxy.py logs/sharelink/proxy2.log 0.125 8998 8990 15641 True

sharelink_graph:
	cd graphs && python ../grapher.py ../logs/sharelink/netsim.log ../logs/sharelink/proxy1.log ../logs/sharelink/proxy2.log 