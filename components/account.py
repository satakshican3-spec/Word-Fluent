from datetime import datetime

import streamlit as st

from core.account_sync import (
    load_online_state,
    reset_to_guest_state,
    save_online_state,
)
from services.supabase_service import (
    login_user,
    logout_user,
    register_user,
)


def friendly_error(error):
    message = str(error)
    lowered_message = message.lower()

    known_errors = {
        "invalid login credentials": (
            "The email or password is incorrect."
        ),
        "email not confirmed": (
            "Confirm your email before signing in."
        ),
        "user already registered": (
            "An account already exists with this email."
        ),
        "password should be": (
            "Please choose a stronger password."
        ),
    }

    for error_text, friendly_message in (
        known_errors.items()
    ):
        if error_text in lowered_message:
            return friendly_message

    return (
        "Something went wrong. Check the information "
        "and try again."
    )


def activate_account(auth_response):
    user = auth_response.user

    if user is None:
        raise RuntimeError(
            "Supabase did not return a user."
        )

    st.session_state.guest_mode = False
    st.session_state.authenticated = True
    st.session_state.user_id = user.id
    st.session_state.user_email = user.email

    sync_result = load_online_state(user.id)

    return sync_result


def render_signed_in_account():
    st.title("👤 Your WordFluent account")

    st.success(
        f"Signed in as {st.session_state.display_name}"
    )

    st.write(
        f"**Email:** {st.session_state.user_email}"
    )

    st.info(
        "Your profile is private by default. Your "
        "progress is stored separately for every language."
    )

    save_column, logout_column = st.columns(2)

    with save_column:
        if st.button(
            "Save progress now",
            type="primary",
        ):
            try:
                save_online_state(
                    st.session_state.user_id
                )
                st.success(
                    "Your progress was saved online."
                )
            except Exception as error:
                st.error(friendly_error(error))

    with logout_column:
        if st.button("Sign out"):
            try:
                save_online_state(
                    st.session_state.user_id
                )
                logout_user()
                reset_to_guest_state()
                st.rerun()
            except Exception as error:
                st.error(friendly_error(error))


def render_login_tab():
    st.subheader("Welcome back")

    with st.form("wordfluent_login_form"):
        email = st.text_input(
            "Email",
            key="login_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        submitted = st.form_submit_button(
            "Sign in",
            type="primary",
        )

    if submitted:
        if not email.strip() or not password:
            st.warning(
                "Enter both your email and password."
            )
            return

        try:
            response = login_user(
                email,
                password,
            )

            sync_result = activate_account(response)

            if sync_result == "converted":
                st.session_state.account_notice = (
                    "Signed in. Your guest progress was "
                    "saved to this account."
                )
            else:
                st.session_state.account_notice = (
                    "Signed in. Your online progress "
                    "was restored."
                )

            st.rerun()

        except Exception as error:
            st.error(friendly_error(error))


def render_registration_tab():
    st.subheader("Create an account")

    current_year = datetime.now().year

    with st.form("wordfluent_registration_form"):
        display_name = st.text_input(
            "Display name",
            max_chars=40,
            key="registration_display_name",
        )

        birth_year = st.number_input(
            "Birth year",
            min_value=1900,
            max_value=current_year,
            value=current_year - 18,
            step=1,
            key="registration_birth_year",
        )

        email = st.text_input(
            "Email",
            key="registration_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            help="Use at least 8 characters.",
            key="registration_password",
        )

        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            key="registration_confirm_password",
        )

        submitted = st.form_submit_button(
            "Create account",
            type="primary",
        )

    st.caption(
        "Birth year is used for age-appropriate settings. "
        "New profiles remain private."
    )

    if submitted:
        if not display_name.strip():
            st.warning("Enter a display name.")
            return

        if not email.strip():
            st.warning("Enter an email address.")
            return

        if len(password) < 8:
            st.warning(
                "Your password must contain at least "
                "8 characters."
            )
            return

        if password != confirm_password:
            st.warning("The passwords do not match.")
            return

        try:
            response = register_user(
                email,
                password,
                display_name,
                birth_year,
            )

            if response.session is not None:
                activate_account(response)

                st.session_state.account_notice = (
                    "Your account was created and your "
                    "guest progress was saved."
                )
            else:
                st.session_state.account_notice = (
                    "Account created. Check your email "
                    "and confirm it, then return here "
                    "and sign in."
                )

            st.rerun()

        except Exception as error:
            st.error(friendly_error(error))


def render_account():
    if st.button("← Home", key="account_home"):
        st.session_state.current_view = "Home"
        st.rerun()

    notice = st.session_state.pop(
        "account_notice",
        None,
    )

    if notice:
        st.success(notice)

    if st.session_state.authenticated:
        render_signed_in_account()
        return

    st.title("👤 Account")

    st.info(
        "You are currently using WordFluent as a guest. "
        "Create an account to save your progress online."
    )

    login_tab, registration_tab = st.tabs(
        [
            "Sign in",
            "Create account",
        ]
    )

    with login_tab:
        render_login_tab()

    with registration_tab:
        render_registration_tab()