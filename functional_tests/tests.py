"""
First functional test to verify the environment setup for django development
"""
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_table(self, item_to_check):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('todo_list_table')
                todo_records = table.find_elements_by_tag_name('tr')
                self.assertIn(item_to_check, [todo_record.text for todo_record in todo_records])
                return
            except(AssertionError, WebDriverException) as ex:
                if time.time() - start_time > MAX_WAIT:
                    raise ex
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('todo_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        # She types "Buy peacock feathers" into a text box (Edith's hobby is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')
        # When she hits enter, the page updates, and now the page lists
        inputbox.send_keys(Keys.ENTER)
        # "1: Buy peacock feathers" as an item in a to-do list
        self.wait_for_row_in_table(item_to_check='1: Buy peacock feathers')
        # There is still a text box inviting her to add another item
        # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('todo_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_table(item_to_check='1: Buy peacock feathers')
        self.wait_for_row_in_table(item_to_check='2: Use peacock feathers to make a fly')
        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('todo_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table(item_to_check='1: Buy peacock feathers')
        # She notices that her list has new URL
        edith_url = self.browser.current_url
        self.assertRegex(edith_url, '/lists/.+', 'URL mismatch for Edith')
        # Now a new user Francis comes along the site
        # We use a new browser session to ensure none of Edith's information is coming through cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()
        # Francis visits the page and there is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text, 'Ediths list observed in the browser')
        # Francis starts new list by entering a new item
        inputbox = self.browser.find_element_by_id('todo_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table(item_to_check='1: Buy milk')
        # Francis gets his own URL
        francis_url = self.browser.current_url
        self.assertRegex(francis_url, '/lists/.+', 'URL mismatch for Francis')
        self.assertNotEqual(edith_url, francis_url, 'Same URL used for both the users')
        # Again there is no trace of Edith's list
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text, 'Ediths list observed in the browser')
        self.assertIn('But milk', page_text, 'Expected content from Francis list is missing')
        # Successfully evaluated the functionality

