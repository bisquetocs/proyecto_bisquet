from django.test import TestCase

# Create your tests here.
class NewInventoryTests(TestCase):
    # OUTPUT TEST CASES
    def test_user_register_product_output_with_negative_amount(self):
        """
            If the user tries to resgister an output of a product, and the amount
            is a negative value , the registration will fail
        """
        # TODO:
        return True


    def test_user_register_product_output_more_than_the_inventory_has(self):
        """
            If the user tries to resgister an output of a product, and the amount
            is bigger than what they have on the inventory, the registration will
            fail
        """
        # TODO:
        return True

    def test_user_register_a_correct_output(self):
        """
            If the user tries to register an output of a product, and it passess
            all the parameters, the registration will continue in a correct way
        """
        # TODO:
        return True


#---------------------------------------------------------------------------------------------------
    #INPUT TEST CASES
    def test_user_register_product_output_with_negative_amount(self):
        """
            If the user tries to resgister an output of a product, and the amount
            is a negative value , the registration will fail
        """
        # TODO:
        return True


    def test_user_register_product_output_more_than_the_inventory_has(self):
        """
            If the user tries to resgister an output of a product, and the amount
            is bigger than what they have on the inventory, the registration will
            fail
        """
        # TODO:
        return True

    def test_user_register_a_correct_output(self):
        """
            If the user tries to register an output of a product, and it passess
            all the parameters, the registration will continue in a correct way
        """
        # TODO:
        return True

#---------------------------------------------------------------------------------------------------
    #CONSULT INPUT/OUTPUT CASES
    def test_user_consult_io_reports(self):
        """
            If the user makes a request to consult all the inputs/outputs and
            registration of new products, the system will display a table of the
            mentioned inventory movements
        """
        # TODO:
        return True
