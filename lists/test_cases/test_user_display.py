from django.test import TestCase
from lists.models import Item, List


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_of_that_list(self):
        expected_list = List.objects.create()
        Item.objects.create(text='ExpectedItem1', list=expected_list)
        Item.objects.create(text='ExpectedItem2', list=expected_list)

        other_list = List.objects.create()
        Item.objects.create(text='UnExpectedItem1', list=other_list)
        Item.objects.create(text='UnExpectedItem2', list=other_list)
        response = self.client.get(f'/lists/{expected_list.id}/')
        self.assertContains(response, 'ExpectedItem1')
        self.assertContains(response, 'ExpectedItem2')
        self.assertNotContains(response, 'UnExpectedItem1')
        self.assertNotContains(response, 'UnExpectedItem2')

    def test_passes_correct_list_to_template(self):
        fake_list = List.objects.create()
        expected_list = List.objects.create()

        response = self.client.get(f'/lists/{expected_list.id}/')
        self.assertEqual(response.context['list'], expected_list)

