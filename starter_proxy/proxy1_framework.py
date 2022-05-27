import requests
from flask import Flask, Response, Request
import xml.dom.minidom
import time
import re
import sys

app = Flask(__name__)


@app.route("/index.html")
def index():
    port = request_dns()
    return Response(requests.get(f"http://localhost:{port}/index.html"))


@app.route("/vod/big_buck_bunny.f4m")
def forward_f4m():
    port = request_dns()
    original_f4m = requests.get(f"http://localhost:{port}/vod/big_buck_bunny.f4m")
    parse_f4m(original_f4m.content.strip())
    f4m_file = requests.get(f"http://localhost:{port}/vod/big_buck_bunny_nolist.f4m")
    return Response(f4m_file)


@app.route("/vod/<chunk_name>")
def forward(chunk_name):
    return Response(modify_request(chunk_name))


@app.route("/swfobject.js")
def obj():
    port = request_dns()
    return Response(requests.get(f"http://localhost:{port}/swfobject.js"))


@app.route("/StrobeMediaPlayback.swf")
def swf():
    port = request_dns()
    return Response(requests.get(f"http://localhost:{port}/StrobeMediaPlayback.swf"))


def modify_request(chunk_name):
    rst = re.search("1000Seg([0-9]*)-Frag([0-9]*)", chunk_name)
    seg_num = rst.group(1)
    frag_num = rst.group(2)

    selected_bitrate = bitrates[sorted(bitrates)[0]]
    debug(f"Current tput: {tput}")
    if tput != 0 and bitrates:
        for bitrate in sorted(bitrates)[::-1]:
            if bitrate * 1.5 <= tput:
                selected_bitrate = bitrate
                break

    server_port = request_dns()
    chunk_name = f"{selected_bitrate}Seg{seg_num}-Frag{frag_num}"
    start = time.clock()
    debug(f"Requesting {chunk_name}")
    rep = requests.get(f"http://localhost:{server_port}/vod/{chunk_name}")
    end = time.clock()
    duration = end - start
    calculate_throughput(len(rep.content), duration)
    log(
        time.time(),
        duration,
        len(rep.content) / (duration * 1024),
        tput,
        selected_bitrate,
        server_port,
        seg_num,
        frag_num
    )
    return rep


def parse_f4m(f4m_data):
    global bitrates
    DOMTree = xml.dom.minidom.parseString(f4m_data)
    collection = DOMTree.documentElement
    medias = collection.getElementsByTagName("media")
    bitrates = {
        int(media.getAttribute("bitrate")): media.getAttribute("url")
        for media in medias
    }


def request_dns():
    if not default_port is None:
        return default_port
    return 8080


def calculate_throughput(trunk_size, time_cost):
    global tput
    new_tput = trunk_size / (time_cost * 1024)
    if tput == 0:
        tput = new_tput
    else:
        tput = tput * (1 - alpha) + new_tput * alpha
    debug(f"data len: {trunk_size}, time cost: {time_cost}, new tput: {tput}")


def debug(msg):
    if debug_flag:
        print(f"\033[36m[DEBUG] {msg}\033[0m")


def log(time, duration, tput, avg_tput, bitrate, server_port, chunk_seg, chunk_frag):
    log_file.write(
        f"{time} {duration} {tput} {avg_tput} {bitrate} {server_port} {chunk_seg}-{chunk_frag}\n"
    )


if __name__ == "__main__":
    default_port = None
    debug_flag = False
    tput = 0
    bitrates = {}
    if len(sys.argv) < 5:
        sys.stderr.write("Too few arguments!\n")
        exit()
    log_file = open(str(sys.argv[1]), "w+", encoding="utf8")
    alpha = float(sys.argv[2])
    port = int(sys.argv[3])
    dns_port = int(sys.argv[4])
    if len(sys.argv) > 5:
        default_port = int(sys.argv[5])
    if len(sys.argv) > 6:
        debug_flag = bool(sys.argv[6])

    try:
        app.run(host="0.0.0.0", port=port)
    except KeyBoardInterrupt:
        log_file.close()
        exit()
