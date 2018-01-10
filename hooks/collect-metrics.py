#!/usr/bin/env python3

# Load modules from $CHARM_DIR/lib
import sys
sys.path.append('lib')

import datetime
from subprocess import check_call
from charmhelpers.core.hookenv import log
from vnf_performance import get_vnf_metrics

log('VNFPROXY-MONITOR.COLLECT-METRICS')

metrics = dict()
try:
    metrics = get_vnf_metrics()
except Exception as e:
    log("Error executing getvfnmetrics: " + e)

try:
    metric_pairs = []
    for metric, value in metrics.items():
        if value:
            metric_pairs.append("%s=%s" % (metric, value))

    if metric_pairs:
        command = ['add-metric']
        command.extend(metric_pairs)
        check_call(command)
except Exception as e:
    log("Error adding metrics: " + e)

try:
    with open("/tmp/collect-metrics.py", "a") as my_file:
        my_file.write(datetime.datetime.now().isoformat())
        my_file.write(metrics)
except Exception as e:
    log("Error creating timestamp: " + e)
