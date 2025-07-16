import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv('EMAIL')
SENHA = os.getenv('SENHA')
IMAP_SERVER = "imap.gmail.com"

mail = imaplib.IMAP4_SSL(IMAP_SERVER)

try:
    status, messages = mail.login(EMAIL, SENHA)
    print(f"Login no e-mail {EMAIL} realizado com sucesso!")

    mail.select('inbox')

    status, search_data = mail.search(None, 'UNSEEN')

    for num in search_data[0].split():
        status, fetch_data = mail.fetch(num, '(RFC822)')
        
        for response_part in fetch_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                from_, encoding = decode_header(msg.get("From"))[0]
                if isinstance(from_, bytes):
                    from_ = from_.decode(encoding if encoding else "utf-8")
                
                print("-" * 30)
                print(f"De: {from_}")
                print(f"Assunto: {subject}")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    mail.close()
    mail.logout()
    print("\nConexão com o e-mail fechada.")