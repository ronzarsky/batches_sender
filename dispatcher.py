import threading
import request
import multiprocessing as mp
import logging

class Dispatcher():

    def __init__(self, reqQ, respQ):
        self.reqQ = reqQ
        self.respQ = respQ
        self.srcQueues = {}
        self.response_loop_thread = self.init_reponse_loop_thread()
        self.response_loop_thread.start()

    @staticmethod
    def src():
        return threading.get_ident()

    def response_loop(self):
        while True:
            logging.info("Dispatcher.response_loop. waiting...")
            resp_batch = self.respQ.get()
            logging.info("Dispatcher.response_loop, got batch")
            for resp in resp_batch:
                logging.info("Dispatcher.response_loop: %s", resp.order.order)
                self.srcQueues[resp.resp_dst].put(resp.order)

    def init_reponse_loop_thread(self):
        return threading.Thread(target=self.response_loop, args=())

    def get_response_blocking(self):
        src = Dispatcher.src()
        logging.info("Dispatcher.get_resp, src: %s", src)
        resp_order = self.srcQueues[src].get()
        logging.info("Deispatcher.get_resp: %s, status: %s", resp_order.order, resp_order.status)
        return resp_order

    def send_request(self, order):
        src = Dispatcher.src()
        logging.info("Dispatcher.send_request, src: %s, order: %s", src, order.order)
        if self.srcQueues.get(src) is None:
            self.srcQueues[src] = mp.Queue()

        self.reqQ.put(request.Request(order, src))







