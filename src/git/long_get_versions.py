
def get_versions():
    # I am in _version.py, which lives at ROOT/VERSIONFILE_SOURCE. If we have
    # __file__, we can work backwards from there to the root. Some
    # py2exe/bbfreeze/non-CPython implementations don't do __file__, in which
    # case we can only use expanded keywords.

    cfg = get_config()
    verbose = cfg.verbose
    ver = git_versions_from_keywords(get_keywords(), cfg.tag_prefix, verbose)
    if ver:
        return ver

    try:
        root = os.path.realpath(__file__)
        # versionfile_source is the relative path from the top of the source
        # tree (where the .git directory might live) to this file. Invert
        # this to find the root from __file__.
        for i in cfg.versionfile_source.split('/'):
            root = os.path.dirname(root)
    except NameError:
        return {"version": "0+unknown", "full-revisionid": None,
                "dirty": None,
                "error": "unable to find root of source tree"}

    return (git_versions_from_vcs(cfg.tag_prefix, root, verbose)
            or versions_from_parentdir(cfg.parentdir_prefix, root, verbose)
            or {"version": "0+unknown", "full-revisionid": None,
                "dirty": None,
                "error": "unable to compute version"})
