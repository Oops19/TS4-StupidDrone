#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#
from typing import List, Any, Union

from interactions.base.super_interaction import SuperInteraction
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from stupid_drone.modinfo import ModInfo

from interactions.privacy import PrivacyService

from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from ts4lib.utils.resilent_injections.argument_updater import ArgumentsUpdater
from ts4lib.utils.resilent_injections.injection_utility import InjectionUtility
from ts4lib.utils.singleton import Singleton

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'stupid_drone_mem')
log.enable()
log.info("Stupid Drone is starting (MEM)...")


class StupidDroneMemory(metaclass=Singleton):
    def __init__(self):
        self.interactions = set()
        self.sim_info: Union[SimInfo, None] = None
