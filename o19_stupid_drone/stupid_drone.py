#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from o19_stupid_drone.modinfo import ModInfo
from interactions.privacy import PrivacyService

from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().base_namespace)
log.enable()
log.info("Stupid Drone is starting ...")
log.debug(f"Enable logging with 's4clib.enablelog {ModInfo.get_identity().base_namespace}'")
log.disable()


class StupidDrone:

    @staticmethod
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), PrivacyService, PrivacyService.add_vehicle_to_monitor.__name__)
    def o19_inj_add_vehicle_to_monitor(original, self, vehicle, *args, **kwargs):
        if 'Drone' in f'{vehicle}':
            log.debug(f'o19_inj_add_vehicle_to_monitor({vehicle}) ... skipping')
        else:
            log.debug(f'o19_inj_add_vehicle_to_monitor({vehicle})')
            original(self, vehicle, *args, **kwargs)

    @staticmethod
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), PrivacyService, PrivacyService.remove_vehicle_to_monitor.__name__)
    def o19_inj_remove_vehicle_to_monitor(original, self, vehicle, *args, **kwargs):
        if 'Drone' in f'{vehicle}':
            log.debug(f'o19_inj_remove_vehicle_to_monitor({vehicle}) ... skipping')
        else:
            log.debug(f'o19_inj_remove_vehicle_to_monitor({vehicle})')
            original(self, vehicle, *args, **kwargs)


StupidDrone()