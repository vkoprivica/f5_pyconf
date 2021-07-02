from bigip.api.device_api import BigipConfig


class IRules(BigipConfig):

    def __init__(self, hostname: str):
        super().__init__(hostname)
        self.sot_irules = self.device_sot_parameters["ltm"]["irules"]

        # Device Irules data
        self.device_irules_dir = f"/f5_pyconf/bigip/data/irules/{self.hostname}"

    def _get_names(self) -> str:
        """Return all existing bigip irule names."""
        try:
            irules = self.authentication().tm.ltm.rules.get_collection(partition=self.partition)
            print()
            for irule in irules:
                print(irule.name)
            print("#" * 79)

            self.logging().info(f"\nCurrent irules:")
            [self.logging().info(f"'{i.name}'") for i in irules]

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _get_config(self) -> str:
        """Return all existing bigip irules."""
        try:
            irules = self.authentication().tm.ltm.rules.get_collection(partition=self.partition)
            print()
            for irule in irules:
                self.authentication().tm.ltm.rules.rule.load(
                    name=irule.name, partition=self.partition)
                print(irule.name)
                if irule.apiAnonymous:
                    irule_lines = irule.apiAnonymous.splitlines()
                    for line in irule_lines:
                        print(line)
                print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _create(self) -> str:
        """Creates empty irules based on SOT."""
        if self.sot_irules is not None:
            for name in self.sot_irules:
                subclass_obj = IRule(self.hostname)
                if not subclass_obj._exists(name):
                    try:
                        data = ""
                        self.authentication().tm.ltm.rules.rule.create(
                            name=name, partition=self.partition, apiAnonymous=data)
                        self.logging().info(
                            f"IRule '{name}' did not exist in bigip device and has been created.")
                        print(
                            f"IRule '{name}' did not exist in bigip device and has been created.")

                    except Exception as e:
                        self.logging().warning(e)
                        print(e)
                else:
                    print(f"IRule '{name}' exists already.")
        else:
            pass

    def _update(self) -> str:
        """Update irules to match SOT."""
        if self.sot_irules is not None:
            for name in self.sot_irules:
                try:
                    with open(
                        f"{self.home_dir + self.device_irules_dir}/{name}.json", "r"
                    ) as irule_configs:
                        data = irule_configs.read()

                    counter = 0
                    if self.authentication().tm.ltm.rules.rule.load(name=name, partition=self.partition):
                        self.logging().info(
                            f"IRule '{name}' exists in bigip device.")
                        print(f"IRule '{name}' exists in bigip device.")

                        irule = self.authentication().tm.ltm.rules.rule.load(
                            name=name, partition=self.partition)
                        data_lines = data.splitlines()

                        try:
                            if irule.apiAnonymous:
                                irule_lines = irule.apiAnonymous.splitlines()

                                for idx, (i1, i2) in enumerate(zip(data_lines, irule_lines), 1):
                                    if i1 not in irule_lines:
                                        counter += 1
                                        self.logging().warning(
                                            f"IRule '{name}' Error - discrepancy:\n{idx} {i1} {i2}"
                                        )
                                        print(
                                            f"IRule '{name}' Error - discrepancy:\n{idx} {i1} {i2}")

                                    elif i2 not in data_lines:
                                        counter += 1
                                        self.logging().info(
                                            f"IRule '{name}' does not exist in SOT:\n{idx} {i1} {i2}"
                                        )
                                        print(
                                            f"IRule '{name}' does not exist in SOT:\n{idx} {i1} {i2}")

                            if counter > 0:
                                irule.apiAnonymous = data
                                irule.update()
                                self.logging().info(
                                    f"IRule '{name}' has been updated.")
                                print(f"IRule '{name}' has been updated.")

                            else:
                                self.logging().info(
                                    f"IRule '{name}' matches source of truth.")
                                print(
                                    f"IRule '{name}' matches source of truth.")

                        except Exception as e:
                            self.logging().warning(e)
                            irule.apiAnonymous = data
                            irule.update()
                            self.logging().info(
                                f"IRule '{name}' was empty and has been updated.")
                            print(
                                f"IRule '{name}' was empty and has been updated.")

                except Exception as e:
                    self.logging().warning(e)
                    self.logging().warning(
                        f"IRule '{name}' configuration does not exist in irules folder. Please create it!")
                    print(e)
                    print(
                        f"IRule '{name}' configuration does not exist in irules folder. Please create it!")
        else:
            pass

    def _delete_not_sot(self) -> str:
        """Delete irules that does not exist in SOT."""
        irules = self.authentication().tm.ltm.rules.get_collection(partition=self.partition)
        bigip_names = [name.name for name in irules]

        try:
            sot_names = [k for k in self.sot_irules]
        except:
            sot_names = []

        delete_candidate = [i for i in bigip_names if i not in sot_names]

        for name in delete_candidate:
            try:
                irule_obj = self.authentication().tm.ltm.rules.rule.load(
                    name=name, partition=self.partition)
                irule_obj.delete()
                self.logging().warning(f"IRule '{name}' has been deleted!")
                print(f"IRule '{name}' has been deleted!")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _delete_all(self) -> str:
        """Delete all bigip irules."""
        irules = self.authentication().tm.ltm.rules.get_collection(partition=self.partition)
        bigip_names = [name.name for name in irules]

        for name in bigip_names:
            try:
                irule_obj = self.authentication().tm.ltm.rules.rule.load(
                    name=name, partition=self.partition)
                irule_obj.delete()
                self.logging().warning(f"IRule '{name}' has been deleted!")
                print(f"IRule '{name}' has been deleted!")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _declare(self) -> str:
        """Create Update Delete to match SOT."""
        self._create()
        self._update()
        self._delete_not_sot()


class IRule(IRules):

    def __init__(self, hostname: str):
        super().__init__(hostname)

    def _get_config(self, name: str) -> str:
        """Get configuration of a specific irule."""
        try:
            irule_obj = self.authentication().tm.ltm.rules.rule.load(
                name=name, partition=self.partition)

            print(irule_obj.name)
            if irule_obj.apiAnonymous:
                irule_lines = irule_obj.apiAnonymous.splitlines()
                for line in irule_lines:
                    print(line)
            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _create(self, name) -> str:
        """Creates an empty irule based on SOT."""
        for irule_name in self.sot_irules:
            if irule_name == name:
                try:
                    data = ""
                    self.authentication().tm.ltm.rules.rule.create(
                        name=name, partition=self.partition, apiAnonymous=data)
                    self.logging().info(
                        f"IRule '{name}' did not exist in bigip device and has been created.")
                    print(
                        f"IRule '{name}' did not exist in bigip device and has been created.")

                except Exception as e:
                    self.logging().warning(e)
                    print(e)

    def _update(self, name) -> str:
        """Update an irule to match SOT."""
        for irule_name in self.sot_irules:
            if irule_name == name:
                try:
                    with open(
                        f"{self.home_dir + self.device_irules_dir}/{name}.json", "r"
                    ) as irule_configs:
                        data = irule_configs.read()

                    counter = 0
                    if self.authentication().tm.ltm.rules.rule.load(name=name, partition=self.partition):
                        self.logging().info(
                            f"IRule '{name}' exists in bigip device.")
                        print(f"IRule '{name}' exists in bigip device.")

                        irule = self.authentication().tm.ltm.rules.rule.load(
                            name=name, partition=self.partition)
                        data_lines = data.splitlines()

                        try:
                            if irule.apiAnonymous:
                                irule_lines = irule.apiAnonymous.splitlines()

                                for idx, (i1, i2) in enumerate(zip(data_lines, irule_lines), 1):
                                    if i1 not in irule_lines:
                                        counter += 1
                                        self.logging().warning(
                                            f"IRule '{name}' Error - discrepancy:\n{idx} {i1} {i2}"
                                        )
                                        print(
                                            f"IRule '{name}' Error - discrepancy:\n{idx} {i1} {i2}")

                                    elif i2 not in data_lines:
                                        counter += 1
                                        self.logging().info(
                                            f"IRule '{name}' does not exist in SOT:\n{idx} {i1} {i2}"
                                        )
                                        print(
                                            f"IRule '{name}' does not exist in SOT:\n{idx} {i1} {i2}")

                            if counter > 0:
                                irule.apiAnonymous = data
                                irule.update()
                                self.logging().info(
                                    f"IRule '{name}' has been updated.")
                                print(f"IRule '{name}' has been updated.")

                            else:
                                self.logging().info(
                                    f"IRule '{name}' matches source of truth.")
                                print(
                                    f"IRule '{name}' matches source of truth.")

                        except Exception as e:
                            self.logging().warning(e)
                            irule.apiAnonymous = data
                            irule.update()
                            self.logging().info(
                                f"IRule '{name}' was empty and has been updated.")
                            print(
                                f"IRule '{name}' was empty and has been updated.")

                except Exception as e:
                    self.logging().warning(e)
                    self.logging().warning(
                        f"IRule '{name}' configuration does not exist in irules folder. Please create it!")
                    print(e)
                    print(
                        f"IRule '{name}' configuration does not exist in irules folder. Please create it!")

    def _delete(self, name: str) -> str:
        """Delete a specified irule."""
        try:
            irule_obj = self.authentication().tm.ltm.rules.rule.load(
                name=name, partition=self.partition)
            irule_obj.delete()
            self.logging().warning(f"IRule '{name}' has been deleted!")
            print(f"IRule '{name}' has been deleted!")

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _exists(self, name: str) -> str:
        """Check if specified irule exists."""
        try:
            irule_obj = self.authentication().tm.ltm.rules.rule.exists(
                name=name, partition=self.partition)
            if irule_obj:
                self.logging().info(f"IRule '{name}' exists: {irule_obj}")
                print(f"IRule '{name}' exists: {irule_obj}")
                return irule_obj

            else:
                self.logging().info(f"IRule '{name}' exists: {irule_obj}")
                print(f"IRule '{name}' exists: {irule_obj}")
                return irule_obj

        except Exception as e:
            self.logging().warning(e)
            print(e)
