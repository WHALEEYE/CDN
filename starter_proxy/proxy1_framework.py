import requests
from flask import Flask, Response, Request

app = Flask(__name__)


@app.route("/example")
def simple():
    return Response(requests.get("http://www.example.com"))


@app.route("/")
def index():
    port = request_dns()
    return Response(requests.get(f"http://localhost:{port}"))


def modify_request(message):
    """
    Here you should change the requested bit rate according to your computation of throughput.
    And if the request is for big_buck_bunny.f4m, you should instead request big_buck_bunny_nolist.f4m
    for client and leave big_buck_bunny.f4m for the use in proxy.
    """


def request_dns():
    return 8080


def calculate_throughput():
    """
    Calculate throughput here.
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8999)
