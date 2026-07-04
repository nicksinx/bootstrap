# Project intake files

Store per-product intake YAML while the operator or Cursor agent completes the `bootstrap-okf-forge-project` workflow.

**Operator guide:** `docs/new-okf-forge-project-standup.md` (canonical) · `docs/new-okf-forge-project-standup-offline.md` (notes app export)

## Express path (recommended)

```bash
scripts/project-intake quick \
  --project-id my-product \
  --target-dir "$HOME/projects/my-product" \
  --purpose "Why this product exists." \
  --owner platform-team

scripts/project-intake validate intake/my-product.yaml
scripts/project-intake apply intake/my-product.yaml --execute
```

## Full init path

```bash
scripts/project-intake init --project-id my-product --target-dir ./out/my-product -o intake/my-product.yaml
# edit intake/my-product.yaml
scripts/project-intake validate intake/my-product.yaml
scripts/project-intake apply intake/my-product.yaml --execute
```

Committed intake files are optional; the launched product keeps a copy at `.okf/project-intake.yaml`.
