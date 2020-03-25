from django.test import TestCase
from lists.models import Item, List


class NewListTest(TestCase):
    def test_can_save_a_post_request(self):
        self.client.post('/lists/new', data={'todo_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1, 'Persisted items mismatch')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item', 'Item content mismatch')

    def test_can_save_a_post_to_existing_list(self):
        fake_list = List.objects.create()
        expected_list = List.objects.create()
        self.client.post(f'/lists/{expected_list.id}/add_item', data={'todo_text': 'New item for existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New item for existing list', 'Item content mismatch')
        self.assertEqual(new_item.list, expected_list)

    def test_redirects_after_post_request(self):
        response = self.client.post('/lists/new', data={'todo_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_redirects_to_list_view(self):
        fake_list = List.objects.create()
        expected_list = List.objects.create()
        response = self.client.post(f'/lists/{expected_list.id}/add_item',
                                    data={'todo_text': 'New item for existing list'})
        self.assertRedirects(response, f'/lists/{expected_list.id}/')
