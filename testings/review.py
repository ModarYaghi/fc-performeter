from functools import wraps
from tqdm import tqdm

def with_progress_bar(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        total = len(args[0].password_dict)  # Assuming first argument is 'self' and has 'password_dict'
        with tqdm(total=total, desc="Decrypting and Reading Files") as pbar:
            def update(*a, **k):
                pbar.update(1)
                return func(*a, **k)
            return update(*args, **kwargs)
    return wrapper
