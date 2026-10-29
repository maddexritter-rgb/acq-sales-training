#!/bin/sh
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
task_cache=${SALES_COACH_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/sales-call-audit-local}
mkdir -p "$task_cache/tools"
if command -v uv >/dev/null 2>&1; then
    task_uv=$(command -v uv)
elif [ -x "$task_cache/tools/uv" ]; then
    task_uv="$task_cache/tools/uv"
else
    case " $* " in *' --offline '*) echo 'Offline setup unavailable: run online once first.' >&2; exit 1;; esac
    echo 'Preparing local tools. No account or API key needed.'
    installer="$task_cache/tools/uv-installer.sh"
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL --retry 2 https://astral.sh/uv/0.11.8/install.sh -o "$installer"
    elif command -v wget >/dev/null 2>&1; then
        wget -q https://astral.sh/uv/0.11.8/install.sh -O "$installer"
    else
        echo 'This computer needs curl or wget to download its local runtime.' >&2; exit 1
    fi
    UV_UNMANAGED_INSTALL="$task_cache/tools" sh "$installer"
    task_uv="$task_cache/tools/uv"
fi
export PATH="$(dirname "$task_uv"):$PATH"
export UV_PYTHON_INSTALL_DIR="$task_cache/python"
if [ "${1:-}" = '--install' ]; then
    shift
    exec "$task_uv" run --no-project --python 3.11 "$script_dir/install_skill.py" "$@"
fi
case " $* " in
    *' --offline '*)
        exec "$task_uv" --offline run --no-project --python 3.11 "$script_dir/run_local_audio.py" "$@" --cache "$task_cache";;
    *) exec "$task_uv" run --no-project --python 3.11 "$script_dir/run_local_audio.py" "$@" --cache "$task_cache";;
esac
