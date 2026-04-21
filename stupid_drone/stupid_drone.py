#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#
from typing import List, Any, Union

from stupid_drone.modinfo import ModInfo

from interactions.privacy import PrivacyService

from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from ts4lib.utils.resilent_injections.injection_utility import InjectionUtility
from ts4lib.utils.resilent_injections.argument_updater import ArgumentsUpdater


log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'stupid_drone')
log.enable()
log.info("Stupid Drone is starting (vanilla)...")


class StupidDrone:
    def __init__(self):
        rv = True
        # class PrivacyService:
        # def def add_vehicle_to_monitor(self, vehicle):
        # def def remove_vehicle_to_monitor(self, vehicle):
        #                                   0     1
        # args                                    0
        rv = rv & InjectionUtility.check_signature(ModInfo.get_identity(), PrivacyService, PrivacyService.add_vehicle_to_monitor.__name__, {'vehicle': (1, None)})
        rv = rv & InjectionUtility.check_signature(ModInfo.get_identity(), PrivacyService, PrivacyService.remove_vehicle_to_monitor.__name__, {'vehicle': (1, None)})
        if rv:
            self.inject()
        else:
            log.warn(f"Method signatures changed. Mod partially disabled itself.")

    @staticmethod
    def inject():
        @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), PrivacyService, PrivacyService.add_vehicle_to_monitor.__name__)
        def o19_inj_add_vehicle_to_monitor(original, self, *args, **kwargs):
            _args = ArgumentsUpdater.get_args([0, ], args)
            if _args is None:
                log.debug(f"o19_inj_add_vehicle_to_monitor(vehicle missing) ... skipping")
                return
            vehicle = args[0]
            if 'Drone' in f'{vehicle}':
                log.debug(f'o19_inj_add_vehicle_to_monitor({vehicle}) ... skipping')
            else:
                log.debug(f'o19_inj_add_vehicle_to_monitor({vehicle})')
                original(self, vehicle, *args, **kwargs)
            return

        @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), PrivacyService, PrivacyService.remove_vehicle_to_monitor.__name__)
        def o19_inj_remove_vehicle_to_monitor(original, self, *args, **kwargs):
            _args = ArgumentsUpdater.get_args([0, ], args)
            if _args is None:
                log.debug(f"o19_inj_remove_vehicle_to_monitor(vehicle missing) ... skipping")
                return
            vehicle = args[0]
            if 'Drone' in f'{vehicle}':
                log.debug(f'o19_inj_remove_vehicle_to_monitor({vehicle}) ... skipping')
            else:
                log.debug(f'o19_inj_remove_vehicle_to_monitor({vehicle})')
                original(self, *args, **kwargs)
            return


StupidDrone()
log.debug(f'initialized')
log.debug(f"Enable logging with 's4clib.enablelog {ModInfo.get_identity().base_namespace}'")
log.disable()

