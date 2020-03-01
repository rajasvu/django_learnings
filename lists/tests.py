from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    def test_home_page_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 0, 'Item saved during get request to home page')

    def test_can_save_a_post_request(self):
        response = self.client.post('/', data={'todo_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1, 'Persisted items mismatch')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item', 'Item content mismatch')

    def test_redirects_after_post_request(self):
        response = self.client.post('/', data={'todo_text': 'A new list item'})
        self.assertEqual(response.status_code, 302, 'Redirection failed')
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2, 'Persistance of items failed')
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item', 'First saved item did not match')
        self.assertEqual(second_saved_item.text, 'The second item', 'second saved item did not match')


class ListViewTest(TestCase):
    def test_displays_all_items(self):
        Item.objects.create(text='Item1')
        Item.objects.create(text='Item2')
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertContains(response, 'Item1')
        self.assertContains(response, 'Item2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
