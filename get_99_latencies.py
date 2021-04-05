#!/usr/bin/env  python3

from matplotlib import pyplot as plt
import sys
import os
import json
import time


def get_autoscaler_name():
    # print("Get Autoscaler Name")
    return os.popen("kubectl get pods -n knative-serving | grep autoscaler | grep -v autoscaler-hpa | awk '{}{print $1}{}'").read().split('\n')[0]


def get_env_vars():
    HOST_KEY = os.getenv("INGRESS_HOST")
    if not HOST_KEY:
        sys.stderr.write(
            "export HOST_KEY => export INGRESS_HOST=$(kubectl get po -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].status.hostIP}')")

    PORT_KEY = os.getenv("INGRESS_PORT")

    if not PORT_KEY:
        sys.stderr.write(
            "export PORT_KEY => INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name==\"http2\")].nodePort}')")

    return (HOST_KEY, PORT_KEY)


def get_timestamp():
    autoscaler = get_autoscaler_name()
    timestamp = os.popen("kubectl logs -n knative-serving " + autoscaler +
                         " autoscaler --tail=1 --timestamps=true | awk '{print $1}'").read()
    return timestamp.rstrip()


def run(duration=30):
    timestamp = get_timestamp()
    algos = ["lc", "wfq"]
    for algo in algos:
        if algo == "lc":
            prefix = "lc"
            header = "least-conn-autoscale-go"
        else:
            prefix = "wfq"
            header = "autoscale-go"
        keys = [x for x in range(400, 1300, 100)]
        res = {k: 0 for k in keys}
        logdir = "logs"
        HOST_KEY, PORT_KEY = get_env_vars()
        if not HOST_KEY or not PORT_KEY:
            sys.stderr.write("env vars are not defined")
            sys.exit(1)
        logfile = "{}-99-percentile-latency-{}.log".format(prefix, timestamp)

        for k in keys:
            print("rps =", k)
            cmd = "loadtest -c 10 --rps {} -H \"Host:{}.default.example.com\" http://{}:{}/?prime=10000 -k -t {}".format(
                k, header, HOST_KEY, PORT_KEY, duration)
            print(cmd)
            lines = os.popen(cmd).read()
            for line in lines.split('\n'):
                if line.find("INFO   99%") > -1:
                    ls = line.split()
                    res[k] = int(ls[ls.index("99%") + 1])
            if algo != algos[-1] and k != keys[-1]:
                # ensure all tcp connections from loadtest have closed down
                time.sleep(60)

        j = json.dumps(res)
        with open(logfile, 'w') as l:
            l.write(j)
        print("results are in:", logfile)


"""
    For the graphing the output files created by run() have to be downloaded to a machine that supports graphing
"""


def graph_99_percentile(lc_file, wfq_file):
    wfq = {}
    with open(wfq_file, 'r') as w:
        wfq = json.load(w)
    lc = {}
    with open(lc_file, 'r') as l:
        lc = json.load(l)
    plt.figure(figsize=(15, 10))
    plt.scatter([k for k in wfq.keys()], list(wfq.values()), label="wfq")
    plt.scatter([k for k in lc.keys()], list(lc.values()), label="lc")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        duration = sys.argv[1]
        run(duration)
    else:
        run()
