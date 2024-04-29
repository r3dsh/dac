import importlib

from contextlib import redirect_stdout

from dac import logging
from dac.manifest import Manifest, ManifestParser  # noqa
from dac.manifest import CustomResourceDefinitionSpec, CustomResourceDefinitionNames

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.info("parsing manifests")

mp = ManifestParser(["../api", "../manifests", "../manifests2"])
manifests = mp.load_all()

# Process CustomResourceDefinitions first
resource_definitions = {
    None: {},  # Global space (when namespace was not specified)
}

log.info("mapping custom resource definitions")
for crd_node in mp.graph.get_resources_kind("CustomResourceDefinition"):
    crd_spec = CustomResourceDefinitionSpec(**crd_node.spec)

    names = CustomResourceDefinitionNames(**crd_spec.Names)
    if not names.ShortNames:
        names.ShortNames = []
    all_names = [names.Kind, names.Plural, names.Singular] + names.ShortNames

    if crd_node.metadata.namespace not in resource_definitions:
        resource_definitions[crd_node.metadata.namespace] = {}

    for spec_ver in crd_spec.Versions:
        api_group = f"{crd_spec.Group}/{spec_ver.Name}"

        if api_group not in resource_definitions[crd_node.metadata.namespace]:
            resource_definitions[crd_node.metadata.namespace][api_group] = {}

        if names.Kind not in resource_definitions[crd_node.metadata.namespace][api_group]:
            resource_definitions[crd_node.metadata.namespace][api_group][names.Kind] = crd_node

kinds = []
kind_handlers = {}

log.info("hitting validate on every handler that will be used by manifests and building handlers map")
for ns in resource_definitions:
    for apiExt in resource_definitions[ns]:
        # if ns is None:
        #     print(f"global ({apiExt}) CRDs (count {len(resource_definitions[None][apiExt])}):")
        # else:
        #     print(f"namespace '{ns}' ({apiExt}) CRDs (count {len(resource_definitions[ns][apiExt])}):")

        for cr in resource_definitions[ns][apiExt]:
            ccr = resource_definitions[ns][apiExt][cr]
            for cver in ccr.spec['versions']:

                if "builtin" in cver['schema']:
                    # TODO: consider if should be exposed to client side
                    module_name = "api." + ccr.metadata.name

                    file_path = cver['schema']["builtin"]["name"]
                    spec = cver['schema']["builtin"]["spec"]

                    import sys

                    # This helps us in two ways:
                    # - we get free logs from imported handlers
                    # - host app stdout/stderr is not polluted by handlers
                    #
                    with open('/tmp/foooo.txt', 'w') as f:  # On Unix-like systems, this will discard the output
                        with redirect_stdout(f):

                            sys.path.append("../api/" + ccr.metadata.name)
                            module = importlib.import_module(f"{cver['name']}.{file_path}")

                            if "validate" not in dir(module):
                                log.warning(
                                    "DEPRECATION WARNING! Handlers will be required to have 'validate' function that "
                                    "will process and validate the spec.")
                                # TODO: remove assigning handlers with missing validation function
                                kind_handlers[cr] = module.handle
                            else:
                                if module.validate(spec):
                                    kind_handlers[cr] = module.handle
                                else:
                                    log.error("VALIDATION ERROR!!!!!!!")

                    # unsilence command-line output
                    sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__

            kinds.append(cr)

log.info(f"cluster available kinds: {', '.join(kinds)}")
log.info("executing manifests:")

for ns_name in manifests:
    namespace = manifests[ns_name]
    for man_name in namespace:
        # manifest = Manifest(**namespace[man_name])
        manifest = namespace[man_name]
        # CRDs are already processed, so we skip here
        if manifest.kind != 'CustomResourceDefinition':
            if manifest.kind in kind_handlers:
                log.debug(
                    f"invoking handler for manifest: {manifest.metadata.namespace} {manifest.kind} {manifest.metadata.name})")
                result = kind_handlers[manifest.kind](manifest.spec)
                log.info(f"handler invocation result: {kind_handlers[manifest.kind](manifest.spec)}")
            else:
                log.warning(f"no supported handler for kind {manifest.kind}")

# print("KIND HANDLERS:", kind_handlers)
