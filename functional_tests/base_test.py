from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class BaseFunctionalTest(StaticLiveServerTestCase):
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

    def allocate_new_browser(self):
        if self.browser:
            self.browser.quit()
        self.browser = webdriver.Firefox()
