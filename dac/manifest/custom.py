import json

from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Dict, Any


class CustomResourceVersion(BaseModel):
    Name: str = Field(default=None, alias='name')
    Served: bool = Field(default=False, alias='served')
    Storage: bool = Field(default=False, alias='storage')
    Schema: Optional[Any] = Field(default=None, alias='schema')


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
    Type: str
    Properties: Optional[Dict[str, str]] = None


# Example usage
custom_resource_yaml = """
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          name:
            type: string
          schedule:
            type: string
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
"""

custom_resource_yaml2 = """
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  versions: []
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
"""

custom_resource_yaml3 = """
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: patching.nighlty.example.com
spec:
  group: nighlty.example.com
  versions:
    - name: v1
      served: true
      storage: true
  scope: Namespaced
  names:
    plural: patchings
    singular: patching
    kind: Patching
    shortNames:
    - pt
    # categories is a list of grouped resources the custom resource belongs to.
    categories:
    - all
"""

import yaml

for cry in [custom_resource_yaml, custom_resource_yaml2, custom_resource_yaml3]:
# for cry in [custom_resource_yaml3]:
    custom_resource_data = yaml.safe_load_all(cry)

    for resource_data in custom_resource_data:
        # crd = CustomResourceDefinition(**resource_data)
        print(resource_data)
        try:
            crd = CustomResourceDefinition(**resource_data)
            print(crd)
            print(crd.Spec.Versions)
        except ValidationError as e:
            print(e)

        # print(json.dumps(custom_resource, indent=4))
