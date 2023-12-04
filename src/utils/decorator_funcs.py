from functools import wraps

from src.utils.progress_bar_tracker import ProgressTracker


def progress_bar_decorator(func):
    """
    A decorator function that adds a progress bar to functions in the ExcelDecryptor class.

    This decorator initializes a ProgressTracker instance and injects it into the decorated function. The decorated function (like read_encrypted_excels) uses this tracker to update the progress bar based on the completion of file processing tasks.

    Parameters:
        func (function): The function to be decorated, typically a method of ExcelDecryptor.

    Returns:
        function: The wrapped function with an integrated ProgressTracker.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]

        selected_files = (
            kwargs.get("selected_files") if "selected_files" in kwargs else None
        )
        if selected_files is None and len(args) > 1:
            selected_files = args[1]

        total = len(selected_files) if selected_files else len(self.password_dict)
        tracker = ProgressTracker(total)

        # Include the tracker as an argument
        result = func(*args, **kwargs, progress_tracker=tracker)

        tracker.close()
        return result

    return wrapper
