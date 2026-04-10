# Day 12 : The Life of a Packet

**Date** : 8 janvier 2026  
**Plateforme** : Jeremy's IT Lab - CCNA 200-301  
**Cours Udemy** : Master Cisco CCNA 200-301  

---

## 🎯 Objectif

Comprendre le processus complet de communication réseau entre deux hôtes (ARP, ICMP, IP, routing).

---

## 📋 Cours : Life of a Packet

**Scénario** : PC1 (`192.168.1.10`) ping PC2 (`192.168.2.10`) via routeur R1.

### Étapes communication

**1. PC1 vérifie destination**
- IP destination (`192.168.2.10`) dans réseau local ? **Non** (différent subnet)
- → Envoyer vers gateway (R1 : `192.168.1.1`)

**2. ARP Request (si cache vide)**
- PC1 cherche MAC address gateway R1
- Broadcast ARP : "Qui a IP `192.168.1.1` ?"
- R1 répond (ARP Reply) : "Moi, MAC `aa:bb:cc:dd:ee:ff`"
- PC1 enregistre dans ARP cache

**3. Encapsulation ICMP**
- PC1 crée paquet ICMP Echo Request
- Couche IP : Source `192.168.1.10`, Destination `192.168.2.10`
- Couche Ethernet : Source MAC PC1, Destination MAC R1 (gateway)

**4. Routeur R1 traite**
- Reçoit frame Ethernet (destination MAC = soi-même)
- Désencapsule : lit IP destination (`192.168.2.10`)
- Consulte table routing : route vers `192.168.2.0/24` via G0/1 (directly connected)
- Ré-encapsule : Nouvelle frame Ethernet (Source MAC R1 G0/1, Destination MAC PC2)

**5. ARP Request R1 → PC2 (si cache vide)**
- R1 cherche MAC address PC2 (`192.168.2.10`)
- Broadcast ARP sur réseau `192.168.2.0/24`
- PC2 répond avec sa MAC address

**6. PC2 reçoit ICMP Echo Request**
- Traite paquet
- Génère ICMP Echo Reply (inverse source/destination)

**7. Retour (processus inverse)**
- PC2 → R1 (gateway)
- R1 route vers `192.168.1.0/24`
- R1 → PC1

**8. PC1 reçoit ICMP Echo Reply**
- Ping réussi ✅

---

## 💡 Notes

- **ARP** : Résolution IP → MAC (Layer 2)
- **ICMP** : Protocol diagnostic (ping, traceroute)
- **Routing** : Décision Layer 3 (table routing, next-hop)
- **Encapsulation** : Données traversent couches OSI (Application → Physical)

**Rien de nouveau** : Révision concepts déjà acquis (ARP process, ICMP, routing basics).

---

## 🏷️ Tags

`#CCNA` `#Networking` `#ARP` `#ICMP` `#Routing` `#OSI` `#PacketFlow` `#JeremyIT`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud
