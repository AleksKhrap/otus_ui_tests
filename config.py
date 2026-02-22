class Settings:
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "Admin123!"

    def get_admin_creds(self):
        return self.ADMIN_EMAIL, self.ADMIN_PASSWORD


settings = Settings()
