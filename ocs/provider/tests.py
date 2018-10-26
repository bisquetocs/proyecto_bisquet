import datetime

from django.test import TestCase
from django.utils import timezone

from .models import LinkWithF


# Create your tests here.
class LinkWithFTests(TestCase):

    def test_code_has_already_expired(self):
        """
            Test case for check_timeout() which returns False for codes that
            had already expired
            INPUT
                - Self
            OUTPUT
                - A boolean value indicating if the test has already passed
        """
        time = timezone.now() + datetime.timedelta(days=-7)
        passed_link_code = LinkWithF(date_of_creation=time)
        self.assertIs(passed_link_code.check_timeout(), False)
