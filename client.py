import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import tkinter as tk
import os.path


LOGGED_EMAIL = "email@example.com"


def send_email(email_recipient,
               email_subject,
               email_message,
               attachment_location=''):

    msg = MIMEMultipart()
    msg['From'] = LOGGED_EMAIL
    msg['To'] = email_recipient
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_message, 'plain'))

    if attachment_location != '':
        filename = os.path.basename(attachment_location)
        attachment = open(attachment_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()
        server.starttls()
        server.login(LOGGED_EMAIL, 'password') #recommended to save password in a pickled file
        text = msg.as_string()
        server.sendmail(LOGGED_EMAIL, email_recipient, text)
        server.quit()
    except:
        print("SMPT server connection error")
    return True


def main():
    window = tk.Tk()
    window.title("Email Client v2.0")

    def update_email():
        with open("emails.txt", "w") as file:
            file.write(email_list.get(1.0,"end-1c"))
            file.close()

    def send_mail():
        subject = email_sub.get()
        message = mail.get(1.0, "end-1c")
        with open("emails.txt") as file:
            for address in file:
                send_email(address, subject, message)
                email_sent.config(text=f"Successfully sent to {address}")
            email_sent.config(text=f"Successfully sent all emails.")
            file.close()


    email_sub_text = tk.Label(text="Enter Email Subject")
    email_sub = tk.Entry(width=100)
    main_message = tk.Label(text="Enter Email Content")
    email_list_text = tk.Label(text="Email List")

    mail = tk.Text(window, height=20, width=100)
    email_list = tk.Text(window, height=20, width=30)
    logged_user = tk.Label(text=f"logged in as {LOGGED_EMAIL}")

    with open("emails.txt") as file:
        for email in file:
            email_list.insert("1.0",email)
        file.close()

    send_email_button = tk.Button(window, text="Send",command=send_mail)
    change_email_button = tk.Button(window, text="Update", command=update_email)

    email_sent = tk.Label(window, text="")

    email_sub_text.grid(row=0, column=0)
    logged_user.grid(row=0, column=4)
    email_sub.grid(row=1, column=0)
    main_message.grid(row=2, column=0)
    mail.grid(row=3, column=0,padx=10, pady=10, columnspan=3)
    send_email_button.grid(row=5, column=0, pady=1)
    change_email_button.grid(row=5, column=4, pady=1)
    email_list_text.grid(row=2, column=4,)
    email_list.grid(row=3, column=4,padx=10, pady=10)
    email_sent.grid()
    window.mainloop()

main()
