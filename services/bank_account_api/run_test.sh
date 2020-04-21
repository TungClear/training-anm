APP_SETTINGS=api.config.TestingConfig python -m unittest tests/TestAuthorization.py
APP_SETTINGS=api.config.TestingConfig python -m unittest tests/TestLogin.py
APP_SETTINGS=api.config.TestingConfig python -m unittest tests/TestCreateAccount.py
APP_SETTINGS=api.config.TestingConfig python -m unittest tests/TestDeleteAccount.py
APP_SETTINGS=api.config.TestingConfig python -m unittest tests/TestGetAccount.py
APP_SETTINGS=api.config.TestingConfig python -m unittest tests/TestInvalidRequestUrl.py
APP_SETTINGS=api.config.TestingConfig python -m unittest tests/TestUpdateAccount.py
APP_SETTINGS=api.config.TestingConfig python -m unittest tests/TestValidBodyPayload.py
