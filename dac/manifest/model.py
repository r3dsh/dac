from typing import Optional, Dict, Any, List

from pydantic import BaseModel, PrivateAttr, Field


class Metadata(BaseModel):
    name: str
    namespace: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
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


class CustomResourceVersion(BaseModel):
    Name: str = Field(default=None, alias='name')
    Served: bool = Field(default=False, alias='served')
    Storage: bool = Field(default=False, alias='storage')
    Schema: Optional[Any] = Field(default=None, alias='schema')


class CustomResourceDefinitionNames(BaseModel):
    Plural: str = Field(default=None, alias='plural')
    Singular: str = Field(default=None, alias='singular')
    Kind: str = Field(default=None, alias='kind')
    ShortNames: List[str] = Field(default=None, alias='shortNames')


class CustomResourceDefinitionSpec(BaseModel):
    Group: str = Field(default=None, alias='group')
    Versions: List[CustomResourceVersion] = Field(default=None, alias='versions')
    Scope: str = Field(default=None, alias='scope')
    Names: dict = Field(default=None, alias='names')


class CustomResourceDefinition(BaseModel):
    ApiVersion: str = Field(default=None, alias='apiVersion')
    Kind: str = Field(alias='kind')
    Metadata: dict = Field(alias='metadata')
    Spec: CustomResourceDefinitionSpec = Field(alias='spec')


class OpenAPIV3Schema(BaseModel):
    # Define the schema fields here, this is just a draft
    Type: str = Field(default=None, alias='type')
    Properties: Optional[Any] = Field(default=None, alias='properties')


class BuiltinSchema(BaseModel):
    # Define the schema fields here, this is just a draft
    Name: str = Field(default=None, alias='name')
    Namespace: str = Field(default=None, alias='namespace')
    Spec: Dict[str, str] = Field(alias='spec')


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
