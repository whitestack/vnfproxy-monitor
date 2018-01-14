import sys
sys.path.append('lib')

import time
import requests

from charmhelpers.core.hookenv import (
    config,
    log,
    hook_name, action_name, action_tag)

from vnf_db import db


def scale_out(hostname, username, password, nsr, scaline_group, instance, port=443):
    if not instance:
        instance = int(time.time()) - 1461024000

    log("SCALING OUT NSR:%s GROUP:%s ID:%s" % (nsr, scaline_group, instance))

    url = 'https://{}:{}@{}:{}/v1/api/config/ns-instance-config/nsr/{}/scaling-group/{}/instance'.\
        format(username, password, hostname, port,
               nsr, scaline_group)
    data = {
        "instance": [
            {"id": instance}
        ]
    }

    response = requests.post(url, data=data)
    log("Response Code %d" % response.status_code)
    log(response.text)

    if 200 <= response.status_code < 300:
        db.insert({'instance': 'John', 'age': 22})



