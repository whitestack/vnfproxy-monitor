import sys
sys.path.append('lib')

import time
from charmhelpers.core.hookenv import (config, log)

from charms.reactive import (when, hook)
from charms.reactive.flags import (clear_flag)
from vnf_db import insert_instance, db, get_last_instance
from vnf_performance import scale_out
from vnf_util import dump_config, dump_environment


@when('scaling.in')
def update_status():
    log('================== VNFPROXY-MONITOR.SCALE-IN')

    clear_flag('scaling.out')
    clear_flag('scaling.in')


@when('scaling.out')
def update_status():
    log('================== VNFPROXY-MONITOR.SCALE-OUT')
    try:
        cfg = config()
        log(cfg)
        osm_so_ip = cfg['osm-so-ip']
        osm_so_username = cfg['osm-so-username']
        osm_so_password = cfg['osm-so-password']
        osm_nsr_ref_id = cfg['osm-nsr-ref-id']
        osm_scaling_group_name = cfg['osm-scaling-group-name']
        scale_out(osm_so_ip, osm_so_username, osm_so_password, osm_nsr_ref_id, osm_scaling_group_name)
    except Exception as e:
        log('Scaling Out failed:' + str(e), level='ERROR')

    clear_flag('scaling.out')


@hook('update-status')
def hook_update_status():
    try:
        log('================== VNFPROXY-MONITOR.UPDATE-STATUS')
        dump_config()
        dump_environment()

        for i in db.all():
             log("Before #%d: %s" %(i.doc_id, i))

        last = get_last_instance()
        if last:
            log("Last #%d %s " % (last.doc_id, last))

        insert_instance({
                'id': int(time.time()) - 1461024000
            })

        for i in db.all():
            log("After   #%d: %s" % (i.doc_id, i))

    except Exception as e:
        log('Update Status failed:' + str(e), level='ERROR')




@hook('start')
def hook_start():
    log('================== VNFPROXY-MONITOR.HOOK.START')
    dump_config()
    dump_environment()


@when('actions.start')
def action_start():
    log('================== VNFPROXY-MONITOR.ACTION.START')
    dump_config()
    dump_environment()
