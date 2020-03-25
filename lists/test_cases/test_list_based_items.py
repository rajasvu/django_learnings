from django.test import TestCase
from lists.models import Item


class NewListTest(TestCase):
    def test_can_save_a_post_request(self):
        self.client.post('/lists/new', data={'todo_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1, 'Persisted items mismatch')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item', 'Item content mismatch')

    def test_redirects_after_post_request(self):
        response = self.client.post('/lists/new', data={'todo_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
