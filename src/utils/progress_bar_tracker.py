from tqdm import tqdm


class ProgressTracker:
    """
    A class to track and update the progress of file processing in the ExcelDecryptor.

    This class is used to create a tqdm progress bar instance. It provides methods to update and close the progress bar, which are invoked in the ExcelDecryptor's file processing methods.

    Attributes:
        pbar (tqdm): A tqdm progress bar instance for displaying the processing progress.

    Methods:
        update: Increments the progress bar by one unit.
        close: Closes the progress bar upon completion of all tasks.
    """

    def __init__(self, total):
        self.pbar = tqdm(total=total, desc="Processing")

    def update(self):
        self.pbar.update(1)

    def close(self):
        self.pbar.close()
