"""
First functional test to verify the environment setup for django development
"""
from selenium.webdriver.common.keys import Keys
from .base_test import BaseFunctionalTest


class MultiUsersTest(BaseFunctionalTest):
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
        self.allocate_new_browser()
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
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text, 'Ediths list observed in the browser')
        self.assertIn('Buy milk', page_text, 'Expected content from Francis list is missing')
        # Successfully evaluated the functionality

