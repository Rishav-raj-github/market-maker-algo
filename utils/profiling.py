import cProfile
import pstats
import io
from functools import wraps

def profile_function(func):
    """
    A decorator that uses cProfile to profile a single function's execution.
    Useful for identifying bottlenecks in the critical path (e.g., matching engine).
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        
        s = io.StringIO()
        sortby = pstats.SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(20) # Print top 20
        print(s.getvalue())
        
        return result
    return wrapper
