import streamlit as st
import stripe

# Configure Stripe API key
stripe.api_key = "your-secret-key"  # Replace with your actual secret key

def support_page_2(config):
    # Support page
    st.title(config.translations["support_title"])
    st.write(config.translations["support_text"])

    # Display donation options
    donation_amounts = [10, 25, 50, 100]  # Predefined donation amounts
    selected_amount = st.selectbox(
        config.translations.get("select_donation", "Select Donation Amount"),
        donation_amounts,
        index=0
    )

    # Custom amount input
    custom_amount = st.number_input(
        config.translations.get("custom_donation", "Or Enter Custom Amount"),
        min_value=1.0,
        step=1.0,
        format="%.2f"
    )

    # Use custom amount if provided, otherwise use selected amount
    donation_amount = custom_amount if custom_amount > 0 else selected_amount

    # Collect user email for payment confirmation
    user_email = st.text_input(
        config.translations.get("enter_email", "Enter your email for payment confirmation")
    )

    # Payment button
    if st.button(config.translations.get("make_payment", "Make Payment")):
        if not user_email:
            st.error(config.translations.get("email_required", "Email is required for payment confirmation."))
            return

        try:
            # Create a Stripe Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": config.translations.get("donation", "Donation"),
                            },
                            "unit_amount": int(donation_amount * 100),  # Convert to cents
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url="https://yourwebsite.com/success",  # Replace with your success URL
                cancel_url="https://yourwebsite.com/cancel",      # Replace with your cancel URL
                customer_email=user_email,
            )

            # Redirect user to Stripe Checkout
            st.markdown(
                f'<a href="{checkout_session.url}" target="_blank">Proceed to Payment</a>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

