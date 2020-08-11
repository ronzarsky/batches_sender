import multiprocessing as mp
import json
import sys

from executorprocess import ExecutorProcess
from http.server import ThreadingHTTPServer
from http.server import SimpleHTTPRequestHandler
from dispatcher import Dispatcher
from order import Order
import logging

def app_init(batch_size):
    logging.basicConfig(filename='app.log',
                        filemode='w',
                        level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s - %(message)s')
    logging.info("app init started ...")
    respQ = mp.Queue()
    reqQ = mp.Queue()
    OrderHTTPHandler.dispatcher = Dispatcher(reqQ, respQ)
    executer_process = ExecutorProcess(reqQ, respQ, batch_size)
    executer_process.start()


def server_init():
    server = ThreadingHTTPServer(('localhost', 8080), OrderHTTPHandler)
    server.serve_forever()


class OrderHTTPHandler(SimpleHTTPRequestHandler):

    dispatcher = None

    def do_POST(self):
        dispatcher = OrderHTTPHandler.dispatcher
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        http_data = self.rfile.read(int(self.headers['Content-Length']))
        req_order_data = json.loads(http_data)
        req_order = Order.order_decoder(req_order_data)
        dispatcher.send_request(req_order)
        resp_order = dispatcher.get_response_blocking()
        resp_order_data = json.dumps(resp_order.__dict__)
        self.wfile.write(resp_order_data.encode())


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("wrong number of command line arguments !!! need batch size ...")
    batch_size_str = sys.argv[1]
    app_init(int(batch_size_str))
    server_init()
