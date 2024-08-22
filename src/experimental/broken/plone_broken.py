"""
Plone-dependent broken object support.
"""

from plone import api
from plone.portlets import interfaces as portlet_ifaces
from zope import component


def cleanup_broken_portlets(context):
    """
    A GenericSetup upgrade step for unregistering broken portlet types.

    Specifically, portlet types whose code has been removed.
    """
    site_manager = component.getSiteManager()
    portal = api.portal.get()
    addviewbase = "++contextportlets++plone.leftcolumn"
    for name, portlet_type in component.getUtilitiesFor(portlet_ifaces.IPortletType):
        addview = "{0}/+/{1}".format(addviewbase, portlet_type.addview)
        if portal.unrestrictedTraverse(addview, None) is None:
            site_manager.unregisterUtility(
                component=portlet_type, provided=portlet_ifaces.IPortletType, name=name
            )
