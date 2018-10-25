from django.test import TestCase
from .models import LinkWithF

# Create your tests here.
class LinkWithFTests(TestCase):

    def code_has_already_expired(self):
        """
            A test case function checking that the code used to link
            has already expired
            INPUT
                - Self
            OUTPUT
                - A boolean value indicating if the test has already passed
        """
        time = timezone.now() + datetime.timedelta(days=-7)
        passed_link_code = LinkWithF(date_of_creation=time)
        self.assertIs(passed_link_code.check_timeout(), False)
