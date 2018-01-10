from charmhelpers.core.hookenv import (
    action_fail,
    action_set,
    action_get,
    config,
    log,
    add_metric)
from subprocess import check_call

from charms.reactive import (
    when,
    remove_state as remove_flag,
    hook)

import datetime

from vnf_performance import get_vnf_metrics, dump_config, evaluate_vnt_metrics


@hook('update-status')
def update_status():
    log('VNFPROXY-MONITOR.UPDATE-STATUS')

    try:
        metrics = get_vnf_metrics()
        evaluate_vnt_metrics(metrics)
    except Exception as e:
        log("Error executing getvfnmetrics: " + str(e))

    try:
        with open("/tmp/update-status", "a") as my_file:
            my_file.write(datetime.datetime.now().isoformat())
    except Exception as e:
        log("Error creating timestamp: " + str(e))


@when('action.getvfnmetrics')
def action_get_vnf_metrics():
    log('VNFPROXY-MONITOR.ACTION.GET_VNF_METRICS')
    try:
        dump_config()
    except Exception as e:
        log("Error dumping getvfnmetrics: " + str(e))

    try:
        get_vnf_metrics()
    except Exception as e:
        log("Error executing getvfnmetrics: " + str(e))
