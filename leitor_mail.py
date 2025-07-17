import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
import google.generativeai as genai # <-- NOVO: Importamos a biblioteca da IA

load_dotenv()

EMAIL = os.getenv('EMAIL')
SENHA = os.getenv('SENHA')
IMAP_SERVER = "imap.gmail.com"

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def get_email_body(msg):
    """Extrai o corpo de texto plano de um objeto de e-mail."""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))
            if ctype == "text/plain" and "attachment" not in cdispo:
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()

def summarize_with_gemini(text):
    """Envia um texto para a API do Gemini e retorna um resumo."""
    if not text or not text.strip():
        return "Não foi possível extrair conteúdo para resumir."
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"Resuma o seguinte texto de e-mail em uma única frase, focando na ação principal ou no assunto central: '{text}'"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Erro ao contatar a IA: {e}"

mail = imaplib.IMAP4_SSL(IMAP_SERVER)

try:
    status, messages = mail.login(EMAIL, SENHA)
    print(f"Login no e-mail {EMAIL} realizado com sucesso!\n")

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
                
                print("-" * 50)
                print(f"De: {from_}")
                print(f"Assunto: {subject}")

                body = get_email_body(msg)
                summary = summarize_with_gemini(body)
                print(f"Resumo IA: {summary}")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    mail.close()
    mail.logout()
    print("\n" + "="*50)
    print("Conexão com o e-mail fechada.")