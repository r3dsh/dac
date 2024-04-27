import networkx as nx

from gitstore.graph.model import Manifest


class ManifestsGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.kind_aliases = {
            "deployment": "Deployment",
            "deploy": "Deployment",
            "dep": "Deployment",
            # Add more aliases as needed
        }

    def add_manifest(self, manifest: Manifest):
        """
        Add a manifest to the Kubernetes manifests graph.

        Args:
        - manifest (Manifest): The manifest to add.
        """
        self.graph.add_node(manifest.metadata.name, manifest=manifest)

    def load_graph(self, file_path):
        """
        Load the Kubernetes manifests graph from a file.

        Args:
        - file_path (str): The path to the file containing the graph data.
        """
        self.graph = nx.read_gpickle(file_path)

    def save_graph(self, file_path):
        """
        Save the Kubernetes manifests graph to a file.

        Args:
        - file_path (str): The path to save the graph data.
        """
        nx.write_gpickle(self.graph, file_path)

    def get_pods_in_namespace(self, namespace):
        """
        Get all pods running in the given namespace.

        Args:
        - namespace (str): The namespace to filter pods.

        Returns:
        - list: A list of pod names running in the given namespace.
        """
        pods = []
        for node, data in self.graph.nodes(data=True):
            manifest = data['manifest']
            if manifest.kind == "Pod" and manifest.metadata.namespace == namespace:
                pods.append(manifest.metadata.name)
        return pods

    def get_kind_in_namespace(self, namespace, kinds):
        """
        Get all resources of the specified kinds running in the given namespace.

        Args:
        - namespace (str): The namespace to filter resources.
        - kinds (list): A list of resource kinds or aliases to retrieve.

        Returns:
        - dict: A dictionary mapping resource kinds to lists of resource names of that kind running in the given namespace.
        """
        resources = {kind: [] for kind in kinds}
        for node, data in self.graph.nodes(data=True):
            manifest = data['manifest']
            if manifest.metadata.namespace == namespace:
                for kind in kinds:
                    real_kind = self.kind_aliases.get(kind, kind)  # Get real kind or use original kind if not aliased
                    if manifest.kind == real_kind:
                        resources[kind].append(manifest.metadata.name)
        return resources

    def get_resources_in_namespace(self, namespace):
        """
        Get all resources running in the given namespace.

        Args:
        - namespace (str): The namespace to filter resources.

        Returns:
        - dict: A dictionary containing lists of resource names for each resource kind.
        """
        resources = {}
        for node, data in self.graph.nodes(data=True):
            manifest = data['manifest']
            if manifest.metadata.namespace == namespace:
                resources.setdefault(manifest.kind, []).append(manifest.metadata.name)
        return resources

    def find_orphaned_resources(self):
        """
        Find orphaned resources in the Kubernetes manifests graph.

        Returns:
        - list: A list of orphaned resource names.
        """
        used_resources = set()
        all_resources = set()

        # Get all resource names
        for node, data in self.graph.nodes(data=True):
            all_resources.add(data['manifest'].metadata.name)

        # Get names of resources that are used
        for node, data in self.graph.nodes(data=True):
            manifest = data['manifest']
            if manifest.kind != "Pod":  # Exclude pods from the check
                for neighbor in self.graph.neighbors(node):
                    used_resources.add(neighbor)

        # Find orphaned resources
        orphaned_resources = all_resources - used_resources
        return list(orphaned_resources)

    def find_services_exposed_by_deployments(self):
        """
        Find services exposed by deployments in the Kubernetes manifests graph.

        Returns:
        - dict: A dictionary mapping deployment names to lists of service names they expose.
        """
        services_exposed_by_deployments = {}

        for node, data in self.graph.nodes(data=True):
            manifest = data['manifest']
            if manifest.kind == "Deployment":
                deployment_name = manifest.metadata.name
                services_exposed_by_deployments[deployment_name] = []

                # Find services exposed by this deployment
                for neighbor in self.graph.neighbors(node):
                    neighbor_manifest = self.graph.nodes[neighbor]['manifest']
                    if neighbor_manifest.kind == "Service":
                        services_exposed_by_deployments[deployment_name].append(neighbor_manifest.metadata.name)

        return services_exposed_by_deployments
