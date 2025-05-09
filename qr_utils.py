# qr_utils.py

import qrcode
from PIL import Image
from io import BytesIO

def generate_upi_qr(user_name, amount, operation_type="Withdraw"):
    """
    Generates a simulated UPI QR code for a transaction.

    Parameters:
    - user_name (str): Name of the user
    - amount (float): Transaction amount
    - operation_type (str): Type of transaction ("Withdraw")

    Returns:
    - BytesIO: In-memory image object of the generated QR code
    """

    # Simulate UPI string
    upi_id = f"{user_name.lower()}@upi"
    upi_payload = f"upi://pay?pa={upi_id}&pn={user_name}&am={amount}&cu=INR&tn={operation_type}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to BytesIO
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
