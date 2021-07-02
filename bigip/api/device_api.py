import yaml
import os
from pathlib import Path
from f5.bigip import ManagementRoot
from bigip.api import logbook_api


# Home directory
home_dir = str(Path.home())


# Inventory location and read data
inventory_subdir = "/f5_pyconf/bigip/data/inventory.yaml"
inventory_data = home_dir + inventory_subdir

with open(inventory_data, "r") as inventory_configs:
    inventory_parameters = yaml.load(inventory_configs, Loader=yaml.FullLoader)


# Profile mappings locaton and read data
mappings_subdir = "/f5_pyconf/bigip/data/mappings.yaml"
mappings_data = home_dir + mappings_subdir

with open(mappings_data, "r") as mappings_configs:
    mappings_parameters = yaml.load(mappings_configs, Loader=yaml.FullLoader)


# Logging location
parent_folder = "/bigip/logs/ltm"
parent_folder_path = home_dir + parent_folder


class BigipConfig:

    def __init__(self, hostname: str):
        self.hostname = hostname

        self.home_dir = home_dir

        # Inventory data
        self.inventory_parameters = inventory_parameters
        try:
            self.partition = inventory_parameters[self.hostname]["partition"]

        except Exception as e:
            self.partition = inventory_parameters["defaults"]["partition"]

        # Profile mappings
        self.mappings_parameters = mappings_parameters

        # Device SOT data
        device_sot_subdir = f"/f5_pyconf/bigip/data/devices_sot/{self.hostname}.yaml"
        device_sot_data = home_dir + device_sot_subdir

        with open(device_sot_data, "r") as sot_configs:
            device_sot_parameters = yaml.load(
                sot_configs, Loader=yaml.FullLoader)
        self.device_sot_parameters = device_sot_parameters

        # Initiate logging
        logbook_api.init_logging("ltm", f"{self.hostname}.log")

    def authentication(self) -> any:
        self.username = os.getenv(
            inventory_parameters[self.hostname]["username"])
        self.password = os.getenv(
            inventory_parameters[self.hostname]["password"])
        self.ipaddress = inventory_parameters[self.hostname]["ipaddress"]

        mgmt = ManagementRoot(self.ipaddress, self.username, self.password)
        return mgmt

    def logging(self) -> str:
        app_log = logbook_api.logbook.Logger(f"Logbook for {self.hostname}")
        return app_log
