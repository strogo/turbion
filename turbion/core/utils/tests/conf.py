# -*- coding: utf-8 -*-
from django.test import TestCase

from turbion.conf import GenericConfigurator, Merge

class ConfTest(TestCase):
    def setUp(self):
        application_settings = {
            "SET_1": 1,
            "SET_2": 2,
            "SET_5": Merge(((0, 1), (1, 2), (None, 6)), "SET_6")
        }

        project_settings = {
            "SET_3": 3,
            "SET_6": [3, 4, 5],
            "CONFTEST_SET_7": 7,
        }

        self.conf = GenericConfigurator(application_settings, "CONFTEST_")
        self.result = project_settings.copy()

        self.result.update(
                self.conf.merge_settings(
                    project_settings,
                    **{
                        "SET_4": 4,
                        "set_7": 77
                    }
                )
            )

    def test_existance(self):
        self.assert_("SET_1" in self.result)
        self.assert_("SET_2" in self.result)

        self.assert_("SET_3" in self.result)

        self.assert_("CONFTEST_SET_7" in self.result)
        self.assertEqual(self.result["CONFTEST_SET_7"], 77)

        self.assert_("CONFTEST_SET_4" in self.result)
        self.assert_("SET_5" not in self.result)
        self.assert_("SET_6" in self.result)

    def test_merge(self):
        val = self.result["SET_6"]

        self.assertEqual(
            val,
            [1, 2, 3, 4, 5, 6]
        )
