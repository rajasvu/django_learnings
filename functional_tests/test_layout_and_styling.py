from .base_test import BaseFunctionalTest
from selenium.webdriver.common.keys import Keys


class PageLayoutTest(BaseFunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to her homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # She notices that input box is well centered
        input_box = self.browser.find_element_by_id('todo_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=10)
        # She starts a new list and sees input is nicely centered there too
        input_box.send_keys('testing')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: testing')
        input_box = self.browser.find_element_by_id('todo_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=10)
