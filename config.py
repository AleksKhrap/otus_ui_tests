class Settings:
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "Admin123!"

    FAILURE_ID: int = 999999999
    API_USER: str = "admin"
    API_PASSWORD: str = "password123"

    def get_admin_creds(self):
        return self.ADMIN_EMAIL, self.ADMIN_PASSWORD


settings = Settings()
