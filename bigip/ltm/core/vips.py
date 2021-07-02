import re
from bigip.api.device_api import BigipConfig

IPV4_ADDR_REGEX = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"


class Vips(BigipConfig):

    def __init__(self, hostname: str) -> str:
        super().__init__(hostname)
        self.sot_vips = self.device_sot_parameters["ltm"]["vips"]

    def _get_names(self) -> str:
        """Return all existing bigip vips."""
        try:
            vips = self.authentication().tm.ltm.virtuals.get_collection(partition=self.partition)
            for vip in vips:
                self.logging().info(vip.name)
                print(vip.name)
            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _get_config(self) -> str:
        """Get all pools and their members from bigip."""
        try:
            vips = self.authentication().tm.ltm.virtuals.get_collection(partition=self.partition)
            for vip in vips:
                print(f"{vip.name}")
                print()
                self.logging().info(f"{vip.name}")
                for key, value in vip.raw.items():
                    print(key, value)
            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _get_members(self) -> str:
        """Get all vips and their members from bigip."""
        try:
            vips = self.authentication().tm.ltm.virtuals.get_collection(partition=self.partition)
            for vip in vips:
                print()
                print(f"{vip.name}")
                self.logging().info(f"{vip.name}")
                for key, value in vip.raw.items():
                    print(key, value)

                profiles = vip.profiles_s.get_collection(
                    partition=self.partition)
                for profile in profiles:
                    print(profile.raw)
                    # print(f"    members:")
                    # print(f"        - {member.name}, ({member.address})")
                # break
            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _create(self) -> str:
        """Create new vips per SOT parameters."""
        for name, vip_property in self.sot_vips.items():
            try:
                self.authentication().tm.ltm.virtuals.virtual.create(
                    name=name,
                    partition=self.partition,
                    description=vip_property["description"],
                    destination=vip_property["destination"],
                    ipProtocol=vip_property["ipProtocol"],
                    mask=vip_property["mask"],
                    pool=vip_property["pool"],
                    source=vip_property["source"],
                    sourceAddressTranslation=vip_property['sourceAddressTranslation'],
                    rules=vip_property["rules"],
                    profiles=vip_property["profiles"],
                )

                self.logging().info(f"VIP '{name}' has been created.")
                print(f"VIP '{name}' has been created.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _update(self) -> str:
        """Assign pools to each vip to match SOT."""
        for name, vip_property in self.sot_vips.items():
            try:
                if self.authentication().tm.ltm.virtuals.virtual.load(name=name, partition=self.partition):
                    self.logging().info(
                        f"Vip '{name}' exists in bigip device.")
                    print(f"Vip '{name}' exists in bigip device.")

                    vip_obj = self.authentication().tm.ltm.virtuals.virtual.load(
                        name=name,
                        partition=self.partition
                    )

                    vip_obj.description = vip_property["description"]
                    vip_obj.destination = vip_property["destination"]
                    vip_obj.ipProtocol = vip_property["ipProtocol"]
                    vip_obj.mask = vip_property["mask"]
                    vip_obj.pool = vip_property["pool"]
                    vip_obj.source = vip_property["source"]
                    vip_obj.sourceAddressTranslation = vip_property['sourceAddressTranslation']
                    vip_obj.rules = vip_property["rules"]
                    vip_obj.profiles = vip_property["profiles"]
                    vip_obj.update()

                    self.logging().info(f"Vip '{name}' has been updated.")
                    print(f"Vip '{name}' has been updated.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _delete_not_sot(self) -> str:
        """Delete not SOT vips. """
        vips = self.authentication().tm.ltm.virtuals.get_collection(partition=self.partition)
        bigip_names = [name.name for name in vips]
        sot_names = [name for name in self.sot_vips.keys()]
        delete_candidate = [
            name for name in bigip_names if name not in sot_names]

        for name in delete_candidate:
            try:
                vip_obj = self.authentication().tm.ltm.virtuals.virtual.load(
                    name=name, partition=self.partition)
                vip_obj.delete()
                self.logging().warning(f"Vip '{name}' has been deleted.")
                print(f"Vip '{name}' has been deleted.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _delete_all(self) -> str:
        """Delete all bigip vips."""
        vips = self.authentication().tm.ltm.virtuals.get_collection(partition=self.partition)
        bigip_names = [name.name for name in vips]

        for name in bigip_names:
            try:
                vip_obj = self.authentication().tm.ltm.virtuals.virtual.load(
                    name=name, partition=self.partition)
                vip_obj.delete()
                self.logging().warning(f"Vip '{name}' has been deleted.")
                print(f"Vip '{name}' has been deleted.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _declare(self) -> str:
        """Create Update Delete to match SOT."""
        self._create()
        self._update()
        self._delete_not_sot()

    def _profiles_get_names(self) -> str:
        """Return profiles assigned to vips."""
        try:
            vips = self.authentication().tm.ltm.virtuals.get_collection(partition=self.partition)
            for vip in vips:
                print()
                self.logging().info(vip.name)
                print(vip.name)
                profiles = vip.profiles_s.get_collection()
                for profile in profiles:
                    self.logging().info(f"{profile.raw['name']}")
                    print(profile.raw['name'])
            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _profiles_get_config(self) -> str:
        """Return profiles assigned to vips."""
        try:
            vips = self.authentication().tm.ltm.virtuals.get_collection(partition=self.partition)
            for vip in vips:
                print()
                # self.logging().info(vip.name)
                print(vip.name)
                profiles = vip.profiles_s.get_collection()
                for profile in profiles:
                    for key, value in profile.raw.items():
                        # self.logging().info(key, value)
                        print(key, value)
                    print("-" * 79)
            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)


class Vip(Vips):

    def __init__(self, hostname: str) -> str:
        super().__init__(hostname)

    def _get_config(self, name) -> str:
        """Check if vip exist in bigip device"""
        try:
            vip_obj = self.authentication().tm.ltm.virtuals.virtual.load(
                name=name, partition=self.partition)
            print(vip_obj.name)
            print()
            self.logging().info(f"{vip_obj.name}")
            for key, value in vip_obj.raw.items():
                self.logging().info(f"{key}: {value}")
                print(key, value)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _create(self, name) -> str:
        """Create new vip per SOT parameters."""
        for vip_name, vip_property in self.sot_vips.items():
            if vip_name == name:
                try:
                    self.authentication().tm.ltm.virtuals.virtual.create(
                        name=name,
                        partition=self.partition,
                        description=vip_property["description"],
                        destination=vip_property["destination"],
                        ipProtocol=vip_property["ipProtocol"],
                        mask=vip_property["mask"],
                        pool=vip_property["pool"],
                        source=vip_property["source"],
                        sourceAddressTranslation=vip_property['sourceAddressTranslation'],
                        rules=vip_property["rules"],
                        profiles=vip_property["profiles"],
                    )

                    self.logging().info(f"VIP '{name}' has been created.")
                    print(f"VIP '{name}' has been created.")
                    break

                except Exception as e:
                    self.logging().warning(e)
                    print(e)
                    break

    def _update(self, name) -> str:
        """Assign pools to specific vip to match SOT."""
        for vip_name, vip_property in self.sot_vips.items():
            if vip_name == name:
                try:
                    if self.authentication().tm.ltm.virtuals.virtual.load(name=name, partition=self.partition):
                        self.logging().info(
                            f"Vip '{name}' exists in bigip device.")
                        print(f"Vip '{name}' exists in bigip device.")

                        vip_obj = self.authentication().tm.ltm.virtuals.virtual.load(
                            name=name,
                            partition=self.partition
                        )

                        vip_obj.description = vip_property["description"]
                        vip_obj.destination = vip_property["destination"]
                        vip_obj.ipProtocol = vip_property["ipProtocol"]
                        vip_obj.mask = vip_property["mask"]
                        vip_obj.pool = vip_property["pool"]
                        vip_obj.source = vip_property["source"]
                        vip_obj.sourceAddressTranslation = vip_property['sourceAddressTranslation']
                        vip_obj.rules = vip_property["rules"]
                        vip_obj.profiles = vip_property["profiles"]
                        vip_obj.update()

                        self.logging().info(f"Vip '{name}' has been updated.")
                        print(f"Vip '{name}' has been updated.")

                except Exception as e:
                    self.logging().warning(e)
                    print(e)

    def _delete(self, name) -> str:
        """Delete specified vip."""
        try:
            vip_obj = self.authentication().tm.ltm.virtuals.virtual.load(
                name=name, partition=self.partition)
            vip_obj.delete()
            self.logging().warning(f"Vip '{name}' has been deleted.")
            print(f"Vip '{name}' has been deleted.")

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _exists(self, name) -> str:
        """Check if vip exist in bigip device"""
        if self.authentication().tm.ltm.virtuals.virtual.exists(name=name, partition=self.partition):
            self.logging().info(f"Vip '{name}' exists.")
            print(f"Vip '{name}' exists.")
        else:
            self.logging().warning(f"Vip '{name}' does not exist.")
            print(f"Vip '{name}' does not exist.")

    def _ip_exists(self, ipv4: str) -> str:
        """Check if vip Ipv4 exist in bigip device"""
        exist = False
        try:
            vips = self.authentication().tm.ltm.virtuals.get_collection(partition=self.partition)
            for vip in vips:
                ipv4_match = re.search(
                    IPV4_ADDR_REGEX, vip.destination).group()
                if ipv4_match == ipv4:
                    exist = True
                    break
            print(ipv4)
            print(exist)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _call_method(self, name):
        try:
            vip_obj = self.authentication().tm.ltm.virtuals.virtual.load(
                name=name, partition=self.partition)
            return vip_obj

        except Exception as e:
            self.logging().warning(e)
            print(e)
