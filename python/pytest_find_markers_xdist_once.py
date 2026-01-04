from _pytest.mark.expression import Expression

def pytest_configure(config: pytest.Config) -> None:
    """Snippet that took me quite some time to craft; can be used with xdist to
    find the markers before tests run -- before fixtures."""
    # We use this hook because it is run on sequential sessions,
    # and both pytest-xdist’s controller and workers
    if "--collect-only" in config.args:
        return  # no need to do work

    is_xdist_worker = hasattr(config, "workerinput")

    mark_expr = config.option.markexpr
    registered_markers = config.getini("markers")
    all_markers = {m.split(':')[0].strip(): True for m in registered_markers}

    slurm_enabled = True
    if mark_expr:
        expression = Expression.compile(mark_expr)
        is_sufficient = expression.evaluate(lambda name: name == "slurm")
        is_possible = expression.evaluate(lambda name: name in all_markers.keys())
        runs_without_slurm = expression.evaluate(lambda name: name != "slurm" and name in all_markers.keys())
        slurm_enabled = is_possible and (is_sufficient or not runs_without_slurm)

    if slurm_enabled:
        if not is_xdist_worker:
            # The xdist controller...
            ssh_port = get_free_port()
            _slurm_container = _start_slurm_container(ssh_port)
            config._slurm_id = container._container.id
            atexit.register(_slurm_container.stop)
