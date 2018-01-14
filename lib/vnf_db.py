import sys
sys.path.append('lib')

from tinydb import TinyDB, Query
from charmhelpers.core.hookenv import (
    config,
    log,
    hook_name, action_name, action_tag)

db = TinyDB('/tmp/instances.json')
User = Query()


def insert_instance(instance):
    if 'id' not in instance:
        raise Exception('Instance with no id')

    db.insert(
        {
            "instance": instance
        }
    )


def get_instances():
    return [i for i in db.all()]


def get_last_instance():
    n = len(db)
    if n > 0:
        return db.all()[n-1]
    else:
        return None


def remove_instance(id):
    o = db.search(User.instance.id == id)
    if not o:
        print("Instance %d Not found" % id)
        return

    db.remove(doc_ids=[o[0].doc_id])


def test_db():
    for i in range(0,10):
        insert_instance({
            'id': i
        })

    while True:
        log("\"-----------\nBefore\"")
        for i in db.all():
            log("Object #%d: %s" %(i.doc_id, i))

        last = get_last_instance()
        if not last:
            break

        log("Last: %s " %  last)
        remove_instance(last['instance']['id'])
        remove_instance(1000)

        log("After")
        for i in db.all():
            log("Object #%d: %s" %(i.doc_id, i))
