import os
import re
import signal
import sys
import time
import xml.dom.minidom
from multiprocessing import Process

import requests
from flask import Flask, Response

app = Flask(__name__)


@app.before_request
def refresh():
    os.kill(os.getppid(), signal.SIGINT)


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
    server_port = request_dns()

    selected_bitrate = bitrates[sorted(bitrates)[0]]
    debug(
        f"(port {server_port}) Current tput: {tput[server_port] if server_port in tput else 0}"
    )
    if server_port in tput and bitrates:
        for bitrate in sorted(bitrates)[::-1]:
            if bitrate * 1.5 <= tput[server_port]:
                selected_bitrate = bitrate
                break

    chunk_name = f"{selected_bitrate}Seg{seg_num}-Frag{frag_num}"
    debug(f"(port {server_port}) Requesting {chunk_name}")
    start = time.time()
    rep = requests.get(f"http://localhost:{server_port}/vod/{chunk_name}")
    end = time.time()
    duration = end - start
    cur_tput = (len(rep.content) * 8) / (duration * 1024)
    calculate_throughput(cur_tput, server_port)

    log(
        time.time(),
        duration,
        cur_tput,
        tput[server_port],
        selected_bitrate,
        server_port,
        seg_num,
        frag_num,
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
    else:
        res = requests.get(f"http://localhost:{1127}/dns")
        return int(res.content)


def calculate_throughput(cur_tput, server_port):
    global tput
    if server_port not in tput:
        tput[server_port] = cur_tput
    else:
        tput[server_port] = tput[server_port] * (1 - alpha) + cur_tput * alpha
    debug(
        f"(port {server_port}) calculated tput: {cur_tput} -- renewed tput: {tput[server_port]}"
    )


def debug(msg):
    if debug_flag:
        print(f"\033[36m[DEBUG] {msg}\033[0m")


def info(msg):
    print(f"\033[32m[INFO] {msg}\033[0m")


def log(time, duration, tput, avg_tput, bitrate, server_port, chunk_seg, chunk_frag):
    log_file.write(
        f"{time} {duration} {tput} {avg_tput} {bitrate} {server_port} {chunk_seg}-{chunk_frag}\n"
    )


def int_handler(a, b):
    global time_cnt
    time_cnt = 0


if __name__ == "__main__":
    time_cnt = 0
    timeout = 30
    default_port = None
    debug_flag = False
    tput = {}
    bitrates = {}
    if len(sys.argv) < 5:
        sys.stderr.write("Too few arguments!\n")
        exit()
    log_file = open(sys.argv[1], "w", encoding="utf8")
    alpha = float(sys.argv[2])
    port = int(sys.argv[3])
    dns_port = int(sys.argv[4])
    if len(sys.argv) > 5:
        default_port = int(sys.argv[5])
    if len(sys.argv) > 6:
        debug_flag = bool(sys.argv[6])

    signal.signal(signal.SIGINT, int_handler)


    server = Process(target=app.run, kwargs={"host": "0.0.0.0", "port": port, "threaded": True})
    server.start()
    while True:
        if time_cnt == timeout:
            server.terminate()
            server.join()
            log_file.close()
            info(f"No requests for {timeout} seconds. Quitted automatically.")
            break
        time_cnt += 1
        time.sleep(1)
