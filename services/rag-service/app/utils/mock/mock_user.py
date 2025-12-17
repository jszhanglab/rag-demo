# app/utils/mock/mock_user.py

from uuid import UUID

# TODO mock user
# Upload success mock
MOCK_USER_ID = UUID('00000000-0000-0000-0000-000000000001')

# Upload fail mock
MOCK_USER_ID_FAIL = UUID('10000000-0000-0000-0000-000000000001')

def get_current_user():
    return MOCK_USER_ID
