"""
Basic Z3 wrapper for simple constraint solving (optional dependency)
"""

from typing import Optional
from crypto_finder.common.logging import log


def check_satisfiable(expr_src: str) -> Optional[bool]:
    """
    Evaluate a simple Z3 Python expression string and return satisfiable state.
    The `expr_src` should define a `solver` variable of type z3.Solver.
    """
    try:
        import z3  # noqa: F401
    except Exception:
        log.warning("z3-solver not installed; cannot check satisfiability")
        return None

    local_ns = {}
    try:
        exec(expr_src, {}, local_ns)
        solver = local_ns.get('solver')
        if solver is None:
            log.error("No solver found in expression context")
            return None
        res = solver.check()
        if res.r == 1:
            return True
        if res.r == -1:
            return None
        return False
    except Exception as e:
        log.error(f"Constraint eval failed: {e}")
        return None


