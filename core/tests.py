from django.test import TestCase
from django.template import Context, Template

class TemplateIncludesTest(TestCase):
    def test_base_includes_header_and_footer(self):
        tpl = Template("{% load static %}{% include 'includes/header.html' %}{% include 'includes/footer.html' %}")
        rendered = tpl.render(Context({}))
        self.assertIn("CEPAC", rendered)
        self.assertIn("Contact", rendered)
