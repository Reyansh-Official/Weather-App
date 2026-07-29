from app.core.database import get_db

def test_supabase_connection():
    try:
        db = get_db()

        response = db.table("weather_history").select("*").order("created_at", desc=True).execute()

        # Verifies that response.data is a valid list (even if it's empty, it shouldn't be None)
        assert response.data is not None, "The database returned a null response!"

    except Exception as e:
        assert False, f"Database connection failed: {e}"

