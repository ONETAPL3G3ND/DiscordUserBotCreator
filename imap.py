import imaplib
import email
from email.header import decode_header

email_address = "-"
password = "-"

# Подключение к почтовому серверу Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(email_address, password)

# Выбор папки "INBOX"
mail.select("INBOX")

# Поиск последних писем
result, data = mail.search(None, "ALL")  # Можно изменить "ALL" на "UNSEEN" для получения только непрочитанных писем

# Получение и анализ писем
for num in data[0].split():
    result, data = mail.fetch(num, "(RFC822)")
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Получение заголовка письма
    subject = decode_header(msg["Subject"])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode()

    # Получение отправителя письма
    from_ = decode_header(msg.get("From"))[0][0]
    if isinstance(from_, bytes):
        from_ = from_.decode()

    print("Subject:", subject)
    print("From:", from_)

    # Получение текста письма
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass
            if content_type == "text/plain" and "attachment" not in content_disposition:
                print("Body:", body)
    else:
        body = msg.get_payload(decode=True).decode()
        print("Body:", body)

# Закрытие соединения
mail.close()
mail.logout()
