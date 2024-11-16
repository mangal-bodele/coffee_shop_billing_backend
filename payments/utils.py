from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO

def generate_invoice_pdf(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Coffee Shop Info
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 750, "Coffee Shop Name")
    p.setFont("Helvetica", 10)
    p.drawString(100, 735, "123 Coffee Street")
    p.drawString(100, 725, "Coffee City, CO 12345")
    p.drawString(100, 715, "Phone: (123) 456-7890")
    p.drawString(100, 705, "Email: info@coffeeshop.com")

    # Invoice Info
    p.setFont("Helvetica-Bold", 12)
    p.drawString(400, 750, f"Invoice #: {order.id}")
    p.drawString(400, 735, f"Invoice Date: {order.invoice_date}")
    p.drawString(400, 720, f"Due Date: {order.due_date}")

    # Customer Info
    p.setFont("Helvetica", 10)
    p.drawString(100, 680, f"Bill To: {order.customer_name}")
    p.drawString(100, 670, f"Address: {order.customer_address}")
    p.drawString(100, 660, f"Email: {order.customer_email}")

    # Coffee Item Details Table
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, 620, "Item Description")
    p.drawString(300, 620, "Quantity")
    p.drawString(400, 620, "Unit Price")
    p.drawString(500, 620, "Amount")

    p.setFont("Helvetica", 10)
    y_position = 600
    for item in order.items:
        p.drawString(100, y_position, item.name)
        p.drawString(300, y_position, str(item.quantity))
        p.drawString(400, y_position, f"INR {item.price}")
        p.drawString(500, y_position, f"INR {item.total_price}")
        y_position -= 20

    # Total Amount
    p.setFont("Helvetica-Bold", 12)
    p.drawString(400, y_position - 20, f"Total Amount: INR {order.total_amount}")

    # Payment Terms
    p.setFont("Helvetica", 10)
    p.drawString(100, y_position - 40, "Payment Terms: Due upon receipt.")
    p.drawString(100, y_position - 55, "For inquiries, please contact us at info@coffeeshop.com.")

    # Footer with bank details
    p.setFont("Helvetica", 10)
    p.drawString(100, y_position - 75, "Bank Details: Bank Name, Account No: XXXXXXXXXX")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
