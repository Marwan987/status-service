#!/usr/bin/python3

import http.server, requests
import datetime as dt
from prometheus_client import start_http_server, Gauge
#from prometheus_api_client import PrometheusConnect

REQUEST_COUNT = Gauge('sample_external_url_up', 'app liveness',['url'])
REQUEST_ELAPSED = Gauge('sample_external_url_response_ms', 'time elapsed for the request to reach server',['url'])
APP_PORT = 8000
METRICS_PORT = 8001
#PROMETHEUS = 'http://127.0.0.1:9090'

#prom = PrometheusConnect()
label_config_req1 = {
   'url': 'https://httpstat.us/503'
}
label_config_req2 = {
   'url': 'https://httpstat.us/200'
}

#Request 1
start_request1 = dt.datetime.now()
response1 = requests.get("https://httpstat.us/503")
end_request1 = dt.datetime.now()
time_delta_request1 = end_request1 - start_request1
response1_time = time_delta_request1.total_seconds()*1000

#Request2
start_request2 = dt.datetime.now()
response2 = requests.get("https://httpstat.us/200")
end_request2 = dt.datetime.now()
time_delta_request2 = end_request2 - start_request2
response2_time = time_delta_request2.total_seconds()*1000

class HandleRequests(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if response1.status_code == 200:
            REQUEST_COUNT.labels('https://httpstat.us/503').set('1')
            REQUEST_ELAPSED.labels('https://httpstat.us/503').set(response1_time)
        else:
            REQUEST_COUNT.labels('https://httpstat.us/503').set('0')
            REQUEST_ELAPSED.labels('https://httpstat.us/503').set(response1_time)
        if response2.status_code == 200:
            REQUEST_COUNT.labels('https://httpstat.us/200').set('1')
            REQUEST_ELAPSED.labels('https://httpstat.us/200').set(response2_time)
        else:
            REQUEST_COUNT.labels('https://httpstat.us/200').set('0')
            REQUEST_ELAPSED.labels('https://httpstat.us/200').set(response2_time)
        self.send_response(200)
        self.send_header("Content-Type", "application/json;charset=UTF-8")
        self.end_headers()

        #query sample_external_url_response_ms
        metric1 =requests.get( 'http://status-service-prometheus-server' + '/api/v1/query', params={'query': 'sample_external_url_response_ms'})
        res1 = bytes(metric1.text, 'utf-8')
        self.wfile.write(res1)

        #query sample_external_url_up
        metric2 = requests.get('http://status-service-prometheus-server' + '/api/v1/query', params={'query': 'sample_external_url_up'})
        res2 = bytes(metric2.text, 'utf-8')
        self.wfile.write(res2)


        self.wfile.close()


if __name__ == "__main__":
    start_http_server(METRICS_PORT)
    server = http.server.HTTPServer(('localhost', APP_PORT), HandleRequests)
    server.serve_forever()
