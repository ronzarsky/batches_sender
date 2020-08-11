import multiprocessing as mp
import executionsdk
import response
import logging

class ExecutorProcess(mp.Process):

    def __init__(self, reqQ, respQ, batch_size):
        super(mp.Process, self).__init__()
        self.reqQ = reqQ
        self.respQ = respQ
        self.batch_size = batch_size

    def get_next_requests_batch(self):
        # TODO: add timeout behavior,
        #   - needed when system is not constantly exhausted with requests
        #   - this could happen a lot: especially, in production temp outages and QA tests

        logging.info("ExecutorProcess.get_batch")
        batch = []
        for _ in range(self.batch_size):
            req = self.reqQ.get()
            logging.info("ExecutorProcess.get_batch req: %s", req.order.order)
            batch.append(req)

        return batch

    def process_next_requests_batch(self):
        req_batch = self.get_next_requests_batch()
        orders = [req.order for req in req_batch]
        executed_orders = executionsdk.ExecutionSdk.execute_orders(orders)
        resp_batch = []
        for i in range(len(executed_orders)):
            req = req_batch[i]
            executed_order = executed_orders[i]
            resp_batch.append(response.Response(executed_order, req.req_src))

        self.respQ.put(resp_batch)

    def run(self):
        while True:
            self.process_next_requests_batch()

