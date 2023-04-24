import tkinter
import tkinter as tk
import smtplib
from tkinter import filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from email.utils import COMMASPACE
from email import encoders
import mimetypes

import tkinter.messagebox as mb

class MailApp:
    def __init__(self, master):
        self.attachments, self.images = [], []
        self.master = master
        master.title("G-Mail Application")
        tkinter.Tk.config(master, background="lightgray")

        # Create the UI
        self.from_label = tk.Label(master, text="From:       ", background="lightgray")
        self.from_label.grid(row=0, column=0, sticky="w", padx=5)
        self.from_entry = tk.Entry(master, width=50)
        self.from_entry.grid(row=0, column=1, sticky="w", pady=10)

        self.pass_label = tk.Label(master, text="App Password:       ", background="lightgray")
        self.pass_label.grid(row=1, column=0, sticky="w", padx=5)
        self.pass_entry = tk.Entry(master, width=50, show="*")
        self.pass_entry.grid(row=1, column=1, sticky="w", pady=10)

        self.to_label = tk.Label(master, text="To:        ", background="lightgray")
        self.to_label.grid(row=2, column=0, sticky="w", padx=5)
        self.to_entry = tk.Entry(master, width=50)
        self.to_entry.grid(row=2, column=1, sticky="w", pady=10)

        self.subject_label = tk.Label(master, text="Subject:     ", background="lightgray")
        self.subject_label.grid(row=3, column=0, sticky="w", padx=5)
        self.subject_entry = tk.Entry(master, width=50)
        self.subject_entry.grid(row=3, column=1, sticky="w", pady=10)

        self.body_label = tk.Label(master, text="Body:     ", background="lightgray")
        self.body_label.grid(row=4, column=0, sticky="w", padx=5)
        self.body_text = tk.Text(master, height=6, width=50)
        self.body_text.grid(row=4, column=1, sticky="w", pady=20)

        self.add_file_button = tk.Button(master, text="Add File", command=self.add_file, width=16,
                                     background="lightgreen", foreground="White", font=8)
        self.add_file_button.grid(row=5, column=0, sticky="w", padx=20)

        self.add_image_button = tk.Button(master, text="Add Image", command=self.add_image, width=16,
                                      background="lightgreen", foreground="White", font=8)
        self.add_image_button.grid(row=5, column=1, sticky="w", padx=20)

        self.send_button = tk.Button(master, text="Send", command=self.send_mail, width=16,
                                     background="Purple", foreground="White", font=8)
        self.send_button.grid(row=5, column=1, sticky="w", padx=200)

    def add_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("Text files", "*.txt, *.docx, *.mp4, *.mp3,*.pdf"), ("all files", "*.*")))
        if filename:
            self.attachments.append(filename)
            mb.showinfo("file", "File Uploaded")
            
    def add_image(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select image",
                                              filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("all files", "*.*")))
        if filename:
            self.images.append(filename)
            mb.showinfo("image", "image uploaded")
            
    def send_mail(self):
        # Get the mail details from the UI
        sender = self.from_entry.get()
        password = self.pass_entry.get()
        recipient = self.to_entry.get()
        subject = self.subject_entry.get()
        body = self.body_text.get('1.0', 'end')
        mb.showinfo("mail", "mail sent")

        # Create the message object
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Add attachments
        for attachment in self.attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attachment, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=attachment)
            message.attach(part)
        # MIME types for common image file extensions


        # Add images
        for image in self.images:
            IMAGE_TYPES = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp',
                '.ico': 'image/x-icon',
            }

            with open(image, 'rb') as f:
                img_data = f.read()
            ext = os.path.splitext(image)[-1].lower()
            if ext in IMAGE_TYPES:
                image_type = IMAGE_TYPES[ext]
            else:
                image_type, _ = mimetypes.guess_type(image)
            part = MIMEImage(img_data, image_type)
            part.add_header('Content-Disposition', 'attachment', filename=image)
            message.attach(part)

        # Connect to the SMTP server and send the message
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, COMMASPACE.join([recipient]), message.as_string())
        smtp_server.quit()

        # Reset the UI after sending the email
        self.from_entry.delete(0, 'end')
        self.pass_entry.delete(0, 'end')
        self.to_entry.delete(0, 'end')
        self.subject_entry.delete(0, 'end')
        self.body_text.delete('1.0', 'end')
        self.attachments = []
        self.images = []
root = tk.Tk()
mail_app = MailApp(root)
root.geometry("550x350")
root.mainloop()