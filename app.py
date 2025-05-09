import streamlit as st
import pandas as pd
import datetime
import os
from voice_auth import recognize_speech, convert_digits_to_words, speak_text, recognize_operation
from qr_utils import generate_upi_qr
import time

# ---------------- Session state setup ----------------

if "spoken_pin" not in st.session_state:
    st.session_state.spoken_pin = ""
if "current_user_pin" not in st.session_state:
    st.session_state.current_user_pin = None
if "selected_operation" not in st.session_state:
    st.session_state.selected_operation = "Balance Enquiry"
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default page is login

# ---------------- Helper Functions ----------------

def get_transaction_file(pin):
    return f"transactions_{pin}.csv"

def load_transactions(pin):
    file_path = get_transaction_file(pin)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["Date", "Type", "Amount", "Balance"])

def save_transaction(pin, date, trans_type, amount, balance):
    file_path = get_transaction_file(pin)
    df = load_transactions(pin)
    new_row = pd.DataFrame([[date, trans_type, amount, balance]], columns=["Date", "Type", "Amount", "Balance"])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(file_path, index=False)

def detect_lang(text):
    if text in ["बैलेंस", "जमा", "निकासी", "पासबुक", "बंद"]:
        return 'hi'
    elif text in ["ಹಣ ಠೇವಣಿ", "ಹಣ ವಾಪಸಾತಿ", "ಪಾಸ್‌ಬುಕ್", "ಹಾರಿ"]:
        return 'kn'
    return 'en'

# ---------------- Page config and title ----------------

st.set_page_config(page_title="ATM Voice Assistant", layout="centered")

# ---------------- Page 1: Login ----------------

if st.session_state.page == "login":
    st.title("🗣 ATM Voice Assistant")
    st.subheader("Enter or Speak your 4-digit PIN")
    
    pin_input = st.text_input("PIN", value=st.session_state.spoken_pin, max_chars=4, type="password")
    
    # Button to trigger speech recognition
    if st.button("🎤Speak PIN"):
        with st.spinner("Listening..."):
            speech = recognize_speech()
        if speech:
            digits = ''.join(filter(str.isdigit, speech))
            if len(digits) == 4:
                st.session_state.spoken_pin = digits
                st.success(f"Recognized PIN: {digits}")
                speak_text(f"Recognized PIN: {digits}")
                st.session_state.current_user_pin = digits
                st.rerun()  # Refresh the page to process the PIN
            else:
                st.warning("Please speak exactly 4 digits.")
                speak_text("Please speak exactly four digits")
        else:
            st.error("Speech not recognized.")
            speak_text("Sorry, speech not recognized.")

    # Submit login if PIN is either spoken or manually entered
    if st.button("✅ Submit & Login") or st.session_state.current_user_pin:
        entered_pin = st.session_state.spoken_pin or pin_input
        users = {
            '1712': {'name': 'Sakshi', 'balance': 95000},
            '5678': {'name': 'Amit', 'balance': 5000},
            '0091': {'name': 'Bhanu', 'balance': 15000},
            '1234': {'name': 'Nanditha', 'balance': 500}
        }

        if entered_pin in users:
            st.session_state.current_user_pin = entered_pin
            if not st.session_state.welcome_shown:
                # Display welcome message for 2 seconds
                welcome_message = st.empty()
                welcome_message.success(f"Welcome, {users[entered_pin]['name']}!")
                speak_text(f"Welcome, {users[entered_pin]['name']}!")
                time.sleep(2)  # Wait for 2 seconds
                welcome_message.empty()  # Remove welcome message after 2 seconds
                st.session_state.welcome_shown = True
            st.session_state.page = "operations"  # Navigate to operations page
            st.rerun()  # Refresh the page to load operations
        else:
            st.error("Invalid PIN.")
            speak_text("Invalid PIN entered.")

# ---------------- Page 2: Operations ----------------

if st.session_state.page == "operations":
    pin = st.session_state.current_user_pin
    users = {
        '1712': {'name': 'Sakshi', 'balance': 95000},
        '5678': {'name': 'Amit', 'balance': 5000},
        '0091': {'name': 'Bhanu', 'balance': 15000},
        '1234': {'name': 'Nanditha', 'balance': 500}
    }

    user = users[pin]
    transactions = load_transactions(pin)

    if not transactions.empty:
        last_balance = transactions.iloc[-1]['Balance']
        try:
            user['balance'] = float(last_balance)
        except:
            user['balance'] = users[pin].get('balance', 0)

    st.subheader("🏦 ATM Operations")
    op_options = [
        "Balance Enquiry", "Deposit", "Withdraw", "Passbook", "Exit",
        "बैलेंस", "जमा", "निकासी", "पासबुक", "बंद",
        "ಹಣ ಠೇವಣಿ", "ಹಣ ವಾಪಸಾತಿ", "ಪಾಸ್‌ಬುಕ್", "ಹಾರಿ"
    ]

    operation = st.selectbox("Choose an operation", op_options,
                             index=op_options.index(st.session_state.selected_operation))

    amount = None
    if operation in ["Deposit", "Withdraw", "जमा", "निकासी", "ಹಣ ಠೇವಣಿ", "ಹಣ ವಾಪಸಾತಿ"]:
        amount = st.number_input("Enter amount", min_value=1, step=1)

    if st.button("🎤 Speak Operation"):
        with st.spinner("Listening for operation..."):
            spoken_op = recognize_operation()
        if spoken_op:
            st.session_state.selected_operation = spoken_op
            speak_text(f"{spoken_op} selected")
            st.rerun()  # Rerun the page to update the operation selection
        else:
            st.warning("Could not recognize operation.")
            speak_text("Sorry, I couldn't understand.")

    if st.button("✅ Proceed"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lang = detect_lang(operation)

        if operation in ["Balance Enquiry", "बैलेंस", "ಬ್ಯಾಲೆನ್ಸ್"]:
            msg = f"Your balance is ₹{user['balance']}."
            st.info(msg)
            speak_text(msg if lang == 'en' else
                       f"आपका बैलेंस ₹{user['balance']} है।" if lang == 'hi' else
                       f"ನಿಮ್ಮ ಶೇಷದ ಮೊತ್ತ ₹{user['balance']} ಆಗಿದೆ.", lang)

        elif operation in ["Deposit", "जमा", "ಹಣ ಠೇವಣಿ"]:
            if amount is not None:
                user['balance'] += amount
                save_transaction(pin, now, "Deposit", amount, user['balance'])
                msg = f"₹{amount} deposited. New balance is ₹{user['balance']}."
                st.success(msg)
                speak_text(msg if lang == 'en' else
                           f"₹{amount} जमा किए गए। नया बैलेंस ₹{user['balance']} है।" if lang == 'hi' else
                           f"₹{amount} ಠೇವಳಿ ಮಾಡಲಾಗಿದೆ. ಹೊಸ ಶೇಷ ₹{user['balance']}.", lang)
            else:
                st.warning("Please enter a valid amount.")
                speak_text("Enter a valid amount.", lang)

        elif operation in ["Withdraw", "निकासी", "ಹಣ ವಾಪಸಾತಿ"]:
            if amount is None:
                st.warning("Please enter a valid amount.")
                speak_text("Enter a valid amount.", lang)
            elif amount > user['balance']:
                msg = "Insufficient balance."
                st.error(msg)
                speak_text("बैलेंस अपर्याप्त है।" if lang == 'hi' else
                           "ಶೇಷದ ಮೊತ್ತ ಸಾಕಷ್ಟಿಲ್ಲ." if lang == 'kn' else
                           msg, lang)
            else:
                st.subheader("📱 Scan UPI QR to Simulate Withdrawal")
                qr_img = generate_upi_qr(user['name'], amount, "Withdraw")
                st.image(qr_img, caption="Simulated UPI Payment for Withdrawal", use_column_width=False)

                user['balance'] -= amount
                save_transaction(pin, now, "Withdraw", amount, user['balance'])
                msg = f"₹{amount} withdrawn. New balance is ₹{user['balance']}."
                st.success(msg)
                speak_text(msg if lang == 'en' else
                           f"₹{amount} निकाले गए। नया बैलेंस ₹{user['balance']} है।" if lang == 'hi' else
                           f"₹{amount} ಹಣ ವಾಪಸು ಮಾಡಲಾಗಿದೆ. ಹೊಸ ಶೇಷ ₹{user['balance']} ಆಗಿದೆ.", lang)

        elif operation in ["Passbook", "पासबुक", "ಪಾಸ್‌ಬುಕ್"]:
            st.subheader("📜 Transaction Passbook")
            if not transactions.empty:
                st.dataframe(transactions)
            else:
                st.write("No transactions available.")
            speak_text("Displaying passbook." if lang == 'en' else
                       "पासबुक दिखा रहा हूँ।" if lang == 'hi' else
                       "ಪಾಸ್‌ಬುಕ್ ಪ್ರದರ್ಶಿಸಲಾಗುತ್ತಿದೆ.", lang)

        elif operation in ["Exit", "बंद", "ಹಾರಿ"]:
            st.session_state.page = "login"
            st.session_state.spoken_pin = ""
            st.session_state.current_user_pin = None
            st.experimental_rerun()  # Rerun the app to reset to login page

# ---------------- Final Thoughts ----------------
# Make sure you have the 'voice_auth' module and 'qr_utils' with required functions for speech recognition, conversion, and QR code generation.
