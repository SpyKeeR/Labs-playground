# Challenge 22 : Linux GPG Encryption

**Difficulté** : Niveau 2  
**Domaine** : GPG/PGP, Cryptographie, Data Security, Encryption/Decryption  
**Date** : 17 janvier 2026

---

## 📋 Présentation

**Objectif** : Chiffrer et déchiffrer des données confidentielles avec GPG (GNU Privacy Guard) en utilisant clés publique/privée.

**Contexte** : xFusionCorp Industries doit transférer des données confidentielles vers un site distant. Ces données doivent être chiffrées avant envoi. Inversement, des données reçues (chiffrées) doivent être déchiffrées pour comprendre leur contenu.

**Requirements** :

1. **Clés GPG disponibles** :
   - Clé publique : `/home/public_key.asc`
   - Clé privée : `/home/private_key.asc`
   - User ID : `kodekloud@kodekloud.com`
   - Passphrase : `kodekloud` (pour chiffrement/déchiffrement)

2. **Encryption** :
   - Fichier source : `/home/encrypt_me.txt`
   - Fichier chiffré : `/home/encrypted_me.asc`

3. **Decryption** :
   - Fichier chiffré : `/home/decrypt_me.asc`
   - Fichier déchiffré : `/home/decrypted_me.txt`

**Serveur** :
- **Storage Server** : `ststor01` (user `natasha`)

---

## ⚙️ Réalisation

### Étape 1 : Connexion Storage Server

```bash
ssh natasha@ststor01
```

### Étape 2 : Navigation répertoire /home

```bash
cd /home
ls -la
```

**Fichiers présents** :
```
public_key.asc       # Clé publique GPG
private_key.asc      # Clé privée GPG
encrypt_me.txt       # Fichier à chiffrer
decrypt_me.asc       # Fichier chiffré à déchiffrer
```

### Étape 3 : Import clés GPG

**Import clé publique** :
```bash
gpg --import public_key.asc
```

**Output attendu** :
```
gpg: key XXXXXXXX: public key "kodekloud <kodekloud@kodekloud.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1
```

**Import clé privée** :
```bash
gpg --import private_key.asc
```

**Output attendu** :
```
gpg: key XXXXXXXX: secret key imported
gpg: Total number processed: 1
gpg:       secret keys read: 1
gpg:   secret keys imported: 1
```

**Vérifier clés importées** :
```bash
gpg --list-keys
```

**Output attendu** :
```
/home/natasha/.gnupg/pubring.kbx
--------------------------------
pub   rsa2048 2026-01-17 [SC]
      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
uid           [ unknown] kodekloud <kodekloud@kodekloud.com>
sub   rsa2048 2026-01-17 [E]
```

```bash
gpg --list-secret-keys
```

**Output attendu** :
```
/home/natasha/.gnupg/pubring.kbx
--------------------------------
sec   rsa2048 2026-01-17 [SC]
      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
uid           [ unknown] kodekloud <kodekloud@kodekloud.com>
ssb   rsa2048 2026-01-17 [E]
```

### Étape 4 : Encryption (chiffrer encrypt_me.txt)

```bash
gpg -o /home/natasha/encrypted_me.asc -r kodekloud@kodekloud.com -e encrypt_me.txt
```

**Explication options** :
- `-o` : Output file (destination fichier chiffré)
- `-r` : Recipient (user ID clé publique - destinataire)
- `-e` : Encrypt (mode chiffrement)

**⚠️ Note** : Fichier chiffré créé dans `/home/natasha/` (home directory user natasha).

**Déplacer vers /home** :
```bash
sudo mv /home/natasha/encrypted_me.asc /home/
```

**Vérifier** :
```bash
ls -l /home/encrypted_me.asc
```

**Output attendu** :
```
-rw-r--r-- 1 root root XXX Jan 17 10:00 /home/encrypted_me.asc
```

### Étape 5 : Decryption (déchiffrer decrypt_me.asc)

```bash
gpg -o /home/natasha/decrypted_me.txt -r kodekloud@kodekloud.com -d decrypt_me.asc
```

**Prompt passphrase** :
```
gpg: encrypted with 2048-bit RSA key, ID XXXXXXXX, created 2026-01-17
      "kodekloud <kodekloud@kodekloud.com>"
Enter passphrase:
```

**Enter passphrase** : `kodekloud`

**Output attendu** :
```
gpg: encrypted with 2048-bit RSA key, ID XXXXXXXX, created 2026-01-17
      "kodekloud <kodekloud@kodekloud.com>"
```

**Déplacer vers /home** :
```bash
sudo mv /home/natasha/decrypted_me.txt /home/
```

**Vérifier** :
```bash
ls -l /home/decrypted_me.txt
```

**Output attendu** :
```
-rw-r--r-- 1 root root XXX Jan 17 10:00 /home/decrypted_me.txt
```

### Étape 6 : Validation finale

**Vérifier fichiers créés** :
```bash
ls -l /home/*.asc /home/*.txt
```

**Output attendu** :
```
-rw-r--r-- 1 root root XXX Jan 17 10:00 /home/decrypted_me.txt     # ✅ Créé
-rw-r--r-- 1 root root XXX Jan 17 09:00 /home/decrypt_me.asc       # Original
-rw-r--r-- 1 root root XXX Jan 17 10:00 /home/encrypted_me.asc     # ✅ Créé
-rw-r--r-- 1 root root XXX Jan 17 09:00 /home/encrypt_me.txt       # Original
```

**Lire contenu déchiffré** :
```bash
cat /home/decrypted_me.txt
```

**⚠️ Contenu encrypted_me.asc illisible** (binaire chiffré) :
```bash
cat /home/encrypted_me.asc
# Output : Binary data, caractères illisibles
```

---

## 🔍 Commandes utiles

### GPG Keys Management

```bash
# Lister clés publiques
gpg --list-keys
gpg -k  # Alias

# Lister clés privées (secret keys)
gpg --list-secret-keys
gpg -K  # Alias

# Import clé (publique ou privée)
gpg --import keyfile.asc

# Export clé publique
gpg --export -a "User Name" > public.key
gpg --export -a kodekloud@kodekloud.com > public.key

# Export clé privée (SENSIBLE)
gpg --export-secret-keys -a "User Name" > private.key

# Supprimer clé publique
gpg --delete-keys "User Name"

# Supprimer clé privée
gpg --delete-secret-keys "User Name"

# Générer nouvelle paire clés
gpg --full-generate-key
# Prompts : Type (RSA), Keysize (2048/4096), Expiration, Name, Email, Passphrase
```

### Encryption / Decryption

```bash
# Chiffrer fichier (recipient)
gpg -e -r user@example.com file.txt
# Output : file.txt.gpg (binaire)

# Chiffrer + output ASCII armor
gpg -e -a -r user@example.com file.txt
# Output : file.txt.asc (texte base64)

# Chiffrer + spécifier output file
gpg -o encrypted.asc -e -r user@example.com file.txt

# Déchiffrer fichier
gpg -d file.txt.gpg > file.txt
# Demande passphrase si clé privée protégée

# Déchiffrer + output file
gpg -o decrypted.txt -d file.txt.gpg

# Chiffrement symétrique (password uniquement, pas clés)
gpg -c file.txt
# Demande password 2x, output : file.txt.gpg

# Déchiffrer symétrique
gpg -d file.txt.gpg > file.txt
# Demande password
```

---

## 📝 Points clés

### GPG (GNU Privacy Guard)

**Concept** : Implémentation open source standard OpenPGP (RFC 4880).

**Use cases** :
- **Encryption** : Chiffrer emails, fichiers sensibles (passwords, données clients)
- **Signatures** : Authentifier authorship fichiers (packages Linux, commits Git)
- **Authentication** : Prouver identité (SSH via gpg-agent)

**Alternatives** :
- **PGP** : Pretty Good Privacy (commercial, original)
- **Age** : Modern encryption tool (simpler que GPG)
- **OpenSSL** : Crypto général (pas spécifique email/files)

### Public Key Cryptography (Asymmetric)

**Principe** : 2 clés mathématiquement liées, usage différent.

**Clé publique** :
- Distribuer librement (email, keyserver, website)
- **Usage** : Chiffrer messages POUR vous, vérifier VOS signatures
- **Analogie** : Cadenas ouvert (tout le monde peut fermer)

**Clé privée** :
- SECRÈTE (JAMAIS partager)
- Protégée passphrase (recommandé)
- **Usage** : Déchiffrer messages pour VOUS, créer VOS signatures
- **Analogie** : Clé unique (seul vous pouvez ouvrir)

**Workflow encryption** :
1. Alice veut envoyer message secret à Bob
2. Alice récupère **clé publique Bob** (keyserver, email)
3. Alice chiffre message avec **clé publique Bob** → ciphertext
4. Alice envoie ciphertext à Bob (interception OK, illisible)
5. Bob déchiffre ciphertext avec **clé privée Bob** → plaintext

**Propriété clé** : Message chiffré avec clé publique Bob → SEULE clé privée Bob peut déchiffrer.

---

## 🎯 Tags

`GPG`, `GnuPG`, `PGP`, `Encryption`, `Decryption`, `Public-Key-Cryptography`, `Asymmetric-Encryption`, `Data-Security`, `Privacy`, `Cryptography`