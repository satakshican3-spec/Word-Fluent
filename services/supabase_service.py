import streamlit as st
from supabase import Client, create_client


CLIENT_STATE_KEY = "_wordfluent_supabase_client"


def get_supabase_client() -> Client:
    if CLIENT_STATE_KEY not in st.session_state:
        try:
            project_url = st.secrets[
                "SUPABASE_URL"
            ].strip()

            publishable_key = st.secrets[
                "SUPABASE_PUBLISHABLE_KEY"
            ].strip()
        except KeyError as error:
            raise RuntimeError(
                "Supabase connection details are missing."
            ) from error

        if not project_url or not publishable_key:
            raise RuntimeError(
                "Supabase connection details are empty."
            )

        st.session_state[CLIENT_STATE_KEY] = create_client(
            project_url,
            publishable_key,
        )

    return st.session_state[CLIENT_STATE_KEY]


def register_user(
    email,
    password,
    display_name,
    birth_year,
):
    client = get_supabase_client()

    return client.auth.sign_up(
        {
            "email": email.strip().lower(),
            "password": password,
            "options": {
                "data": {
                    "display_name": display_name.strip(),
                    "birth_year": int(birth_year),
                }
            },
        }
    )


def login_user(email, password):
    client = get_supabase_client()

    return client.auth.sign_in_with_password(
        {
            "email": email.strip().lower(),
            "password": password,
        }
    )


def logout_user():
    client = get_supabase_client()
    client.auth.sign_out()

    st.session_state.pop(
        CLIENT_STATE_KEY,
        None,
    )


def get_current_session():
    client = get_supabase_client()
    return client.auth.get_session()


def fetch_profile(user_id):
    client = get_supabase_client()

    response = (
        client.table("profiles")
        .select("*")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


def fetch_language_progress(user_id):
    client = get_supabase_client()

    response = (
        client.table("language_progress")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    return response.data or []


def save_profile(profile_data):
    client = get_supabase_client()

    return (
        client.table("profiles")
        .upsert(
            profile_data,
            on_conflict="id",
        )
        .execute()
    )


def save_language_progress(progress_data):
    client = get_supabase_client()

    return (
        client.table("language_progress")
        .upsert(
            progress_data,
            on_conflict="user_id,language",
        )
        .execute()
    )