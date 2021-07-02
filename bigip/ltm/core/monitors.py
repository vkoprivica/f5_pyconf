from bigip.api.device_api import BigipConfig


class Monitors(BigipConfig):

    def __init__(self, hostname: str) -> str:
        super().__init__(hostname)
        self.sot_monitors = self.device_sot_parameters["ltm"]["monitors"]
        self.mon_types = self.mappings_parameters["monitor_type_mappings"]

    def _get_names(self) -> str:
        """Return all existing bigip monitors."""
        monitor_names = []
        for parent_mon_type in self.mon_types.values():
            try:
                monitors = getattr(self.authentication(
                ).tm.ltm.monitor, parent_mon_type).get_collection(partition=self.partition)
                for monitor in monitors:
                    self.logging().info(monitor.name)
                    print(monitor.name)
                    monitor_names.append(monitor.name)
                print("#" * 79)

            except Exception as e:
                self.logging().warning(e)
                print(e)

        return monitor_names

    def _get_config(self) -> str:
        """Return all existing bigip monitors and their configurations."""
        for parent_mon_type in self.mon_types.values():
            try:
                monitors = getattr(self.authentication(
                ).tm.ltm.monitor, parent_mon_type).get_collection(partition=self.partition)
                for monitor in monitors:
                    self.logging().info(monitor.name)
                    print(monitor.name)
                    for key, value in monitor.raw.items():
                        print(f"{key}: {value}")
                    print()

            except Exception as e:
                self.logging().warning(e)
                print(e)

        print("#" * 79)

    def _create(self) -> str:
        """Create monitors based on SOT."""
        for name, monitor_property in self.sot_monitors.items():
            try:
                getattr(
                    getattr(
                        self.authentication(
                        ).tm.ltm.monitor, self.mon_types[monitor_property["type"]]
                    ),
                    monitor_property["type"],
                ).load(name=name,
                       partition=self.partition,
                       )
                print(f"Monitor '{name}' exists in bigip device.")
                self.logging().info(
                    (f"Monitor '{name}' exists in bigip device."))

            except Exception as e:

                if "icmp" in monitor_property["type"]:
                    getattr(
                        getattr(
                            self.authentication().tm.ltm.monitor,
                            self.mon_types[monitor_property["type"]],
                        ),
                        monitor_property["type"],
                    ).create(
                        name=name,
                        partition=self.partition,
                    )

                elif "http" in monitor_property["type"]:
                    getattr(
                        getattr(
                            self.authentication().tm.ltm.monitor,
                            self.mon_types[monitor_property["type"]],
                        ),
                        monitor_property["type"],
                    ).create(
                        name=name,
                        partition=self.partition,
                    )

                else:
                    getattr(
                        getattr(
                            self.authentication().tm.ltm.monitor,
                            self.mon_types[monitor_property["type"]],
                        ),
                        monitor_property["type"],
                    ).create(name=name,
                             partition=self.partition,
                             )

                print(
                    f"Monitor '{name}' did not exist in bigip device and has been created.")
                self.logging().warning(
                    f"Monitor '{name}' did not exist in bigip device and has been created.")

    def _update(self) -> str:
        """Update all existing bigip monitors."""
        for name, monitor_property in self.sot_monitors.items():
            try:
                if getattr(
                    getattr(
                        self.authentication(
                        ).tm.ltm.monitor, self.mon_types[monitor_property["type"]]
                    ),
                    monitor_property["type"],
                ).load(name=name, partition=self.partition):
                    self.logging().info(
                        f"Monitor '{name}' exists in bigip device.")

                    mon_obj = getattr(
                        getattr(
                            self.authentication(
                            ).tm.ltm.monitor, self.mon_types[monitor_property["type"]]
                        ),
                        monitor_property["type"],
                    ).load(name=name, partition=self.partition)

                    if "icmp" in monitor_property["type"]:
                        mon_obj.name = name
                        mon_obj.interval = monitor_property["interval"]
                        mon_obj.timeout = monitor_property["timeout"]
                        mon_obj.destination = monitor_property["alias"]
                        mon_obj.adaptive = monitor_property["adaptive"]
                        mon_obj.update()

                    elif "http" in monitor_property["type"]:
                        mon_obj.name = name
                        mon_obj.interval = monitor_property["interval"]
                        mon_obj.upInterval = monitor_property["upInterval"]
                        mon_obj.timeUntilUp = monitor_property["timeUntilUp"]
                        mon_obj.timeout = monitor_property["timeout"]
                        mon_obj.manualResume = monitor_property["manualResume"]
                        mon_obj.send = monitor_property["send"]
                        mon_obj.recv = monitor_property["recv"]
                        mon_obj.username = monitor_property["username"]
                        mon_obj.password = monitor_property["password"]
                        mon_obj.destination = monitor_property["alias"]
                        mon_obj.adaptive = monitor_property["adaptive"]
                        mon_obj.compatibility = "enabled"
                        mon_obj.update()

                    elif "tcp" in monitor_property["type"]:
                        mon_obj.name = name
                        mon_obj.interval = monitor_property["interval"]
                        mon_obj.upInterval = monitor_property["upInterval"]
                        mon_obj.timeUntilUp = monitor_property["timeUntilUp"]
                        mon_obj.timeout = monitor_property["timeout"]
                        mon_obj.manualResume = monitor_property["manualResume"]
                        mon_obj.send = monitor_property["send"]
                        mon_obj.recv = monitor_property["recv"]
                        mon_obj.alias = monitor_property["alias"]
                        mon_obj.adaptive = monitor_property["adaptive"]
                        mon_obj.update()

                    self.logging().info(
                        f"Monitor '{name}' has been updated."
                    )
                    print(f"Monitor '{name}' has been updated.")

            except Exception as e:
                self.logging().warning(e)
                # print(e)

    def _delete_not_sot(self) -> str:
        """Delete not SOT monitors that are not members of any pool. """
        bigip_names = self._get_names()
        sot_names = [name for name in self.sot_monitors.keys()]
        delete_candidate = [
            name for name in bigip_names if name not in sot_names]
        for name in delete_candidate:
            subclass_obj = Monitor(self.hostname)
            subclass_obj._delete(name)

    def _delete_all(self) -> str:
        """Delete all existing bigip monitors that are not member of any pool."""
        for child_mon_type, parent_mon_type in self.mon_types.items():
            try:
                monitors = getattr(self.authentication().tm.ltm.monitor, parent_mon_type).get_collection(
                    partition=self.partition)
                for monitor in monitors:
                    try:
                        mon_obj = getattr(
                            getattr(self.authentication(
                            ).tm.ltm.monitor, parent_mon_type), child_mon_type
                        ).load(name=monitor.name, partition=self.partition)
                        mon_obj.delete()
                        self.logging().info(
                            f"monitor '{monitor.name}' has been deleted.")
                        print(f"monitor '{monitor.name}' has been deleted.")

                    except Exception as e:
                        self.logging().warning(e)
                        print(e)

            except Exception as e:
                self.logging().warning(e)
                print(e)


    def _declare(self) -> str:
        """Create Update Delete to match SOT."""
        self._create()
        self._update()
        self._delete_not_sot()


class Monitor(Monitors):

    def __init__(self, hostname: str) -> str:
        super().__init__(hostname)

    def _get_config(self, name) -> str:
        """Returns existing bigip monitor and its configurations."""
        for child_mon_type, parent_mon_type in self.mon_types.items():
            try:
                monitors = getattr(self.authentication(
                ).tm.ltm.monitor, parent_mon_type).get_collection(partition=self.partition)

                for monitor in monitors:
                    if monitor.name == name:
                        monitor_obj = getattr(getattr(self.authentication().tm.ltm.monitor, parent_mon_type), child_mon_type
                                              ).load(name=name, partition=self.partition)
                        self.logging().info(monitor.name)
                        print(monitor.name)
                        print()
                        for key, value in monitor_obj.raw.items():
                            self.logging().info(f"{key}: {value}")
                            print(f"{key}: {value}")
                        break

            except Exception as e:
                self.logging().warning(e)
                print(e)

        print("#" * 79)

    def _create(self, name) -> str:
        """Create specific monitor per SOT parameters."""
        for monitor_name, monitor_property in self.sot_monitors.items():
            if monitor_name == name:
                try:
                    getattr(
                        getattr(
                            self.authentication(
                            ).tm.ltm.monitor, self.mon_types[monitor_property["type"]]
                        ),
                        monitor_property["type"],
                    ).create(name=name,
                             partition=self.partition,
                             )
                    self.logging().info(f"monitor '{name}' has been created.")
                    print(f"monitor '{name}' has been created.")

                except Exception as e:
                    self.logging().warning(e)
                    print(e)

    def _update(self) -> str:
        """Update all existing bigip monitors."""
        pass

    def _delete(self, name) -> str:
        """Delete specified monitor if not member of any pool."""
        for child_mon_type, parent_mon_type in self.mon_types.items():
            try:
                mon_obj = getattr(
                    getattr(self.authentication().tm.ltm.monitor,
                            parent_mon_type), child_mon_type
                ).load(name=name, partition=self.partition)
                try:
                    mon_obj.delete()
                    self.logging().warning(
                        f"Monitor '{name}' has been deleted.")
                    print(f"Monitor '{name}' has been deleted.")
                except Exception as e:
                    self.logging().info(
                        f"Monitor '{name}' can't be deleted")
                    print(f"Monitor '{name}' can't be deleted")

            except Exception as e:
                # self.logging().warning(e)
                # print(e)
                pass

    def _exists(self, name) -> str:
        """Check if monitor exist in bigip device"""
        exists = False
        for child_mon_type, parent_mon_type in self.mon_types.items():
            try:
                mon_obj = getattr(
                    getattr(self.authentication().tm.ltm.monitor,
                            parent_mon_type), child_mon_type
                ).exists(name=name, partition=self.partition)

                exists = exists or mon_obj

            except Exception as e:
                self.logging().warning(e)
                print(e)

        # return exists
        self.logging().info(name)
        self.logging().info(exists)
        print(name)
        print(exists)
