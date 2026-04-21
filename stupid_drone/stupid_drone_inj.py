#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#



from interactions.base.super_interaction import SuperInteraction
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from stupid_drone.modinfo import ModInfo

from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from stupid_drone.stupid_drone_si import StupidDroneSI
from ts4lib.utils.resilent_injections.injection_utility import InjectionUtility

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'stupid_drone_inj')
log.enable()
log.info("Stupid Drone is starting (INJ)...")



class StupidDroneInjections:
    def __init__(self):
        rv = True
        # class SuperInteraction:
        # def cancel(self, finishing_type, cancel_reason_msg, **kwargs):
        #            0     1               2                  {'immediate': False, 'ignore_must_run': False, 'carry_cancel_override': None}
        # args             0               1
        rv = rv & InjectionUtility.check_signature(ModInfo.get_identity(), SuperInteraction, SuperInteraction.cancel.__name__, {'cancel_reason_msg': (2, 'str')})

        # class CommonSimSpawnUtils
        # def soft_reset(cls, sim_info: SimInfo, reset_reason: ResetReason = ResetReason.RESET_EXPECTED, hard_reset_on_exception: bool = False, source: Any = None, cause: str = 'S4CL Soft Reset') -> bool:
        #                -    0                  1                                                       2                                      3                   4
        # args           -    0                  1                                                       2                                      3                   4
        rv = rv & InjectionUtility.check_signature(ModInfo.get_identity(), CommonSimSpawnUtils, CommonSimSpawnUtils.soft_reset.__name__, {'sim_info': (0, 'SimInfo'), 'cause': (4, str)})

        # class CommonSimSpawnUtils
        # def hard_reset(cls, sim_info: SimInfo, reset_reason: ResetReason = ResetReason.RESET_EXPECTED, source: Any = None, cause: str = 'S4CL Hard Reset') -> bool:
        #                -    0                  1                                                       2                   3
        # args           -    0                  1                                                       2                   3
        rv = rv & InjectionUtility.check_signature(ModInfo.get_identity(), CommonSimSpawnUtils, CommonSimSpawnUtils.hard_reset.__name__, {'sim_info': (0, SimInfo), 'cause': (3, str)})

        if rv:
            self.inject()
        else:
            log.warn(f"Method signatures changed. Mod partially disabled itself.")

        import inspect
        method = CommonSimSpawnUtils.hard_reset
        if hasattr(method, "__func__"):
            method = method.__func__
        else:
            method = method.__name__
        # method = getattr(CommonSimSpawnUtils, CommonSimSpawnUtils.soft_reset.__func__)
        log.debug(f"method = {method}: {type(method)}")
        sig = inspect.signature(method)
        log.debug(f"sig = {sig}: {type(sig)}")
        params = list(sig.parameters.values())
        names = [p.name for p in params]
        log.debug(f"names = {names}: {type(names)}")

    def inject(self):
        pass

    @staticmethod
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CommonSimSpawnUtils, CommonSimSpawnUtils.soft_reset.__name__)
    def o19_inj_reset_soft(original, cls, *args, **kwargs):
        return StupidDroneSI().handle_reset_soft(original, cls, *args, **kwargs)

    @staticmethod
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CommonSimSpawnUtils, CommonSimSpawnUtils.hard_reset.__name__)
    def o19_inj_reset_hard(original, cls, *args, **kwargs):
        return StupidDroneSI().handle_reset_hard(original, cls, *args, **kwargs)

    @staticmethod
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SuperInteraction, SuperInteraction.cancel.__name__)
    def o19_inj_si_cancel(original, self, *args, **kwargs):
        return StupidDroneSI().handle_cancel_si(original, self, *args, **kwargs)


StupidDroneInjections()