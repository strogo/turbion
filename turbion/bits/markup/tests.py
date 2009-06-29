import textwrap

from django.test import TestCase
from turbion.bits.markup import processing

TEMPLATE = """{% block summary %}
summary text
{% endblock %}
more text
"""

class ProcessingTest(TestCase):
    def test_render(self):
        self.assertEqual(
            processing.render_string(TEMPLATE),
            textwrap.dedent("""
            summary text

            more text
            """)
        )

    def test_extract_block(self):
        self.assertEqual(
            processing.extract_block(TEMPLATE, 'summary'),
            """summary text
            """.strip('\n ')
        )

    def test_restrincted_tag(self):
        from django import template
        self.assertRaises(
            template.TemplateSyntaxError,
            processing.render_string,
            "{% for i in foobar %}{% endfor %}"
        )
