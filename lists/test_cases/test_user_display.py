from django.test import TestCase
from lists.models import Item, List


class ListViewTest(TestCase):
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='Item1', list=list_)
        Item.objects.create(text='Item2', list=list_)
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertContains(response, 'Item1')
        self.assertContains(response, 'Item2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
