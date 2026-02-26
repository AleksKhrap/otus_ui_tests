class TestRegistrationPage:
    def test_check_registration_page_availability(self, registration_page):
        registration_page.assert_page_elements_is_visible()

    def test_create_new_user(self, registration_page):
        registration_page.register_new_account()
