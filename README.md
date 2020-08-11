# batches_sender
- Batch Sender project
  - sends orders in batches to executor
  - the batch size is configurable via command line argument
  
- Basic libraries
  - multiprocessing: for processes and queues
  - http.server.ThreadingHTTPServer: for concurrent http requests handling
  - logging: for audit and debug
  - json: for deserializing/serializing http requests/response

- Basic data structures:
  - Requests queue
    - producer context: http request handler thread
    - consumer context: execution process
  - Response batch queue:
    - producer context: execution process
    - consumer context: main process dedicated thread  
  - Response "per source queue" 
    - producer context: main process dedicated thread  
    - consumer context: http request handler thread 
 
- Basic modules:
  - main.py (main process)
    - initializes the http server
    - receives post requests from the client 
    - parses the order from the request payload
    - sends the request via dispatcher api 
    - blocks on the "per source" response queue via dispatcher api 
    - once the response order has arrived it is send to the client within the http response body
    
  - dispatcher.py
    - request sending
      - send_request api: produces orders using to a dedicated queue 
      - these orders are consumed later on by the executionprocessor (described below)
      - it appends some metadata to each order
      - this metadata is used later on to dispatch the response after order execution
    - delivering response back to http handler context
      - consumes response batches from the response batch queue
      - produces individual orders to a "per source" queue
  
  - executorprocess (a dedicated process)
    - consumes the orders that are produces from the http handler context
    - waits for enough orders to arrive
    - executes all orders that arrived
    - produces executed orders to the response batch queue
    
    
    
    
    
    
    
    
