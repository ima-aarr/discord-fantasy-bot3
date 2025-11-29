import os
BOT_OWNER_ID = os.getenv('BOT_OWNER_ID')  # expected to be string of numeric discord id
def is_owner(user_id):
    try:
        return BOT_OWNER_ID is not None and str(user_id) == str(BOT_OWNER_ID)
    except Exception:
        return False
