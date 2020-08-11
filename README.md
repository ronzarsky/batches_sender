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
    - consumer context: response batch loop thread (main process dedicated thread)  
  - Response "per source queue" 
    - producer context: response batch loop thread (main process dedicated thread)
    - consumer context: http request handler thread 
 
- Basic modules:
  - main.py (main process)
    - initializes the http server
    - receives post requests from the client 
    - parses the order from the request payload
    - sends the request via dispatcher api 
    - consumes the response from the "per source queue" via dispatcher api 
    - once the response order has arrived it is sent to the client within the http response body
    
  - dispatcher.py 
    - request sending api
      - send_request api: produces orders via dedicated queue 
      - orders are consumed by the executionprocessor (described below)
      - it appends some metadata to each order
      - this metadata is used later on to dispatch the response back to the client after order execution
    - response batch consumer loop thread (spawned by main process)
      - consumes response batches from the response batch queue
      - produces individual orders to a "per source queue"
    - individual response dispatching
      - the "response batch consumer thread" divides the response into inidividual response orders
      - each order is sent to the appropriate "per source" queue
    
  - executorprocess (a dedicated process)
    - consumes the orders that are produced by the http handler context
    - waits for enough orders to arrive
    - executes all orders that arrived
    - produces executed orders to the "response batch queue"
    
    
    
    
    
    
    
    
