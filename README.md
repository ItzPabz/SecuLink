# VaultTalk - Encrypted Messaging App
VaultTalk is a secure and user-friendly encrypted messaging application developed in Python. It provides end-to-end encryption to protect your conversations from prying eyes. This is/was a school project, and I have no plans to continue development; no support will be offered either.

## Features
- **End-to-End Encryption**: Your messages are encrypted on your device and decrypted only on the recipient's device.
- **User-Friendly Interface**: Easy-to-use, intuitive user interface for seamless communication.
- **Cross-Platform**: VaultTalk is available on Windows, macOS, and Linux.

## School Presentation 
As mentioned, this is a school project, and below, I have added an outline of the slides and the information on the slides for a tad bit more information.

### RSA Encryption
#### What is it?
- RSA encryption is a type of asymmetric encryption using two different linked keys to increase security among messaging apps.

#### Why is it important?
- It allows the user to secure a message before sending it to the recipient, enhancing basic security measures in daily life.

#### How is it implemented?
- Using a public key that everyone knows encrypts the message, which can only be decrypted with the private key in a certain amount of time.

### RSA Padding
#### What is RSA Padding?
- A technique used in RSA encryption to ensure security
- Adds random bytes to plaintext message before encryption
  - This helps prevent Chosen Ciphertext Attacks
    - Method where attackers attempt to decrypt ciphertext
  - This randomness makes each encrypted message unique
    - Even if the plaintext message is the same

#### How is RSA Padding Used?
- Uses specifically OAEP (Optimal Asymmetric Encryption Padding)
  - Provides randomness & integrity checking
- How it works in the App
  1. The message is encrypted using a public key
  2. It uses MGF1 as the padding scheme and SHA256 as the hash
  3. The encrypted message is then sent to the client
- The process ensures the message is encrypted 

### Demo Video

WORK IN PROGRESS

