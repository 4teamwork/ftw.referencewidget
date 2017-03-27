from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.tests import FunctionalTestCase
from ftw.testbrowser import browsing
import json
import transaction


class TestRelatedItemsReplacement(FunctionalTestCase):

    def setUp(self):
        super(TestRelatedItemsReplacement, self).setUp()
        self.setup_fti()
        self.grant('Manager')

    @browsing
    def test_relateditems_behavior_with_one_item(self, browser):
        folder = create(Builder('folder').titled(u'Some folder'))

        content = create(Builder('sample content').titled(u'Sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Items': folder})
        browser.find_button_by_label('Save').click()

        self.assertEquals(
            [folder],
            [relation.to_object for relation in content.relatedItems])

    @browsing
    def test_relateditems_behavior_with_multiple_items(self, browser):
        folder1 = create(Builder('folder').titled(u'Some folder'))
        folder2 = create(Builder('folder').titled(u'Some folder'))

        content = create(Builder('sample content').titled(u'Sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Items': [folder1, folder2]})
        browser.find_button_by_label('Save').click()

        self.assertEquals(
            [folder1, folder2],
            [relation.to_object for relation in content.relatedItems])

    @browsing
    def test_relateditems_with_removed_relation(self, browser):
        folder1 = create(Builder('folder').titled(u'Some folder'))
        folder2 = create(Builder('folder').titled(u'Some folder'))

        content = create(Builder('sample content')
                         .titled(u'Sample content')
                         .having(relatedItems=[folder1, folder2]))

        self.portal.manage_delObjects([folder2.getId()])
        transaction.commit()

        browser.login().visit(content, view='@@edit')

        self.assertEquals(
            [folder1, None],
            [relation.to_object for relation in content.relatedItems])

        selected = json.loads(browser.css(
            '.selected_items').first.attrib['data-select'])
        self.assertEquals(1, len(selected), 'Expect only one item')
        self.assertEquals(['/'.join(folder1.getPhysicalPath())],
                          [item['path'] for item in selected])
