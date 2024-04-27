from typing import Dict, Any, Optional

from pydantic import BaseModel, PrivateAttr, Field


class Metadata(BaseModel):
    name: str
    namespace: str
    labels: Dict[str, str]
    annotations: Dict[str, Any] = {}  # Default value is an empty dictionary


class Manifest(BaseModel):
    apiVersion: Optional[str] = None  # Make apiVersion optional
    kind: str = Field(..., pattern="^[A-Za-z]+$")  # Require kind to be non-empty and only alphabetic
    metadata: Metadata
    spec: Any

    _kind: str = PrivateAttr()  # Define a private attribute to hold the overridden kind

    def __init__(self, **data):
        super().__init__(**data)
        self._kind = data.get("kind", "Base")  # Store the overridden kind

    # @property
    # def kind(self):
    #     return self._kind


class PodManifest(Manifest):
    kind: str = "Pod"  # Override kind field for PodManifest
    pass


class ServiceManifest(Manifest):
    kind: str = "Service"  # Override kind field for ServiceManifest
    pass


class DeploymentSpec(BaseModel):
    replicas: int


class DeploymentManifest(Manifest):
    kind: str = "Deployment"  # Override kind field for DeploymentManifest
    spec: DeploymentSpec
