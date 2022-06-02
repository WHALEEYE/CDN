from webbrowser import get
from flask import Flask, Response, Request
import sys

app = Flask(__name__)

@app.route("/dns")
def dns():
    port = get_port()
    return str(port)


def get_port():
    global pt
    max_len = len(ports)
    tar_port = ports[pt]
    pt = (pt + 1) % max_len
    return tar_port

if __name__ == "__main__":    
    ports = []
    pt = 0
    with open(sys.argv[1], encoding="utf8") as port_file:
        for line in port_file:
            ports.append(int(line))
    
    port = int(sys.argv[2])
    try:
        app.run(host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        exit()