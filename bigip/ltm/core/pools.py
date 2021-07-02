from bigip.api.device_api import BigipConfig


class Pools(BigipConfig):

    def __init__(self, hostname: str) -> str:
        super().__init__(hostname)
        self.sot_pools = self.device_sot_parameters["ltm"]["pools"]

    def _get_names(self) -> str:
        """Return all existing bigip pools."""
        try:
            pools = self.authentication().tm.ltm.pools.get_collection(partition=self.partition)
            for pool in pools:
                print(f"{pool.name}")
                self.logging().info(pool.name)
            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _get_config(self) -> str:
        """Get all pools and their members from bigip."""
        try:
            pools = self.authentication().tm.ltm.pools.get_collection(partition=self.partition)
            for pool in pools:
                print(f"{pool.name}:")
                self.logging().info(f"{pool.name}:")
                print()
                print(f"    load balanding method: {pool.loadBalancingMode}")
                self.logging().info(
                    f"    load balanding method: {pool.loadBalancingMode}")
                print(f"    monitor: {pool.monitor}")
                self.logging().info(f"    monitor: {pool.monitor}")

                for member in pool.members_s.get_collection():
                    self.logging().info(f"    members:")
                    self.logging().info(f"        - {member.name}")
                    print(f"    members:")
                    # print(f"        - {member.name}")
                    print(f"        - {member.name}, ({member.address}, {member.session})")
            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _create(self) -> str:
        """Create new empty pools per SOT parameters."""
        for name in self.sot_pools.keys():
            try:
                if self.authentication().tm.ltm.pools.pool.load(name=name, partition=self.partition):
                    self.logging().info(
                        f"Pool '{name}' exists in bigip device.")
                    print(f"Pool '{name}' exists in bigip device.")

            except Exception as e:
                self.authentication().tm.ltm.pools.pool.create(
                    name=name, partition=self.partition)
                self.logging().info(
                    f"Pool '{name}' did not exist in bigip device and has been created.")
                print(
                    f"Pool '{name}' did not exist in bigip device and has been created.")

    def _update(self) -> str:
        """Assign monitors and members to each pool to match SOT."""
        for name, pool_property in self.sot_pools.items():
            try:
                if self.authentication().tm.ltm.pools.pool.load(name=name, partition=self.partition):
                    self.logging().info(
                        f"Pool '{name}' exists in bigip device.")
                    print(f"Pool '{name}' exists in bigip device.")

                    pool_obj = self.authentication().tm.ltm.pools.pool.load(
                        name=name, partition=self.partition)
                    pool_obj.monitor = pool_property["monitor"]
                    pool_obj.update()
                    self.logging().info(
                        f"Monitor '{pool_property['monitor']}' has been updated.")
                    print(
                        f"Monitor '{pool_property['monitor']}' has been updated.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

            try:
                if self.authentication().tm.ltm.pools.pool.load(name=name, partition=self.partition):
                    pool_obj = self.authentication().tm.ltm.pools.pool.load(
                        name=name, partition=self.partition)
                    for mem in pool_obj.members_s.get_collection(partition=self.partition):
                        mem.delete()

                    for name in pool_property["members"]:
                        pool_obj.members_s.members.create(
                            name=name, partition=self.partition)
                        self.logging().info(
                            f"Member '{name}' has been updated.")
                        print(f"Member '{name}' has been updated.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _delete_not_sot(self) -> str:
        """Delete not SOT pools that are not members of any virtual server. """
        pools = self.authentication().tm.ltm.pools.get_collection(partition=self.partition)
        bigip_names = [name.name for name in pools]
        sot_names = [name for name in self.sot_pools.keys()]
        delete_candidate = [
            name for name in bigip_names if name not in sot_names]

        for name in delete_candidate:
            self.logging().info(name)
            print(name)
            try:
                pool_obj = self.authentication().tm.ltm.pools.pool.load(
                    name=name, partition=self.partition)
                pool_obj.delete()
                self.logging().warning(f"Pool '{name}' has been deleted.")
                print(f"Pool '{name}' has been deleted.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _delete_all(self) -> str:
        """Delete all bigip pools that are not members of any virtual server."""
        pools = self.authentication().tm.ltm.pools.get_collection(partition=self.partition)
        bigip_names = [name.name for name in pools]

        for name in bigip_names:
            try:
                pool_obj = self.authentication().tm.ltm.pools.pool.load(
                    name=name, partition=self.partition)
                pool_obj.delete()
                self.logging().warning(f"Pool '{name}' has been deleted.")
                print(f"Pool '{name}' has been deleted.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _declare(self) -> str:
        """Create Update Delete to match SOT."""
        self._create()
        self._update()
        self._delete_not_sot()


class Pool(Pools):

    def __init__(self, hostname: str) -> str:
        super().__init__(hostname)

    def _get_config(self, name) -> str:
        """Get configuration of pool"""
        try:
            pool = self.authentication().tm.ltm.pools.pool.load(
                name=name, partition=self.partition)
            print(f"{pool.name}:")
            self.logging().info(f"{pool.name}:")
            print()
            print(f"    load balanding method: {pool.loadBalancingMode}")
            self.logging().info(
                f"    load balanding method: {pool.loadBalancingMode}")
            print(f"    monitor: {pool.monitor}")
            self.logging().info(f"    monitor: {pool.monitor}")

            for member in pool.members_s.get_collection():
                self.logging().info(f"    members:")
                self.logging().info(f"        - {member.name}")
                print(f"    members:")
                # print(f"        - {member.name}")
                print(f"        - {member.name}, ({member.address}, {member.session})")
            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _create(self, name) -> str:
        """Create new empty pool per SOT parameters."""
        for node_name in self.sot_pools.keys():
            if node_name == name:
                try:
                    if self.authentication().tm.ltm.pools.pool.load(name=name, partition=self.partition):
                        self.logging().info(
                            f"Pool '{name}' exists in bigip device.")
                        print(f"Pool '{name}' exists in bigip device.")
                        break

                except Exception as e:
                    self.authentication().tm.ltm.pools.pool.create(
                        name=name, partition=self.partition)
                    self.logging().info(
                        f"Pool '{name}' did not exist in bigip device and has been created.")
                    print(
                        f"Pool '{name}' did not exist in bigip device and has been created.")
                    break

    def _update(self, name) -> str:
        """Assign monitors and members to specific pool to match SOT."""
        for node_name, pool_property in self.sot_pools.items():
            if node_name == name:
                try:
                    if self.authentication().tm.ltm.pools.pool.load(name=name, partition=self.partition):
                        self.logging().info(
                            f"Pool '{name}' exists in bigip device.")
                        print(f"Pool '{name}' exists in bigip device.")

                        pool_obj = self.authentication().tm.ltm.pools.pool.load(
                            name=name, partition=self.partition)
                        pool_obj.monitor = pool_property["monitor"]
                        pool_obj.update()
                        self.logging().info(
                            f"Monitor '{pool_property['monitor']}' has been updated.")
                        print(
                            f"Monitor '{pool_property['monitor']}' has been updated.")

                except Exception as e:
                    self.logging().warning(e)
                    print(e)

                try:
                    if self.authentication().tm.ltm.pools.pool.load(name=name, partition=self.partition):
                        pool_obj = self.authentication().tm.ltm.pools.pool.load(
                            name=name, partition=self.partition)
                        for mem in pool_obj.members_s.get_collection(partition=self.partition):
                            mem.delete()

                        for name in pool_property["members"]:
                            pool_obj.members_s.members.create(
                                name=name, partition=self.partition)
                            self.logging().info(
                                f"Member '{name}' has been updated.")
                            print(f"Member '{name}' has been updated.")
                        break

                except Exception as e:
                    self.logging().warning(e)
                    print(e)
                    break

    def _delete(self, name) -> str:
        """Delete specified pool if not member of any virtual server."""
        try:
            pool_obj = self.authentication().tm.ltm.pools.pool.load(
                name=name, partition=self.partition)
            pool_obj.delete()
            self.logging().warning(f"Pool '{name}' has been deleted.")
            print(f"Pool '{name}' has been deleted.")

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _exists(self, name) -> str:
        """Check if node exist in bigip device"""
        try:
            if self.authentication().tm.ltm.pools.pool.exists(name=name, partition=self.partition):
                self.logging().info(f"Pool '{name}' exists.")
                print(f"Pool '{name}' exists.")

            else:
                self.logging().warning(f"Pool '{name}' does not exist.")
                print(f"Pool '{name}' does not exist.")

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _call_method(self, name):
        try:
            pool_obj = self.authentication().tm.ltm.pools.pool.load(
                name=name, partition=self.partition)
            return pool_obj

        except Exception as e:
            self.logging().warning(e)
            print(e)
