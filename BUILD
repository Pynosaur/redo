genrule(
    name = "redo_bin",
    srcs = glob(["app/**/*.py", "doc/**/*.yaml"]),
    outs = ["redo"],
    cmd = """
        /opt/homebrew/bin/nuitka \
            --onefile \
            --include-data-dir=doc=doc \
            --onefile-tempdir-spec=/tmp/nuitka-redo \
            --no-progressbar \
            --assume-yes-for-downloads \
            --no-deployment-flag=self-execution \
            --output-dir=$$(dirname $(location redo)) \
            --output-filename=redo \
            $(location app/main.py)
    """,
    local = 1,
    visibility = ["//visibility:public"],
)
