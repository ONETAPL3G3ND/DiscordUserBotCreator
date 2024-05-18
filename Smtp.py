import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message

class CustomMessageHandler(Message):
    async def handle_DATA(self, server, session, envelope):
        print('Message from:', envelope.mail_from)
        print('Message to  :', envelope.rcpt_tos)
        print('Message data:')
        print(envelope.content.decode('utf8', errors='replace'))
        print('End of message')
        return '250 Message accepted for delivery'

if __name__ == '__main__':
    handler = CustomMessageHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=25)
    controller.start()

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()
