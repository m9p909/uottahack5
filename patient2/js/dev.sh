#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

cd "$(dirname "$0")"

main() {
  npx esbuild ./scripts/metamask.ts --watch --bundle --outdir=../static
}

main "$@"
