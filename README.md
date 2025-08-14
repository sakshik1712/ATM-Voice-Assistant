# ATM Voice Assistant

A **Streamlit-based Voice-Enabled ATM Simulation** that allows users to interact with an ATM using **voice PIN input** in **English, Hindi, and Kannada**. The project demonstrates how AI-powered speech recognition can be applied in financial systems to enhance accessibility and security.

Demo:  http://localhost:8501
---

##  Features
-  **Voice PIN Authentication** – Supports English, Hindi, and Kannada number recognition.  
-  **Autofill PIN Entry** – Automatically fills in the PIN when correctly spoken.  
-  **Banking Operations** – Deposit, Withdraw, Balance Enquiry, Passbook, and Exit options.  
-  **Transaction Reports** – Generates PDF reports and sends via email.  
-  **UPI QR Code Simulation** – Simulated QR codes for deposits/withdrawals.  
-  **Multilingual Support** – Enhances accessibility for regional users.  

---

## Tech Stack
- **Frontend:** Streamlit  
- **Speech Recognition:** Google Speech Recognition API  
- **Backend:** Python  
- **Libraries:** `speechrecognition`, `streamlit`, `qrcode`, `fpdf`, `smtplib`

---

## ⚡ Getting Started
1. Clone the repository:  
   ```bash
   git clone https://github.com/sakshik1712/ATM-Voice-Assistant.git
   cd ATM-Voice-Assistant
   pip install -r requirements.txt
   streamlit run app.py

## Future Enhancements
Face recognition login for added security
Mobile app integration
Support for more Indian languages


## License
This project is licensed under the MIT License.
