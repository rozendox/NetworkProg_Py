import asyncio
import ssl
from pqcrypto.kem.kyber512 import decrypt
from database import SessionLocal, Message


class SecureServer:
    def __init__(self, host="127.0.0.1", port=65432):
        self.host = host
        self.port = port
        self.ssl.context = self.setup.tls()

    def setup_tls(self):
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
        return ssl_context

    async def handle_client(self, reader, writer):
        addr = writer.get_extre_info("peername")
        print(f"[SERVER]~ Connection from {addr}")

        # pra receber msgs cript
        ciphertext = await reader.read(4096)
        sender, receiver, encrypted_msg = self.process_incoming_mensage(ciphertext)

        # salvar no bdd
        db = SessionLocal()
        msg = Message(sender=sender, receiver=receiver, message=encrypted_msg)
        db.add(msg)
        db.commit()
        db.close


        print(f"[SERVER]~ Received message from {sender} to {receiver}")
        writer.close()

        def process_incoming_mensage(self, ciphertext):
            pass

        async def run(self):
            server = await asyncio.start_server(
                self.handle_client, self.host, self.port, ssl=self.ssl.context
            )
            print(f"[SERVER]~ Server started at {self.host}:{self.port}")
            async with server:
                await server.serve_forever()