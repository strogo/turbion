import textwrap

from django.test import TestCase
from turbion.core.utils.markup import processing

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
