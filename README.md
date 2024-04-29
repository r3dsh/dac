
# DAC

Output from examples/invoking_crds.py

```shell
INFO: 2024-04-29 07:52:48,842 __main__ parsing manifests
DEBUG: 2024-04-29 07:52:48,842 dac.manifest.parser available directories ['../api', '../manifests', '../manifests2']
DEBUG: 2024-04-29 07:52:48,842 dac.manifest.parser searching in ../api
DEBUG: 2024-04-29 07:52:48,864 dac.manifest.parser adding clients.dac.r3d.sh to namespace homelab
DEBUG: 2024-04-29 07:52:48,886 dac.manifest.parser adding store.dac.r3d.sh to namespace None
DEBUG: 2024-04-29 07:52:48,974 dac.manifest.parser searching in ../manifests
DEBUG: 2024-04-29 07:52:48,990 dac.manifest.parser adding cronjobs.dac.r3d.sh to namespace None
DEBUG: 2024-04-29 07:52:48,997 dac.manifest.parser adding crontabs.dac.r3d.sh to namespace None
DEBUG: 2024-04-29 07:52:49,003 dac.manifest.parser adding test to namespace homelab
DEBUG: 2024-04-29 07:52:49,038 dac.manifest.parser adding orders.acme.cert-manager.io to namespace None
DEBUG: 2024-04-29 07:52:49,044 dac.manifest.parser adding test to namespace homelab
DEBUG: 2024-04-29 07:52:49,061 dac.manifest.parser adding slot_generator to namespace emb_dev
DEBUG: 2024-04-29 07:52:49,067 dac.manifest.parser adding slot_generator to namespace emb_dev
DEBUG: 2024-04-29 07:52:49,079 dac.manifest.parser adding kafka_monthly to namespace emb_dev
DEBUG: 2024-04-29 07:52:49,080 dac.manifest.parser adding kafka_servers to namespace emb_test
DEBUG: 2024-04-29 07:52:49,091 dac.manifest.parser adding STRING to namespace default
DEBUG: 2024-04-29 07:52:49,100 dac.manifest.parser adding STRING to namespace default
DEBUG: 2024-04-29 07:52:49,427 dac.manifest.parser adding STRING to namespace default
DEBUG: 2024-04-29 07:52:49,428 dac.manifest.parser searching in ../manifests2
INFO: 2024-04-29 07:52:49,428 dac.manifest.graph connecting nodes
INFO: 2024-04-29 07:52:49,428 __main__ mapping custom resource definitions
INFO: 2024-04-29 07:52:49,428 __main__ hitting validate on every handler that will be used by manifests and building handlers map
WARNING: 2024-04-29 07:52:49,469 __main__ DEPRECATION WARNING! Handlers will be required to have 'validate' function that will process and validate the spec.
INFO: 2024-04-29 07:52:49,519 __main__ cluster available kinds: Secret, CronJob, CronTab, Order, HttpClient
INFO: 2024-04-29 07:52:49,519 __main__ executing manifests:
DEBUG: 2024-04-29 07:52:49,519 __main__ invoking handler for manifest: homelab Secret test)
INFO: 2024-04-29 07:52:49,519 __main__ handler invocation result: {'foo': 'secret_bar'}
WARNING: 2024-04-29 07:52:49,519 __main__ no supported handler for kind STRING
DEBUG: 2024-04-29 07:52:49,519 __main__ invoking handler for manifest: emb_dev HttpClient slot_generator)
INFO: 2024-04-29 07:52:49,520 __main__ handler invocation result: CIACH
WARNING: 2024-04-29 07:52:49,520 __main__ no supported handler for kind Patching
WARNING: 2024-04-29 07:52:49,520 __main__ no supported handler for kind Server
          v1.secret ZOMMMMM {'url': 'http://localhost', 'method': 'GET', 'cookie': {'refSecret': 'test-cookie'}}
          v1.secret ZOMMMMM {'url': 'http://localhost', 'method': 'GET', 'cookie': {'refSecret': 'test-cookie'}}
          v1.http ZOMMMMM {'ref': 'kafka_servers', 'url': 'https://ifconfig.me/', 'command': '/all.json'}
          v1.http ZOMMMMM {'ref': 'kafka_servers', 'url': 'https://ifconfig.me/', 'command': '/all.json'}

Process finished with exit code 0
```