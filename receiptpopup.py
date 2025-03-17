from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog
from PyQt6.QtGui import QPixmap
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class ReceiptPopup(QDialog):
    def __init__(self, parent, transaction_details):
        super().__init__(parent)
        self.setWindowTitle("Receipt")
        self.transaction_details = transaction_details
        
        layout = QVBoxLayout()
        self.receipt_label = QLabel(self.format_receipt_text())
        layout.addWidget(self.receipt_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email to send receipt")
        layout.addWidget(self.email_input)
        
        self.download_btn = QPushButton("Download PDF")
        self.download_btn.clicked.connect(self.download_receipt)
        layout.addWidget(self.download_btn)
        
        self.send_email_btn = QPushButton("Send Email")
        self.send_email_btn.clicked.connect(self.send_email)
        layout.addWidget(self.send_email_btn)
        
        self.setLayout(layout)

    def format_receipt_text(self):
        receipt_text = "\n".join([f"{key}: {value}" for key, value in self.transaction_details.items()])
        return receipt_text

    def generate_pdf(self, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Receipt", ln=True, align='C')
        pdf.ln(10)
        
        for key, value in self.transaction_details.items():
            pdf.cell(200, 10, f"{key}: {value}", ln=True)
        
        pdf.output(filename)

    def download_receipt(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Receipt", "receipt.pdf", "PDF Files (*.pdf)")
        if filename:
            self.generate_pdf(filename)
            print("✅ Receipt saved successfully!")

    def send_email(self):
        recipient_email = self.email_input.text().strip()
        if not recipient_email:
            print("⚠️ Please enter an email address!")
            return

        pdf_filename = "receipt.pdf"
        self.generate_pdf(pdf_filename)

        sender_email = "your_email@example.com"
        sender_password = "your_password"
        smtp_server = "smtp.example.com"
        smtp_port = 587
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Your Receipt"
        
        body = "Please find your receipt attached."
        msg.attach(MIMEText(body, 'plain'))
        
        attachment = open(pdf_filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={pdf_filename}")
        msg.attach(part)
        attachment.close()
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            print("✅ Email sent successfully!")
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
        
        os.remove(pdf_filename)  # Remove temporary file after sending
