# Project intake files

Store per-product intake YAML here while the operator or Cursor agent completes the `bootstrap-okf-forge-project` workflow.

Example:

```bash
scripts/project-intake init --project-id my-product --target-dir ./out/my-product -o intake/my-product.yaml
# edit intake/my-product.yaml
scripts/project-intake validate intake/my-product.yaml
scripts/project-intake apply intake/my-product.yaml --execute
```

Committed intake files are optional; the launched product keeps a copy at `.okf/project-intake.yaml`.
