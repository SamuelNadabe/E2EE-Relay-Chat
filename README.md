# 🛡️ E2EE Terminal Chat (Zero-Knowledge Relay)

> A lightweight, high-performance terminal messaging system with End-to-End Encryption (E2EE).

This project demonstrates core networking concepts and applied cryptography. It uses a **Client/Server** architecture where the server acts purely as a "Zero-Knowledge Relay"—routing packets without ever reading the message contents. 

## 🧠 How it Works

1. **Client-Side Encryption:** When a user types a message, it is encrypted locally using an AES-128 key (Fernet). This key is derived from a shared "Room Password" using PBKDF2 (SHA-256).
2. **Zero-Knowledge Routing:** The encrypted payload is sent to the central Relay Server.
3. **Broadcasting:** The server forwards the encrypted bytes to all other connected clients.
4. **Client-Side Decryption:** The receiving clients use their local derived key to decrypt and display the message.

### Architecture Flow

```mermaid
graph TD
    A[Client 1\n🔑 Local Key] -->|Encrypted Bytes| S((Relay Server\nBlind Router))
    S -->|Encrypted Bytes| B[Client 2\n🔑 Local Key]
    S -->|Encrypted Bytes| C[Client 3\n🔑 Local Key]
    
    style S fill:#2d3436,stroke:#636e72,stroke-width:2px,color:#fff
    style A fill:#0984e3,stroke:#74b9ff,stroke-width:2px,color:#fff
    style B fill:#0984e3,stroke:#74b9ff,stroke-width:2px,color:#fff
    style C fill:#0984e3,stroke:#74b9ff,stroke-width:2px,color:#fff