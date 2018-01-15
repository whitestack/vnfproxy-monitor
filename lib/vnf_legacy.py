import sys
sys.path.append('lib')

import charms
from charmhelpers.core.hookenv import (
    config,
    log)

from charms.reactive import set_state, clear_flag


def get_vnf_metrics():
    # Get VNF Metrics

    metrics = dict()
    try:
        cmd = ['vmstat', '--one-header', '--active',
               '1', # interval
               '2', # count
              ]
        result, err = charms.sshproxy._run(cmd, keep_alive=True)
        log("Err: " + err)
        lines = result.split('\n')
        for line in lines:
            log("LINE: " + line)

        if len(lines) >= 3:
            cols = lines[1].split()
            vals = lines[3].split()
            for col, val in zip(cols, vals):
                if col == 'us': col = 'cpu_user'
                if col == 'sy': col = 'cpu_system'
                if col == 'id': col = 'cpu_idle'
                if col == 'wa': col = 'cpu_waiting'
                if col == 'st': col = 'cpu_stolen'
                if col == 'free': col = 'mem_free'
                if col == 'buff': col = 'mem_buffers'
                if col == 'cache': col = 'mem_cached'
                if col == 'inact': col = 'mem_inactive'
                if col == 'active': col = 'mem_active'

                log('METRIC: %s=%s' % (col, val))
                metrics[col] = val

    except Exception as e:
        log('Metrics Evaluation failed:' + str(e), level='ERROR')

    return metrics


def evaluate_vnt_metrics(metrics):
    log('evaluate_vnt_metrics')
    log(metrics)
    try:
        cpu_used = 100 - int(metrics['cpu_idle'])
        log('cpu_used: %d' % cpu_used)

        cfg = config()
        log('scaleout_cpu_treshold: %d' % cfg['scaleout_cpu_treshold'])
        log('scalein_cpu_treshold: %d' % cfg['scalein_cpu_treshold'])

        if cpu_used > int(cfg['scaleout_cpu_treshold']):
            set_state('scaling.out')
            clear_flag('scaling.in')
        elif cpu_used < int(cfg['scalein_cpu_treshold']):
            clear_flag('scaling.out')
            set_state('scaling.in')
        else:
            clear_flag('scaling.out')
            clear_flag('scaling.in')
    except Exception as e:
        log('Metrics Evaluation failed:' + str(e), level='ERROR')
        log('Metrics Evaluation failed:' + sys.exc_info(), level='WARN')