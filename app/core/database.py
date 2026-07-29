from app.core.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
from supabase import create_client, Client


def get_db() -> Client:
    # 1. Error boundary: Make sure keys aren't empty strings or None
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("Missing Supabase environmental variables.")

    # 2. Return the active, authenticated connection client
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

