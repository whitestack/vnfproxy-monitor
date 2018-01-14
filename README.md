# vnfproxy-monitor

This layer adds to a VNF Proxy Charm the functionality to monitor VNF
performance metrics, and invoke OSM scaling API in case trhesholds are
met

## Usage

Add this layer to your charm's `layer.yaml`:

```
includes:
 - layer:vnfproxy-monitor
```

## How it works?

This layer implements metrics retrieval as reaction to three different 
events:

### update-status
This layer adds a reactive handler for the update-status hook, that is 
called periodically form the controller. 

In this handler some basic performance commands are run in the VNF in
order to get performance metrics (at the moment we use vmstat as very 
first attempt to get CPU and Memory metrics, other will be add in the 
future)

If metrics reach the defined tresholds, two states are set
- scaling.in
- scaling.out

You can implement reactive code to this states in yor charm code.

You will see this invocation in juju debug-logs

Unfortunately, the update-status hook runs in a restrictive context that
prevents to save metrics for juju metrics.

###  collect-metrics
When this hook is invoked, metrics are retrieved, but only to add them 
in the controller pool.
No scaling decisions are made.

You WILL NOT see this invocation in juju debug-logs.

** Support for collect-metrics is EXPERIMENTAL and under development **

###  action: getvnfmetric
This layer adds a reactive handler for the getvnfmetric action.
When action getvnfmetric is ran, metrics are retrieved.
In this case no metrics are added, or scaling decisions are made.
(For now this is for testing purposes)

You will see this invocation in juju debug-logs

** Support for actions is EXPERIMENTAL and under development **

## Timers

*update-status* interval is adjustable, by invoking
```
$ juju model-config update-status-hook-interval=30s
$ juju model-config update-status-hook-interval
30s
```
in the controller model.
Acceptable intervals are for example, 30s, 2m, etc

## Reactive code for Scaling
If the layer detect that conditions for scalign are met, it will 
set the proper state
- scaling.in
- scaling.out

You can react to those states, by implementing the reactive code in your charm

A very basic example will be
```python
from charms.reactive import when, when_not, set_state, clear_flag
from charmhelpers.core.hookenv import log

. . .

@when('scaling.in')
def update_status():
    log('VNF.SCALE-IN')
    # Do whatever is required for scaling in (eg. invoke OSM api)
    clear_flag('scaling.in')


@when('scaling.out')
def update_status():
    log('VNF.SCALE-OUT')
    # Do whatever is required for scaling out (eg. invoke OSM api)
    clear_flag('scaling.out')
```

## References
* https://jujucharms.com/docs/stable/developer-getting-started