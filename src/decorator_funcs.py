from functools import wraps
from tqdm import tqdm


def with_progress_bar(total=None, desc="Processing", position=0, step=1):
    pbar = None

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal pbar
            if pbar is None:
                pbar = tqdm(total=total, desc=desc, position=position)
            result = func(*args, **kwargs)
            pbar.update(step)
            if pbar.n >= pbar.total:
                pbar.close()
            return result

        return wrapper

    return decorator
