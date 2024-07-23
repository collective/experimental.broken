"""Broken Interfaces Handling"""

from ZODB.interfaces import IBroken

from zope.component import persistentregistry

from experimental.broken import interface

orig_registry = persistentregistry.PersistentAdapterRegistry.__setstate__
PersistentComponents = persistentregistry.PersistentComponents

def rebuildBrokenRegisrations(iface, broken_iface, components):
    for reg_iface, comps in components.items():
        if reg_iface is None or isinstance(reg_iface, unicode):
            # We've reached the registration name or handler level
            return
        if reg_iface is iface:
            components[broken_iface] = components.pop(reg_iface)
        rebuildBrokenRegisrations(iface, broken_iface, comps)


def registry_setstate(self, state):
    provided = state['_provided']
    for iface, order in provided.items():
        broken_iface = interface.rebuildBrokenInterface(iface)
        if broken_iface.extends(IBroken):
            provided[broken_iface] = provided.pop(iface)

            for registry in ('_adapters', '_subscribers'):
                byorder = state[registry]
                for components in byorder:
                    rebuildBrokenRegisrations(iface, broken_iface, components)

    return orig_registry(self, state)


def components_setstate(self, state):
    registrations = state['_adapter_registrations']
    for key, value in registrations.items():
        required, provided, name = key
        broken = False

        required = list(required)
        for idx, iface in enumerate(required):
            iface = interface.rebuildBrokenInterface(iface)
            if iface.extends(IBroken):
                required[idx] = iface
                broken = True
        required = tuple(required)

        provided = interface.rebuildBrokenInterface(provided)
        if provided.extends(IBroken):
            broken = True

        if broken:
            registrations[(required, provided, name)] = registrations.pop(key)

    registrations = state['_utility_registrations']
    for key, value in registrations.items():
        provided, name = key
        provided = interface.rebuildBrokenInterface(provided)
        if provided.extends(IBroken):
            registrations[(provided, name)] = registrations.pop(key)

    registrations = state['_subscription_registrations']
    for index, (required, provided, name, factory, info
                ) in enumerate(registrations):
        broken = False

        required = list(required)
        for idx, iface in enumerate(required):
            iface = interface.rebuildBrokenInterface(iface)
            if iface.extends(IBroken):
                required[idx] = iface
                broken = True
        required = tuple(required)

        provided = interface.rebuildBrokenInterface(provided)
        if provided.extends(IBroken):
            broken = True

        if broken:
            registrations[index] = (required, provided, name, factory, info)

    registrations = state['_handler_registrations']
    for index, (required, name, factory, info) in enumerate(registrations):
        broken = False

        required = list(required)
        for idx, iface in enumerate(required):
            iface = interface.rebuildBrokenInterface(iface)
            if iface.extends(IBroken):
                required[idx] = iface
                broken = True
        required = tuple(required)

        if broken:
            registrations[index] = (required, name, factory, info)

    self.__dict__.update(**state)
