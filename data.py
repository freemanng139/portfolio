PROFILE = {
    "name": "Ngarmodeng Freeman",
    "short": "Freeman",
    "role": "Étudiant en Sécurité Informatique",
    "roles_typing": ["Licence Pro ICT4D · Sécurité Informatique", "BTS Réseaux & Sécurité", "Administration Système & Réseau", "Sécurité des Infrastructures"],
    "email": "freemanng139@gmail.com",
    "github": "https://github.com/freemanng139",
    "linkedin": "https://www.linkedin.com/in/freemanng139/",
    "whatsapp": "+237 695 984 955",
    "whatsapp_url": "https://wa.me/237695984955",
    "location": "Yaoundé · Cameroun",
    "available": True,
    "bio": (
        "Étudiant en Licence Pro ICT4D option Sécurité Informatique et titulaire d'un BTS Réseaux & Sécurité. "
        "en administration système (Linux, Windows Server), réseaux Cisco et sécurisation d'infrastructures. "
        "Rigoureux et motivé par l'apprentissage continu, je privilégie la compréhension approfondie des protocoles "
        "et la pratique méthodique en laboratoire."
    ),
}

PROJECTS = [
    {
        "slug": "gestion-parc-windows-server-2022",
        "title": "Gestion d’un parc informatique avec Windows Server 2022 — cas de Force Telecoms",
        "icon": "server",
        "category": "systeme",
        "category_label": "Système",
        "summary": "Mise en place et administration d’un environnement informatique basé sur Windows Server 2022.",
        "description": "Mise en place et administration d’un environnement informatique basé sur Windows Server 2022.",
        "stack": ["Windows Server 2022", "AD DS", "DNS", "DHCP", "GPO"],
        "metrics": [("1", "Serveur WS 2022"), ("100%", "Administration centralisée"), ("0", "Compte non tracé")],
        "problem": "Nécessité de structurer, sécuriser et centraliser la gestion des postes et des accès utilisateurs au sein de Force Telecoms.",
        "delivered": [
            "Installation et configuration de Windows Server 2022.",
            "Déploiement des services d'annuaire Active Directory Domain Services (AD DS).",
            "Configuration des services d'infrastructure réseau : DNS et DHCP.",
            "Application des stratégies de groupe (GPO) pour sécuriser et uniformiser le parc.",
        ],
        "decisions": [
            "Centralisation complète des identités et des permissions.",
            "Application stricte du principe du moindre privilège.",
        ],
        "architecture": "Serveur Windows Server 2022 (AD DS, DNS, DHCP, GPO)\n   │\n   └── Postes clients & utilisateurs Force Telecoms",
    },
    {
        "slug": "infrastructure-multisite-fortigate",
        "title": "Conception, déploiement et sécurisation d’une infrastructure réseau multisite avec FortiGate",
        "icon": "shield",
        "category": "reseau",
        "category_label": "Réseau & Sécurité",
        "summary": "Conception et déploiement d’une infrastructure réseau reliant plusieurs sites, avec sécurisation des échanges à l’aide de FortiGate.",
        "description": "Conception et déploiement d’une infrastructure réseau reliant plusieurs sites, avec sécurisation des échanges à l’aide de FortiGate.",
        "stack": ["FortiGate", "VPN IPsec", "VLAN", "Routage", "Pare-feu"],
        "metrics": [("Multi-sites", "Interconnectés"), ("IPsec", "Tunnels chiffrés"), ("UTM", "Inspection des flux")],
        "problem": "Interconnexion sécurisée de plusieurs sites distants pour permettre des échanges fiables et protégés contre les intrusions.",
        "delivered": [
            "Architecture réseau multisite segmentée avec VLAN et routage adapté.",
            "Déploiement et intégration des équipements de sécurité FortiGate.",
            "Mise en place de tunnels VPN IPsec chiffrés pour lier les sites distants.",
            "Définition et application de politiques de sécurité et de filtrage rigoureuses.",
        ],
        "decisions": [
            "Chiffrement systématique des flux intersites via VPN IPsec.",
            "Inspection approfondie du trafic et contrôle d'accès strict.",
        ],
        "architecture": "Site Central (FortiGate) ── Tunnels VPN IPsec ── Sites Distants (FortiGate)\n       │\n   Inspection des flux & Sécurisation périmétrique",
    },
    {
        "slug": "segmentation-reseau-local-vlan",
        "title": "Segmentation d’un réseau local avec VLAN",
        "icon": "network",
        "category": "reseau",
        "category_label": "Réseau",
        "summary": "Conception d’un réseau local segmenté en VLAN, configuration des commutateurs et vérification de la communication entre les segments.",
        "description": "Conception d’un réseau local segmenté en VLAN, configuration des commutateurs et vérification de la communication entre les segments.",
        "stack": ["Cisco IOS", "VLAN", "Trunk 802.1Q", "Inter-VLAN", "Switching"],
        "metrics": [("VLAN", "Segmentation logique"), ("802.1Q", "Liaisons Trunk"), ("100%", "Isolation des flux")],
        "problem": "Nécessité de cloisonner les flux réseau par service pour réduire le domaine de diffusion et renforcer la sécurité interne.",
        "delivered": [
            "Conception du plan d'adressage et segmentation en sous-réseaux logiques.",
            "Création et assignation des VLAN sur commutateurs Cisco.",
            "Configuration des liaisons Trunk (protocole 802.1Q) et du routage inter-VLAN.",
            "Tests de connectivité, d'isolation et vérification de la communication inter-segments.",
        ],
        "decisions": [
            "Isolation stricte des services sensibles du reste des postes utilisateurs.",
            "Optimisation de la bande passante par réduction des tempêtes de broadcast.",
        ],
        "architecture": "Routeur / Passerelle Inter-VLAN\n       │ Trunk 802.1Q\n   Switch Core\n   ├── VLAN 10 (Administration)\n   ├── VLAN 20 (Technique)\n   └── VLAN 30 (Invités)",
    },
    {
        "slug": "deploiement-environnement-virtualisation-services-reseau",
        "title": "Déploiement d’un environnement de virtualisation pour tester des services réseau",
        "icon": "virtual",
        "category": "systeme",
        "category_label": "Virtualisation & Réseau",
        "summary": "Création d’un laboratoire virtuel avec GNS3, EVE-NG ou VMware pour installer et tester des services comme DHCP et DNS",
        "description": "Création d’un laboratoire virtuel avec GNS3, EVE-NG ou VMware pour installer et tester des services comme DHCP et DNS",
        "stack": ["GNS3", "EVE-NG", "VMware", "DHCP", "DNS", "Linux"],
        "metrics": [("Lab", "Environnement isolé"), ("Services", "DHCP & DNS validés"), ("0 risque", "Plateforme de test")],
        "problem": "Besoin d'un bac à sable technique isolé pour valider le bon fonctionnement de services réseau avant toute mise en production.",
        "delivered": [
            "Déploiement et interconnexion de machines virtuelles sous VMware / GNS3 / EVE-NG.",
            "Installation, configuration et test des services réseau fondamentaux (DHCP, DNS).",
            "Mise en place d'un réseau isolé (host-only) pour des expérimentations sécurisées.",
            "Validation de l'attribution dynamique d'adresses et de la résolution de noms.",
        ],
        "decisions": [
            "Isolation réseau complète pour expérimenter sans impacter le réseau réel.",
            "Reproductibilité de l'environnement de test pour futurs déploiements.",
        ],
        "architecture": "Hyperviseur (VMware / EVE-NG / GNS3)\n   ├── Serveur DHCP & DNS (Linux / Windows)\n   └── Clients de test (Ubuntu / Windows)",
    },
]

SKILLS = [
    {
        "title": "Administration système",
        "icon": "server",
        "description": "Installation et gestion de systèmes Linux et Windows, configuration de serveurs et gestion des utilisateurs.",
        "skills": [
            "Ubuntu",
            "Kali Linux",
            "Windows Server",
            "Bash",
        ],
    },
    {
        "title": "Réseaux informatiques",
        "icon": "network",
        "description": "Configuration et simulation de réseaux, adressage IPv4, services réseau et protocoles de routage.",
        "skills": [
            "IPv4",
            "TCP/IP",
            "VLAN",
            "DHCP",
            "DNS",
            "NAT",
        ],
    },
    {
        "title": "Programmation et développement web",
        "icon": "code",
        "description": "Création de programmes et de pages web avec des langages de programmation et des technologies web.",
        "skills": [
            "Python",
            "PHP",
            "SQL",
            "HTML",
            "CSS",
        ],
    },
    {
        "title": "Outils et logiciels",
        "icon": "tools",
        "description": "Analyse de trafic, exploration réseau, administration à distance et simulation d’environnements virtuels.",
        "skills": [
            "Wireshark",
            "PuTTY",
            "GNS3",
            "EVE-NG",
            "VMware",
        ],
    },
]

TIMELINE = [
    ("2024 – Présent", "Formation en Sécurité Informatique — Université de Yaoundé I", "Apprentissage académique : architecture des systèmes, protocoles réseaux, sécurité et cryptographie appliquée."),
    ("2025 – En cours", "Préparation Cisco CCNA & Labs pratiques", "Routage inter-VLAN, OSPF, ACL, segmentation réseau et durcissement des services sous Packet Tracer."),
    ("2024", "Pratique en laboratoire virtuel (Linux & Windows Server)", "Installation, configuration et durcissement d'annuaires Active Directory, serveurs Debian et scripts d'administration."),
]

CERTIFS = ["Cisco CCNA (en préparation)", "TryHackMe — parcours Pre-Security", "Cisco — Introduction to Cybersecurity"]

QUIZ = [
    {"q": "Quel port utilise SSH par défaut ?", "choices": ["21", "22", "80", "443"], "answer": 1,
     "explain": "SSH écoute sur le port TCP 22."},
    {"q": "Combien d'hôtes utilisables dans un /26 ?", "choices": ["30", "62", "64", "126"], "answer": 1,
     "explain": "2^6 = 64 adresses, moins réseau et broadcast = 62."},
    {"q": "Quel protocole attribue automatiquement une adresse IP ?", "choices": ["DNS", "ARP", "DHCP", "ICMP"], "answer": 2,
     "explain": "DHCP distribue adresse, masque, passerelle et DNS."},
    {"q": "Le principe du « moindre privilège » signifie…", "choices": ["Tout le monde est admin", "Donner uniquement les droits nécessaires", "Supprimer les comptes", "Désactiver le pare-feu"], "answer": 1,
     "explain": "Chaque compte ne reçoit que les droits indispensables à sa tâche."},
    {"q": "Quelle commande Cisco affiche la table de routage ?", "choices": ["show vlan", "show ip route", "show run", "ping"], "answer": 1,
     "explain": "« show ip route » liste les routes connues du routeur."},
]
