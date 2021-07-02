from bigip.api.device_api import BigipConfig


class Profiles(BigipConfig):

    def __init__(self, hostname: str) -> str:
        super().__init__(hostname)
        self.sot_profiles = self.device_sot_parameters["ltm"]["profiles"]
        self.prof_types = self.mappings_parameters["profile_type_mappings"]

    def _get_names(self) -> str:
        """Return all existing bigip profiles."""
        self.logging().info(f"\nCurrent profiles:")
        print(f"\nCurrent profiles:")
        profile_names = []
        for parent_prof_type in self.prof_types.values():
            try:
                profiles = getattr(self.authentication(
                ).tm.ltm.profile, parent_prof_type).get_collection()
                for profile in profiles:
                    self.logging().info(profile.name)
                    print(profile.name)
                    profile_names.append(profile.name)

            except Exception as e:
                self.logging().warning(e)
                print(e)

        print("#" * 79)
        return profile_names

    def _get_config(self) -> str:
        """Return all existing bigip profiles and their configurations."""
        for parent_prof_type in self.prof_types.values():
            try:
                profiles = getattr(self.authentication(
                ).tm.ltm.profile, parent_prof_type).get_collection(partition=self.partition)
                for profile in profiles:
                    self.logging().info(profile.name)
                    print(profile.name)
                    print()
                    for k, v in profile.raw.items():
                        self.logging().info(f"{k}: {v}")
                        print(f"{k}: {v}")
                print()

            except Exception as e:
                self.logging().warning(e)
                print(e)

        print("#" * 79)

    def _create(self) -> str:
        """Create new profiles per SOT parameters."""
        for name, profile_property in self.sot_profiles.items():
            try:
                getattr(
                    getattr(
                        self.authentication(
                        ).tm.ltm.profile, self.prof_types[profile_property["type"]]
                    ),
                    profile_property["type"],
                ).create(name=name,
                         partition=self.partition,
                         )
                self.logging().info(f"Profile '{name}' has been created.")
                print(f"Profile '{name}' has been created.")

            except Exception as e:
                self.logging().warning(e)
                print(e)

    def _update(self) -> str:
        """Update all existing bigip profiles."""
        pass

    def _delete_not_sot(self) -> str:
        """Delete not SOT profiles that are not members of any pool. """
        bigip_names = self._get_names()
        sot_names = [name for name in self.sot_profiles]
        delete_candidate = [
            name for name in bigip_names if name not in sot_names]
        for name in delete_candidate:
            subclass_obj = Profile(self.hostname)
            subclass_obj._delete(name)

    def _delete_all(self) -> str:
        """Delete all bigip profiles."""
        for child_prof_type, parent_prof_type in self.prof_types.items():
            try:
                profiles = getattr(self.authentication().tm.ltm.profile, parent_prof_type).get_collection(
                    partition=self.partition)
                for profile in profiles:
                    try:
                        mon_obj = getattr(
                            getattr(self.authentication(
                            ).tm.ltm.profile, parent_prof_type), child_prof_type
                        ).load(name=profile.name, partition=self.partition)
                        mon_obj.delete()
                        self.logging().info(
                            f"Profile '{profile.name}' has been deleted.")
                        print(f"Profile '{profile.name}' has been deleted.")

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


class Profile(Profiles):

    def __init__(self, hostname: str) -> str:
        super().__init__(hostname)

    def _get_config(self, name) -> str:
        """Return all existing bigip profiles and their configurations."""
        for child_prof_type, parent_prof_type in self.prof_types.items():
            try:
                profiles = getattr(self.authentication(
                ).tm.ltm.profile, parent_prof_type).get_collection(partition=self.partition)

                for profile in profiles:
                    if profile.name == name:
                        profile_obj = getattr(getattr(self.authentication().tm.ltm.profile, parent_prof_type), child_prof_type
                                              ).load(name=name, partition=self.partition)
                        self.logging().info(profile.name)
                        print(profile.name)
                        print()
                        for key, value in profile_obj.raw.items():
                            self.logging().info(f"{key}: {value}")
                            print(f"{key}: {value}")
                        break

            except Exception as e:
                self.logging().warning(e)
                print(e)

        print("#" * 79)

    def _create(self, name) -> str:
        """Create specific profile per SOT parameters."""
        for profile_name, profile_property in self.sot_profiles.items():
            if profile_name == name:
                try:
                    getattr(
                        getattr(
                            self.authentication(
                            ).tm.ltm.profile, self.prof_types[profile_property["type"]]
                        ),
                        profile_property["type"],
                    ).create(name=name,
                             partition=self.partition,
                             )
                    self.logging().info(f"Profile '{name}' has been created.")
                    print(f"Profile '{name}' has been created.")

                except Exception as e:
                    self.logging().warning(e)
                    print(e)

    def _update(self, name) -> str:
        """Update all existing bigip profiles."""
        pass

    def _delete(self, name) -> str:
        """Delete specified profile if not member of any pool."""
        for child_prof_type, parent_prof_type in self.prof_types.items():
            try:
                prof_obj = getattr(
                    getattr(self.authentication().tm.ltm.profile,
                            parent_prof_type), child_prof_type
                ).load(name=name, partition=self.partition)
                try:
                    prof_obj.delete()
                    self.logging().warning(
                        f"Profile '{name}' has been deleted.")
                    print(f"Profile '{name}' has been deleted.")

                except Exception as e:
                    self.logging().warning(
                        f"Profile '{name}' can't be deleted")
                    print(f"Profile '{name}' can't be deleted")

            except Exception as e:
                # self.logging().warning(e)
                # print(e)
                pass

    def _exists(self, name) -> str:
        """Check if profile exist in bigip device"""
        exists = False
        for child_prof_type, parent_prof_type in self.prof_types.items():
            try:
                prof_obj = getattr(
                    getattr(self.authentication().tm.ltm.profile,
                            parent_prof_type), child_prof_type
                ).exists(name=name, partition=self.partition)

                exists = exists or prof_obj

            except Exception as e:
                self.logging().warning(e)
                print(e)

        # return exists
        self.logging().info(name)
        self.logging().info(exists)
        print(name)
        print(exists)
