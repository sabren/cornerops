
Duckbill GPG setup.
-------------------

Duckbill requires GnuPGInterface to
encrypt credit cards.

Running the tests requires generating a
fake private key with a hard coded
passphrase.

Here's how to generate the private key 
for the encryption tests:

[~]: gpg --gen-key

- Please select what kind of key you want:
  (1) DSA and ElGamal (default)

- What keysize do you want? 
  (1024)

- Please specify how long the key should be valid.
  0 = key does not expire


Real name: Duckbill Test Key
Email address: encrypted.card.test@sabren.com
Passphrase: encrypted card test

