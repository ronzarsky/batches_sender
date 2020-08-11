import multiprocessing as mp
import json

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
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        http_data = self.rfile.read(int(self.headers['Content-Length']))
        req_order_data = json.loads(http_data)
        req_order = Order.order_decoder(req_order_data)
        OrderHTTPHandler.dispatcher.send_request(req_order)
        resp_order = OrderHTTPHandler.dispatcher.get_response_blocking()
        resp_order_data = json.dumps(resp_order.__dict__)
        self.wfile.write(resp_order_data.encode())


if __name__ == '__main__':
    app_init(2)
    server_init()
