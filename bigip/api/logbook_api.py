import sys
import logbook

from pathlib import Path

# Logging location
home_dir = str(Path.home())
parent_folder = "/f5_pyconf/bigip/logs"
parent_folder_path = home_dir + parent_folder


def init_logging(log_folder: str, filename: str):
    """Logging function to create new logging file each day.
    """
    level = logbook.TRACE
    logbook.set_datetime_format("local")  # Logging in local timezone.

    # Set location of logs.
    # base_folder = os.path.dirname(__file__)
    base_folder = f"{parent_folder_path}/{log_folder}"
    # filename = os.path.join(base_folder, filename)
    filename = f"{base_folder}/{filename}"

    if filename:
        logbook.TimedRotatingFileHandler(
            filename, level=level).push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=level).push_application()

    msg = "Logging initialized, level: {}, mode: {}\n".format(
        level, "stdout mode" if not filename else "file mode: " + filename)

    logger = logbook.Logger("\nStartup")
    logger.notice(msg)
