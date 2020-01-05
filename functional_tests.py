"""
First functional test to verify the environment setup for django development
"""
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')
assert 'Django' in browser.title
