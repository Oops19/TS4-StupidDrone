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
from stupid_drone.stupid_drone_mem import StupidDroneMemory
from ts4lib.utils.resilent_injections.argument_updater import ArgumentsUpdater
from ts4lib.utils.resilent_injections.injection_utility import InjectionUtility
from ts4lib.utils.singleton import Singleton

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'stupid_drone_si')
log.enable()
log.info("Stupid Drone is starting (SI)...")


class StupidDroneSI:
    def __init__(self):
        self.mem = StupidDroneMemory()


    def handle_reset_hard(self, original, _cls, *args, **kwargs):
        # def hard_reset(cls, sim_info: SimInfo, reset_reason: ResetReason = ResetReason.RESET_EXPECTED, source: Any = None, cause: str = 'S4CL Hard Reset') -> bool:

        def get_args(items: List[int], xargs) -> Union[None, List[Any]]:
            """
            Returns a list of 1-n items if possible or None
            :param items: 'args' Index of the items to return, in this order
            :param xargs: The 'args'
            :return:None if there are not enough 'args', else a list with the values of the args.
            """
            low = min(items)
            high = max(items)
            log.debug(f"{low} ... {items} ... {high} ... {xargs}")
            if low >= 0 and high <= len(args):
                log.debug(f"ok")
                rv: List[Any] = []
                for i in items:
                    rv.append(xargs[i])
                    log.debug(f"xxx {i} = {xargs[i]}")
                log.debug(f"get_args.rv = {rv}")
                return rv
            log.debug(f"get_args.rv = None")
            return None

        log.debug(f"hard_reset()")
        log.debug(f"hard_reset({_cls}; {args}; {kwargs}")
        for arg in args:
            log.debug(f"\targ {arg}: {type(arg)}")
        for k, v in kwargs.items():
            log.debug(f"\tkwarg {k} = {v}: {type(v)}")

        _args = ArgumentsUpdater.get_args([0, ], args)
        log.debug(f"ArgumentsUpdater._args = {_args}")
        _args = get_args([0, ], args)
        log.debug(f"_args = {_args}")

        if _args is None:
            log.debug(f"hard_reset(sim_info missing) ... skipping")
            sim_info = args[0]
            log.debug(f"hard_reset({sim_info}")
            # return original(*args, **kwargs)
        else:
            sim_info = _args[0]
        sim = CommonSimUtils.get_sim_instance(sim_info)
        si_state = getattr(sim, 'si_state', None)
        if si_state is None:
            log.debug(f"hard_reset(si_state missing) ... skipping")
            return original(*args, **kwargs)

        log.debug(f"si_state = {si_state}: {type(si_state)}")
        for interaction in si_state:
            log.debug(f"interaction = {interaction}: {type(interaction)}")

            on_reset = getattr(interaction, 'on_reset', (lambda: None))
            org_reset = getattr(interaction, 'org_reset', None)

            if org_reset is None:
                setattr(interaction, 'org_reset', on_reset)
                setattr(interaction, 'on_reset', (lambda: None))
                StupidDroneMemory().interactions.add(interaction)
                StupidDroneMemory().sim_info = sim_info

                log.debug(f"interaction.on_reset patched")
        rv = True
        try:
            rv = original(*args, **kwargs)
        except Exception as e:
            log.error(f"OOPS o19_inj_reset_hard {e}")
        finally:
            # restore on_reset
            for interaction in StupidDroneMemory().interactions:
                org_reset = getattr(interaction, 'org_reset', None)
                setattr(interaction, 'on_reset', org_reset)
                log.debug(f"interaction.on_reset restored")
            StupidDroneMemory().interactions = set()
            StupidDroneMemory().sim_info = None

        log.debug(f"hard_reset() -> DONE")
        return rv

    def handle_reset_soft(self, original, _cls, *args, **kwargs):
        # def soft_reset(cls, sim_info: SimInfo, reset_reason: ResetReason = ResetReason.RESET_EXPECTED, hard_reset_on_exception: bool = False, source: Any = None, cause: str = 'S4CL Soft Reset') -> bool:
        log.debug(f"soft_reset()")
        rv = self.handle_reset_hard(original, _cls, *args, **kwargs)
        log.debug(f"soft_reset() -> DONE")
        return rv


    def handle_cancel_si(self, original, _self, *args, **kwargs):
        # def cancel(self, finishing_type, cancel_reason_msg, **kwargs):
        log.debug(f"handle_cancel_si({_self}: {type(_self)}; {args}; {kwargs}")  # class: sims4.tuning.instances.
        if StupidDroneMemory().sim_info is None:
            return original(_self, *args, **kwargs)

        for arg in args:
            log.debug(f"\targ {arg}: {type(arg)}")
        for k, v in kwargs.items():
            log.debug(f"\tkwarg {k} = {v}: {type(v)}")
        return False


        #     if len(ctrl.args) > 2 and ("Drone" in str(ctrl.args[0])) and ("DC" in str(ctrl.args[2])):
        #       return False  # seems to be the default to return
        # self.do_skip_call()
        # sim_info = getattr(self, 'sim_info', None)  # AttributeError: 'sim-stand' object has no attribute 'sim_info'
        # log.debug(f"sim_info = {sim_info}: {type(sim_info)}")

        if len(StupidDroneMemory().interactions) > 0:
            # return False  # not successful
            return True  # confirm success ??
        return original(_self, *args, **kwargs)  # run cancel


    #@staticmethod
    #@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CommonSimSpawnUtils, CommonSimSpawnUtils.soft_reset.__name__)
    def old_o19_inj_reset_soft(original, cls, *args, **kwargs):
        def get_args(items: List[int], xargs) -> Union[None, List[Any]]:
            """
            Returns a list of 1-n items if possible or None
            :param items: 'args' Index of the items to return, in this order
            :param xargs: The 'args'
            :return:None if there are not enough 'args', else a list with the values of the args.
            """
            low = min(items)
            high = max(items)
            log.debug(f"{low} ... {items} ... {high} ... {xargs}")
            if low >= 0 and high <= len(args):
                log.debug(f"ok")
                rv: List[Any] = []
                for i in items:
                    rv.append(xargs[i])
                    log.debug(f"xxx {i} = {xargs[i]}")
                log.debug(f"get_args.rv = {rv}")
                return rv
            log.debug(f"get_args.rv = None")
            return None
        log.debug(f"soft_reset()")
        log.debug(f"soft_reset({cls}; {args}; {kwargs}")
        for arg in args:
            log.debug(f"\targ {arg}: {type(arg)}")
        for k, v in kwargs.items():
            log.debug(f"\tkwarg {k} = {v}: {type(v)}")

        # _args = ArgumentsUpdater.get_args([0, ], args)
        _args = get_args([0, ], args)
        if _args is None:
            log.debug(f"soft_reset(sim_info missing) ... skipping")
            sim_info = args[0]
            log.debug(f"soft_reset({sim_info}")
            # return original(*args, **kwargs)
        else:
            sim_info = _args[0]
        sim = CommonSimUtils.get_sim_instance(sim_info)

        si_state = getattr(sim, 'si_state', None)
        if not None:
            log.debug(f"soft_reset(si_state missing) ... skipping")
            return original(*args, **kwargs)

        log.debug(f"si_state = {si_state}: {type(si_state)}")
        for interaction in si_state:
            log.debug(f"interaction = {interaction}: {type(interaction)}")

            on_reset = getattr(interaction, 'on_reset', (lambda: None))
            org_reset = getattr(interaction, 'org_reset', None)

            if org_reset is None:
                setattr(interaction, 'org_reset', on_reset)
                setattr(interaction, 'on_reset', (lambda: None))
                StupidDroneMemory().interactions.add(interaction)
                StupidDroneMemory().sim_info = sim_info
                log.debug(f"interaction.on_reset patched")

        rv = True
        try:
            rv = original(*args, **kwargs)
        except Exception as e:
            log.error(f"OOPS soft_reset {e}")
        finally:
            # restore on_reset
            for interaction in StupidDroneMemory().interactions:
                org_reset = getattr(interaction, 'on_reset', None)
                setattr(interaction, 'on_reset', org_reset)
                log.debug(f"interaction.on_reset restored")
            StupidDroneMemory().interactions = set()
        return rv

    #@staticmethod
    #@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CommonSimSpawnUtils, CommonSimSpawnUtils.hard_reset.__name__)
    def old_o19_inj_reset_hard(original, cls, *args, **kwargs):
        def get_args(items: List[int], xargs) -> Union[None, List[Any]]:
            """
            Returns a list of 1-n items if possible or None
            :param items: 'args' Index of the items to return, in this order
            :param xargs: The 'args'
            :return:None if there are not enough 'args', else a list with the values of the args.
            """
            low = min(items)
            high = max(items)
            log.debug(f"{low} ... {items} ... {high} ... {xargs}")
            if low >= 0 and high <= len(args):
                log.debug(f"ok")
                rv: List[Any] = []
                for i in items:
                    rv.append(xargs[i])
                    log.debug(f"xxx {i} = {xargs[i]}")
                log.debug(f"get_args.rv = {rv}")
                return rv
            log.debug(f"get_args.rv = None")
            return None


        log.debug(f"hard_reset()")
        log.debug(f"hard_reset({cls}; {args}; {kwargs}")
        for arg in args:
            log.debug(f"\targ {arg}: {type(arg)}")
        for k, v in kwargs.items():
            log.debug(f"\tkwarg {k} = {v}: {type(v)}")

        # _args = ArgumentsUpdater.get_args([0, ], args)
        _args = get_args([0, ], args)
        if _args is None:
            log.debug(f"hard_reset(sim_info missing) ... skipping")
            sim_info = args[0]
            log.debug(f"hard_reset({sim_info}")
            # return original(*args, **kwargs)
        else:
            sim_info = _args[0]
        sim = CommonSimUtils.get_sim_instance(sim_info)
        si_state = getattr(sim, 'si_state', None)
        if si_state is None:
            log.debug(f"soft_reset(si_state missing) ... skipping")
            return original(*args, **kwargs)

        log.debug(f"si_state = {si_state}: {type(si_state)}")
        for interaction in si_state:
            log.debug(f"interaction = {interaction}: {type(interaction)}")

            on_reset = getattr(interaction, 'on_reset', (lambda: None))
            org_reset = getattr(interaction, 'org_reset', None)

            if org_reset is None:
                setattr(interaction, 'org_reset', on_reset)
                setattr(interaction, 'on_reset', (lambda: None))
                StupidDroneMemory().interactions.add(interaction)
                StupidDroneMemory().sim_info = sim_info

                log.debug(f"interaction.on_reset patched")
        rv = True
        try:
            rv = original(*args, **kwargs)
        except Exception as e:
            log.error(f"OOPS o19_inj_reset_hard {e}")
        finally:
            # restore on_reset
            for interaction in StupidDroneMemory().interactions:
                org_reset = getattr(interaction, 'on_reset', None)
                setattr(interaction, 'on_reset', org_reset)
                log.debug(f"interaction.on_reset restored")
            StupidDroneMemory().interactions = set()

        return rv



    #         from turbolib2.wrappers.sim.internal import _TurboSimInternalMixin
    #         injector.wrap_function(_TurboSimInternalMixin, 'soft_reset', observe_key='_TurboSimInternalMixin#soft_reset')
    #         injector.before('_TurboSimInternalMixin#soft_reset', start_turbo)
    #         injector.after('_TurboSimInternalMixin#soft_reset', end_turbo)
    # CommonSimSpawnUtils.hard_reset(sim_info, source=self.mod_identity.name, cause='DC: Starting animation runner')
    #         self._si_state = SIState(self)
    # SIState(self)
    #   def on_reset(self):
    #     self = ctrl.args[0]
    #     sim = self.get_sim_instance()
    #     if sim is not None and sim.si_state is not None:
    #         for int in sim.si_state:
    #             int.orig_on_reset = int.on_reset
    #             int.on_reset = (lambda: None)
    #             turbo_tracker.saved_interactions.add(int)
    # def end_turbo(obs, val, ctrl):
    #     self = ctrl.args[0]
    #     sim = self.get_sim_instance()
    #     if sim is not None and sim.si_state is not None:
    #         for int in turbo_tracker.saved_interactions:
    #             int.on_reset = int.orig_on_reset
    #             sim.si_state._super_interactions.add(int)

    #@staticmethod
    #@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SuperInteraction, SuperInteraction.cancel.__name__)
    def old_o19_inj_si_cancel(original, self, *args, **kwargs):
        log.debug(f"o19_inj_si_cancel({self}: {type(self)}; {args}; {kwargs}")
        for arg in args:
            log.debug(f"\targ {arg}: {type(arg)}")
        for k, v in kwargs.items():
            log.debug(f"\tkwarg {k} = {v}: {type(v)}")

        #     if len(ctrl.args) > 2 and ("Drone" in str(ctrl.args[0])) and ("DC" in str(ctrl.args[2])):
        #       return False  # seems to be the default to return
        # self.do_skip_call()
        sim_info = getattr(self, 'sim_info', None)  # AttributeError: 'sim-stand' object has no attribute 'sim_info'

        log.debug(f"sim_info = {sim_info}: {type(sim_info)}")

        if len(StupidDroneMemory().interactions) > 0:
            # return False  # not successful
            return True  # confirm success
        return original(self, *args, **kwargs)  # run cancel



