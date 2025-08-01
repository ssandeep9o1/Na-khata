# In get_token.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# --- FILL IN THESE FOUR VALUES ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "password"
# ------------------------------------

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Sign in as the test user
    response = supabase.auth.sign_in_with_password({
        "email": "one@gmail.com",
        "password": "123"
    })

    # Get the JWT (access token) from the session
    jwt_token = response.session.access_token

    print("\n--- COPY YOUR TOKEN BELOW ---\n")
    print(jwt_token)
    print("\n---------------------------\n")

except Exception as e:
    print(f"An error occurred: {e}")