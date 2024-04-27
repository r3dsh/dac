
# GitStore


# Definitions

## Manifest

Yaml file that complies to interface:
```yaml
apiVersion: foo/v1
kind: ManifestKind
metadata:
  name: bar
spec:
```

## ManifestParser

Parses manifest in its basic (interface) form, and then it executes handlers based on manifest api and kind.

Basic form parsing happens on every kind of manifest, supported or not. Handlers however might not always run (e.g. when handler doesn't exist)

## ManifestHandler

Handler receives fully parsed and ready to use manifest on which it will act upon.

There are three kinds of handlers

### Passive Handlers

Passive handlers do not trigger anything and don't have any external logic. They only hold and adjust configuration.

### Active Handlers

Active handlers use provided information from parsed manifests to execute their logic.

### Custom Resource Handlers

Handlers that allow to define custom resources. Because of the nature of this system, all custom resources are either remote endpoints or containers.

For example:

```yaml
kind: CustomResourceHandler
metadata:
  name: weather
spec:
    kind: Weather
    
```
