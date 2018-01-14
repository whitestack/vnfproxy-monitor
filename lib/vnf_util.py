import sys
sys.path.append('lib')

import os

from charmhelpers.core.hookenv import (
    config,
    log,
    hook_name, action_name, action_tag)


def dump_config():
    try:
        cfg = config()
        log(cfg)
        for key, value in cfg.items():
            log("CONFIG: %s=%s" % (key, value))
    except Exception as e:
        log('Dumping config failed:' + str(e), level='ERROR')


def dump_environment():
    log("HookName: %s" % hook_name())
    log("ActionName: %s" % action_name())
    log("ActionTag: %s" % action_tag())
    log(os.environ)
