from bigip.api.device_api import BigipConfig


class Nodes(BigipConfig):

    def __init__(self, hostname: str) -> str:
        super().__init__(hostname)
        self.sot_nodes = self.device_sot_parameters["ltm"]["nodes"]

    def _get_names(self):
        """Return all existing bigip nodes."""
        try:
            nodes = self.authentication().tm.ltm.nodes.get_collection(partition=self.partition)
            print()
            for node in nodes:
                print(f"{node.name}")
                self.logging().info(node.name)
            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _get_config(self) -> str:
        """Return all existing bigip nodes."""
        try:
            nodes = self.authentication().tm.ltm.nodes.get_collection(partition=self.partition)
            print()
            for node in nodes:

                print(f"{node.name}:")
                print(f"    address: {node.address}")
                print(f"    connectionLimit: {node.connectionLimit}")
                print(f"    dynamicRatio: {node.dynamicRatio}")
                print(f"    logging: {node.logging}")
                print(f"    monitor: {node.monitor}")
                print(f"    rateLimit: {node.rateLimit}")
                print(f"    ratio: {node.ratio}")
                print(f"    state: {node.state}")
                print(f"    session: {node.session}")

                self.logging().info(f"{node.name}:")
                self.logging().info(f"    address: {node.address}")
                self.logging().info(
                    f"    connectionLimit: {node.connectionLimit}")
                self.logging().info(f"    dynamicRatio: {node.dynamicRatio}")
                self.logging().info(f"    logging: {node.logging}")
                self.logging().info(f"    monitor: {node.monitor}")
                self.logging().info(f"    rateLimit: {node.rateLimit}")
                self.logging().info(f"    ratio: {node.ratio}")
                self.logging().info(f"    state: {node.state}")
                self.logging().info(f"    session: {node.session}")

            print("#" * 79)

        except Exception as e:
            self.logging().warninging(e)
            print(e)

    def _create(self) -> str:
        """Create new empty nodes per SOT parameters."""
        for name, node_property in self.sot_nodes.items():
            try:
                if self.authentication().tm.ltm.nodes.node.load(name=name, partition=self.partition):
                    self.logging().info(
                        f"Node '{name}' exists in bigip device.")
                    print(f"Node '{name}' exists in bigip device.")

            except Exception as e:
                self.authentication().tm.ltm.nodes.node.create(
                    name=name,
                    partition=self.partition,
                    address=node_property["address"],
                )
                self.logging().info(
                    f"Node '{name}' did not exist in bigip device and has been created.")
                print(
                    f"Node '{name}' did not exist in bigip device and has been created.")

    def _update(self) -> str:
        """Update all existing bigip nodes."""
        for name, node_property in self.sot_nodes.items():
            try:
                if self.authentication().tm.ltm.nodes.node.load(name=name, partition=self.partition):
                    self.logging().info(
                        f"Node '{name}' exists in bigip device.")
                    print(f"Node '{name}' exists in bigip device.")

                    node_obj = self.authentication().tm.ltm.nodes.node.load(
                        name=name, partition=self.partition)
                    node_obj.name = name
                    node_obj.address = node_property["address"]
                    node_obj.connectionLimit = node_property["connectionLimit"]
                    node_obj.dynamicRatio = node_property["dynamicRatio"]
                    node_obj.logging = node_property["logging"]
                    node_obj.monitor = node_property["monitor"]
                    node_obj.rateLimit = node_property["rateLimit"]
                    node_obj.ratio = node_property["ratio"]
                    node_obj.state = node_property["state"]
                    node_obj.session = node_property["session"]
                    node_obj.update()

                    self.logging().info(f"Node '{name}' has been updated.")
                    print(f"Node '{name}' has been updated.")

            except Exception as e:
                self.logging().warning(name)
                self.logging().warning(e)
                print(name)
                print(e)

    def _delete_not_sot(self) -> str:
        """Delete not SOT nodes that are not members of any pool. """
        nodes = self.authentication().tm.ltm.nodes.get_collection(partition=self.partition)
        bigip_names = [name.name for name in nodes]
        sot_names = [name for name in self.sot_nodes.keys()]
        delete_candidate = [
            name for name in bigip_names if name not in sot_names]

        for name in delete_candidate:
            self.logging().info(name)
            print(name)
            try:
                node_obj = self.authentication().tm.ltm.nodes.node.load(
                    name=name, partition=self.partition)
                node_obj.delete()
                self.logging().warning(f"Node '{name}' has been deleted.")
                print(f"Node '{name}' has been deleted.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _delete_all(self) -> str:
        """Delete all bigip nodes that are not members of any pool."""
        nodes = self.authentication().tm.ltm.nodes.get_collection(partition=self.partition)
        bigip_names = [name.name for name in nodes]

        for name in bigip_names:
            try:
                node_obj = self.authentication().tm.ltm.nodes.node.load(
                    name=name, partition=self.partition)
                node_obj.delete()
                self.logging().warning(f"Node '{name}' has been deleted.")
                print(f"Node '{name}' has been deleted.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _declare(self) -> str:
        """Create Update Delete to match SOT."""
        self._create()
        self._update()
        self._delete_not_sot()


class Node(Nodes):

    def __init__(self, hostname: str) -> str:
        super().__init__(hostname)

    def _get_config(self, name: str) -> str:
        """Get configuration of node"""
        try:
            node_obj = self.authentication().tm.ltm.nodes.node.load(
                name=name, partition=self.partition)
            print(f"{node_obj.name}:")
            print(f"    address: {node_obj.address}")
            print(f"    connectionLimit: {node_obj.connectionLimit}")
            print(f"    dynamicRatio: {node_obj.dynamicRatio}")
            print(f"    logging: {node_obj.logging}")
            print(f"    monitor: {node_obj.monitor}")
            print(f"    rateLimit: {node_obj.rateLimit}")
            print(f"    ratio: {node_obj.ratio}")
            print(f"    state: {node_obj.state}")
            print(f"    session: {node_obj.session}")

            self.logging().info(f"{node_obj.name}:")
            self.logging().info(f"    address: {node_obj.address}")
            self.logging().info(
                f"    connectionLimit: {node_obj.connectionLimit}")
            self.logging().info(f"    dynamicRatio: {node_obj.dynamicRatio}")
            self.logging().info(f"    logging: {node_obj.logging}")
            self.logging().info(f"    monitor: {node_obj.monitor}")
            self.logging().info(f"    rateLimit: {node_obj.rateLimit}")
            self.logging().info(f"    ratio: {node_obj.ratio}")
            self.logging().info(f"    state: {node_obj.state}")
            self.logging().info(f"    session: {node_obj.session}")

            print("#" * 79)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _create(self, name) -> str:
        """Create new empty node per SOT parameters."""
        for node_name, node_property in self.sot_nodes.items():
            if node_name == name:
                try:
                    if self.authentication().tm.ltm.nodes.node.load(name=name, partition=self.partition):
                        self.logging().info(
                            f"Node '{name}' exists in bigip device.")
                        print(f"Node '{name}' exists in bigip device.")
                        break

                except Exception as e:
                    self.authentication().tm.ltm.nodes.node.create(
                        name=name,
                        partition=self.partition,
                        address=node_property["address"],
                    )
                    self.logging().info(
                        f"Node '{name}' did not exist in bigip device and has been created.")
                    print(
                        f"Node '{name}' did not exist in bigip device and has been created.")
                    break

    def _update(self, name) -> str:
        """Update sepcified node per SOT parameters."""
        for node_name, node_property in self.sot_nodes.items():
            if node_name == name:
                try:
                    if self.authentication().tm.ltm.nodes.node.load(name=name, partition=self.partition):
                        self.logging().info(
                            f"Node '{name}' exists in bigip device.")
                        print(f"Node '{name}' exists in bigip device.")

                        node_obj = self.authentication().tm.ltm.nodes.node.load(
                            name=name, partition=self.partition)
                        node_obj.name = name
                        node_obj.address = node_property["address"]
                        node_obj.connectionLimit = node_property["connectionLimit"]
                        node_obj.dynamicRatio = node_property["dynamicRatio"]
                        node_obj.logging = node_property["logging"]
                        node_obj.monitor = node_property["monitor"]
                        node_obj.rateLimit = node_property["rateLimit"]
                        node_obj.ratio = node_property["ratio"]
                        node_obj.state = node_property["state"]
                        node_obj.session = node_property["session"]
                        node_obj.update()

                        self.logging().info(f"Node '{name}' has been updated.")
                        print(f"Node '{name}' has been updated.")
                        break

                except Exception as e:
                    self.logging().warning(name)
                    self.logging().warning(e)
                    print(name)
                    print(e)
                    break

    def _delete(self, name: str) -> str:
        """Delete specified node if not member of any pool."""
        try:
            node_obj = self.authentication().tm.ltm.nodes.node.load(
                name=name, partition=self.partition)
            node_obj.delete()
            self.logging().info(f"Node '{name}' has been deleted.")
            print(f"Node '{name}' has been deleted.")

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _exists(self, name: str) -> str:
        """Check if node exist in bigip device"""
        try:
            if self.authentication().tm.ltm.nodes.node.exists(name=name, partition=self.partition):
                self.logging().info(f"Node '{name}' exists.")
                print(f"Node '{name}' exists.")
            else:
                self.logging().warning(f"Node '{name}' does not exist.")
                print(f"Node '{name}' does not exist.")

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _ip_exists(self, ipv4: str) -> str:
        """Check if node Ipv4 exist in bigip device"""
        exist = False
        try:
            nodes = self.authentication().tm.ltm.nodes.get_collection(partition=self.partition)
            for node in nodes:
                if node.address == ipv4:
                    exist = True
                    break
            print(ipv4)
            print(exist)

        except Exception as e:
            self.logging().warning(e)
            print(e)

    def _call_method(self, name):
        try:
            node_obj = self.authentication().tm.ltm.nodes.node.load(
                name=name, partition=self.partition)
            return node_obj

        except Exception as e:
            self.logging().warning(e)
            print(e)
