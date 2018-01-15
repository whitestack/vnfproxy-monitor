import sys

from release import RELEASE

sys.path.append('lib')

from charmhelpers.core.hookenv import (config, log, status_set, action_fail)
from charms.reactive import (when, hook)
from charms.reactive.flags import (clear_flag)

from vnf_performance import scale_out
from vnf_util import dump_config


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
        osm_so_port = cfg['osm-so-port']

        osm_so_username = cfg['osm-so-username']
        osm_so_password = cfg['osm-so-password']
        osm_nsr_ref_id = cfg['osm-nsr-ref-id']
        osm_scaling_group_name = cfg['osm-scaling-group-name']
        scale_out(osm_so_ip, osm_so_username, osm_so_password, osm_nsr_ref_id, osm_scaling_group_name, port=osm_so_port)
    except Exception as e:
        log('Scaling Out failed:' + str(e), level='ERROR')

    clear_flag('scaling.out')
    clear_flag('scaling.in')


@when('actions.start')
def action_start():
    log('================== VNFPROXY-MONITOR.ACTION.START %s' % RELEASE)
    dump_config()
    # dump_environment()

    try:
        cfg = config()
        if not cfg['ssh-hostname'] or cfg['ssh-hostname'] == '0.0.0.0':
            raise Exception("Invalid ssh-hostname %s" % cfg['ssh-hostname'])

        status_set('active', 'Ready to rock!')

    except Exception as e:
        action_fail(str(e))
        clear_flag('actions.start')
        return


@hook('config-changed')
def hook_config_changes():
    log('================== VNFPROXY-MONITOR.HOOK.CONFIG-CHANGED %s' % RELEASE)
    dump_config()
    try:
        cfg = config()
        if not cfg['ssh-hostname'] or cfg['ssh-hostname'] == '0.0.0.0':
            raise Exception("Invalid ssh-hostname %s" % cfg['ssh-hostname'])

        status_set('active', 'Ready to rock!')

    except Exception as e:
        status_set('blocked', str(e))
        return


@hook('start')
def hook_start():
    log('================== VNFPROXY-MONITOR.HOOK.START %s' % RELEASE)
    status_set('blocked', 'Waiting for Configuration')
    dump_config()
    # dump_environment()


# @hook('update-status')
# def hook_update_status():
#     log('================== VNFPROXY-MONITOR.UPDATE-STATUS %s' % RELEASE)
#     dump_config()
#     dump_environment()





