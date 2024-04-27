import copy
import logging
import os
from pathlib import Path

import yaml
from fastapi import HTTPException, APIRouter

log = logging.getLogger()


class ManifestParser:
    def __init__(self, dir_paths):
        self.dir_paths = dir_paths
        self.manifests = {}
        self.manifests_map = {}
        self.manifest_files = {}

    def load_all(self):
        for dir_path in self.dir_paths:
            for path in Path(dir_path).rglob('*.y*ml'):
                # print("FOUND MANIFEST:", str(path))

                file_path = path.name.replace(dir_path + os.sep, '')
                file_path = "/".join([dir_path, file_path])

                self.manifest_files[file_path] = {'path': file_path, 'file': self.load(path)}
        return self.manifests

    def load(self, file_path):
        log.info(f"loading: {file_path}")

        with open(file_path, 'r') as file:
            return self.parse_manifest(file)

    def parse_manifest(self, file):
        # TODO: Handle invalid manifests and corrupted yaml files!
        # TODO: Handle invalid manifests and corrupted yaml files!
        # TODO: Handle invalid manifests and corrupted yaml files!
        # TODO: Handle invalid manifests and corrupted yaml files!
        for manifest in yaml.safe_load_all(file):
            print(manifest)
            kind = manifest.get('kind')
            if not kind:
                # print("[NOTICE] no supported manifest in", file.name)
                return {}

            metadata = manifest.get('metadata', {})
            namespace = metadata.get('namespace')
            name = metadata.get('name')

            parsed_manifest = {
                'apiVersion': manifest.get('apiVersion'),
                'kind': manifest.get('kind'),
                'metadata': metadata,
                'spec': manifest.get('spec')
            }

            self.manifests_map[name] = parsed_manifest

            if namespace and name:
                self.manifests.setdefault(namespace, {})[name] = parsed_manifest

        return self.manifests

    def route_handlers(self):
        output = {}
        for namespace, manifests in self.manifests.items():
            for name, manifest in manifests.items():
                # print("ROUTING", name, manifest)
                kind = manifest.get('kind')
                if kind:
                    handler_class_name = f"{kind.capitalize()}Handler"
                    handler_class = globals().get(handler_class_name)
                    if handler_class:
                        handler = handler_class(manifest, self.manifests)
                        if namespace not in output:
                            output[namespace] = {}
                        output[namespace][name] = handler.handle()
                        # output.append(handler.handle())
                    else:
                        print(f"Unsupported kind: {kind} (class {handler_class_name} is missing)")
                else:
                    print(f"Manifest {name} in namespace {namespace} does not contain a 'kind' field.")
        return output

    def reload(self):
        self.manifests = {}
        self.manifests_map = {}
        self.manifest_files = {}
        self.load_all()
        print("ManifestParser reloaded")


class Manifest:

    def __init__(self, name: str, manifest_parser: ManifestParser):
        self.name = name
        self.router = APIRouter()
        self.router.add_api_route("/", self.dump_all, methods=["GET"])
        self.router.add_api_route("/{ns}", self.dump_namespace, methods=["GET"])
        self.router.add_api_route("/{ns}/{name}", self.dump_manifest, methods=["GET"])

        self.manifest_parser = manifest_parser
        self.manifests = self.manifest_parser.load_all()

    def custom_json_dump(self, obj, depth=0, max_depth=3):
        if depth >= int(max_depth):
            return str(obj)

        if isinstance(obj, dict):
            return {key: self.custom_json_dump(value, depth + 1, max_depth) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.custom_json_dump(item, depth + 1, max_depth) for item in obj]
        elif hasattr(obj, '__dict__'):
            return self.custom_json_dump(obj.__dict__, depth + 1, max_depth)
        else:
            return obj

    def dump_all(self, max_depth=5, resolve_references: bool = False):
        print(max_depth, resolve_references, self.manifests)
        output = copy.deepcopy(self.manifests)

        # resolving references
        if resolve_references == True:
            for ns in output:
                for name in output[ns]:
                    manifest = output[ns][name]

                    if 'ref' in manifest['spec'] and manifest['spec']['ref'] in self.manifest_parser.manifests_map:
                        print(">>", manifest['spec']['ref'])
                        output[ns][name]['spec']['ref'] = self.manifest_parser.manifests_map[manifest['spec']['ref']]

        return {"Hello": self.custom_json_dump(output, max_depth=max_depth), "parser": self.manifest_parser}

    def dump_namespace(self, ns):
        output = copy.deepcopy(self.manifests)

        if ns not in output:
            raise HTTPException(status_code=404, detail="namespace not found")

        return output[ns]

    def dump_manifest(self, ns, name):
        output = copy.deepcopy(self.manifests)

        if ns not in output:
            raise HTTPException(status_code=404, detail="namespace not found")

        if name not in output[ns]:
            raise HTTPException(status_code=404, detail="manifest not found")

        return output[ns][name]


class Exec:

    def __init__(self, name: str, manifest_parser: ManifestParser):
        self.name = name
        self.router = APIRouter()
        self.router.add_api_route("/{namespace_in}/{name_in}", self.exec, methods=["GET"])
        self.router.add_api_route("/{namespace_in}", self.exec_ns, methods=["GET"])

        self.manifest_parser = manifest_parser
        self.manifests = self.manifest_parser.load_all()

    def exec(self, namespace_in, name_in):
        output = copy.deepcopy(self.manifests)

        if namespace_in not in output:
            raise HTTPException(status_code=404, detail="namespace not found")

        if name_in not in output[namespace_in]:
            raise HTTPException(status_code=404, detail="manifest not found")

        for ns in output:
            for name in output[ns]:
                manifest = output[ns][name]

                if 'ref' in manifest['spec'] and manifest['spec']['ref'] in self.manifest_parser.manifests_map:
                    print(">>", manifest['spec']['ref'])
                    output[ns][name]['spec']['ref'] = self.manifest_parser.manifests_map[manifest['spec']['ref']]

        results = self.manifest_parser.route_handlers()
        for ns in results:
            if ns == namespace_in and name_in in results[ns]:
                return results[ns][name_in]

        return {}

    def exec_ns(self, namespace_in):
        output = copy.deepcopy(self.manifests)

        if namespace_in not in output:
            raise HTTPException(status_code=404, detail="namespace not found")

        for ns in output:
            for name in output[ns]:
                manifest = output[ns][name]

                if 'ref' in manifest['spec'] and manifest['spec']['ref'] in self.manifest_parser.manifests_map:
                    print(">>", manifest['spec']['ref'])
                    output[ns][name]['spec']['ref'] = self.manifest_parser.manifests_map[manifest['spec']['ref']]

        results = self.manifest_parser.route_handlers()
        for ns in results:
            if ns == namespace_in:
                return results[ns]

        return {}
