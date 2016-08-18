from unittest2 import TestCase
from ftw.referencewidget.testing import FTW_REFERENCE_FUNCTIONAL_TESTING
from ftw.referencewidget.browser.utils import get_traversal_types
from ftw.referencewidget.browser.utils import get_selectable_types
from ftw.referencewidget.tests.views.form import TestView
from plone.registry.interfaces import IRegistry
from ftw.referencewidget.interfaces import IReferenceSettings
from zope.component import getUtility


class TestWidgetConfig(TestCase):
    layer = FTW_REFERENCE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        self.widget = form.form_instance.widgets['relation']
        self.widget.override = True
        tns = self.portal.portal_properties.site_properties.types_not_searched
        tns = tns + ('Folder',)
        self.portal.portal_properties.site_properties.types_not_searched = tns

    def test_traversable_types_allowed(self):
        self.widget.allow_traversal = ['Folder']

        result = get_traversal_types(self.widget)
        self.assertEquals(1, len(result))
        self.assertEquals(['Folder'], result)

    def test_selectable_types_allowed(self):
        self.widget.selectable = ['Folder']

        result = get_selectable_types(self.widget)
        self.assertEquals(1, len(result))
        self.assertEquals(['Folder'], result)
