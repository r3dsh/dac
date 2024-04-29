import copy
import os
import yaml
from pathlib import Path
from fastapi import HTTPException, APIRouter

from dac import logging
from dac.manifest.graph import ManifestsGraph

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



class ManifestParser:
    def __init__(self, dir_paths):
        self.dir_paths = dir_paths
        self.manifests = {}
        self.graph = ManifestsGraph()
        self.manifests_map = {}
        self.manifest_files = {}

    def load_all(self):
        log.debug(f"available directories {self.dir_paths}")
        for dir_path in self.dir_paths:
            log.debug(f"searching in {dir_path}")
            for path in Path(dir_path).rglob('*.y*ml'):
                if path.name[0] == "_":
                    continue
                # log.debug(f"FOUND MANIFEST: {str(path)}")

                file_path = path.name.replace(dir_path + os.sep, '')
                file_path = "/".join([dir_path, file_path])

                self.manifest_files[file_path] = {'path': file_path, 'file': self.load(path)}

        # connect the graph
        self.graph.connect()

        return self.manifests

    def load(self, file_path):
        # log.debug(f"loading: {file_path}")

        with open(file_path, 'r') as file:
            return self.parse_manifest(file)

    def parse_manifest(self, file):
        from dac.manifest import Manifest

        for manifest in yaml.safe_load_all(file):
            man = Manifest(**manifest)

            if not man.kind:
                # print("[NOTICE] no supported manifest in", file.name)
                return {}

            # log.warning(f"manifest namespace: {man.metadata.namespace}")
            namespace = "default"
            if man.metadata.namespace:
                namespace = man.metadata.namespace

            # TODO: this here has to be replaced with dac.manifest.graph
            # TODO: this here has to be replaced with dac.manifest.graph
            # TODO: this here has to be replaced with dac.manifest.graph
            # TODO:
            # TODO: right now small1.py somehow depends on two lines below
            # TODO: right now small1.py somehow depends on two lines below
            self.manifests_map[man.metadata.name] = man
            self.manifests.setdefault(namespace, {})[man.metadata.name] = man

            if man.kind != "CustomResourceDefinition":
                man.metadata.namespace = namespace

            log.debug(f"adding {man.metadata.name} to namespace {man.metadata.namespace}")
            self.graph.add_manifest(man)

        return self.manifests

    def reload(self):
        self.graph = ManifestsGraph()
        self.manifests = {}
        self.manifests_map = {}
        self.manifest_files = {}
        self.load_all()
        print("ManifestParser reloaded")
