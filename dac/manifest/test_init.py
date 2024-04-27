import networkx as nx
from dac.manifest import Manifest, Metadata


def test_init(graph_path):
    # Example manifests
    manifest1 = Manifest(
        apiVersion="v1",
        kind="Pod",
        metadata=Metadata(name="pod1", namespace="namespace2", labels={"app": "frontend", "env": "production"}),
        spec={}
    )
    manifest2 = Manifest(
        apiVersion="v1",
        kind="Pod",
        metadata=Metadata(name="pod2", namespace="namespace1", labels={"app": "frontend", "env": "staging"}),
        spec={}
    )
    manifest3 = Manifest(
        apiVersion="v1",
        kind="Service",
        metadata=Metadata(name="service1", namespace="namespace1", labels={"app": "frontend", "env": "production"}),
        spec={}
    )
    manifest4 = Manifest(
        apiVersion="v1",
        kind="Service",
        metadata=Metadata(name="service2", namespace="namespace2", labels={"app": "backend", "env": "production"}),
        spec={}
    )
    # Additional pods in namespace1
    manifest5 = Manifest(
        apiVersion="v1",
        kind="Pod",
        metadata=Metadata(name="pod3", namespace="namespace2", labels={"app": "frontend", "env": "testing"}),
        spec={}
    )
    manifest6 = Manifest(
        apiVersion="v1",
        kind="Pod",
        metadata=Metadata(name="pod4", namespace="namespace1", labels={"app": "frontend", "env": "testing"}),
        spec={}
    )

    # Additional deployments in namespace1
    manifest7 = Manifest(
        apiVersion="apps/v1",
        kind="Deployment",
        metadata=Metadata(name="deployment3", namespace="namespace2", labels={"app": "frontend", "env": "testing"}),
        spec={}
    )
    manifest8 = Manifest(
        apiVersion="apps/v1",
        kind="Deployment",
        metadata=Metadata(name="deployment4", namespace="namespace1", labels={"app": "frontend", "env": "testing"}),
        spec={}
    )

    # Additional services in namespace1
    manifest9 = Manifest(
        apiVersion="v1",
        kind="Service",
        metadata=Metadata(name="service3", namespace="namespace1", labels={"app": "frontend", "env": "testing"}),
        spec={}
    )
    manifest10 = Manifest(
        apiVersion="v1",
        kind="Service",
        metadata=Metadata(name="service4", namespace="namespace2", labels={"app": "frontend", "env": "testing"}),
        spec={}
    )

    # Create a graph
    graph = nx.Graph()

    # Add nodes
    for manifest in [manifest1, manifest2, manifest3, manifest4]:
        graph.add_node(manifest.metadata.name, manifest=manifest)

    # Add additional manifests to the graph
    additional_manifests = [manifest5, manifest6, manifest7, manifest8, manifest9, manifest10]
    for manifest in additional_manifests:
        graph.add_node(manifest.metadata.name, manifest=manifest)

    # Connect nodes based on label and namespace matches
    for node1, data1 in graph.nodes(data=True):
        for node2, data2 in graph.nodes(data=True):
            if node1 != node2:
                if data1['manifest'].metadata.namespace == data2['manifest'].metadata.namespace:
                    for label in data1['manifest'].metadata.labels:
                        if label in data2['manifest'].metadata.labels and data1['manifest'].metadata.labels[label] == \
                                data2['manifest'].metadata.labels[label]:
                            graph.add_edge(node1, node2)

    nx.write_gpickle(graph, graph_path)
