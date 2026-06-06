#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import shutil
import subprocess
import threading
import zipfile
import tarfile
import time
try:
    import readline
except ImportError:
    readline = None
import argparse
import re
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
import textwrap
from datetime import datetime, timedelta

# --- VERSION & PROJECT INFO ---
VERSION = "1.0"
UPDATE_URL = "https://raw.githubusercontent.com/ZiadMo123/PenKit/main/penkit.py"
UPDATE_CHECK_INTERVAL_DAYS = 7

AUTHOR = "github:ZiadMo123"
PROJECT = f"PenKit Arsenal Framework  |  {AUTHOR}"

# --- COLORS & UI ---
class C:
    RED     = "\033[38;5;196m"
    GREEN   = "\033[38;5;46m"
    YELLOW  = "\033[38;5;226m"
    BLUE    = "\033[38;5;33m"
    MAGENTA = "\033[38;5;201m"
    CYAN    = "\033[38;5;51m"
    WHITE   = "\033[38;5;231m"
    GRAY    = "\033[38;5;244m"
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    BG_RED  = "\033[48;5;196m"

def c(color, text): return f"{color}{text}{C.RESET}"

def banner_gradient(db=None):
    os.system("clear" if os.name == "posix" else "cls")
    lines = [
        "██████╗ ███████╗███╗   ██╗██╗  ██╗██╗████████╗",
        "██╔══██╗██╔════╝████╗  ██║██║ ██╔╝██║╚══██╔══╝",
        "██████╔╝█████╗  ██╔██╗ ██║█████╔╝ ██║   ██║   ",
        "██╔═══╝ ██╔══╝  ██║╚██╗██║██╔═██╗ ██║   ██║   ",
        "██║     ███████╗██║ ╚████║██║  ██╗██║   ██║   ",
        "╚═╝     ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝   ╚═╝   "
    ]
    colors = ["\033[38;5;51m", "\033[38;5;45m", "\033[38;5;39m", "\033[38;5;33m", "\033[38;5;27m", "\033[38;5;21m"]
    print()
    for i, line in enumerate(lines):
        print(f"  {colors[i]}{line}{C.RESET}")
    subtitle = f"[ Arsenal Management Framework v{VERSION} ]"
    print(c(C.GRAY, f"\n  {subtitle:^80}"))
    print(c(C.GRAY, f"  {'by github:ZiadMo123':^80}\n"))

# --- PATHS ---
HOME        = Path.home()
CONFIG_DIR  = HOME / ".penkit"
DB_FILE     = CONFIG_DIR / "tools.json"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE= CONFIG_DIR / "history"
LOG_FILE    = CONFIG_DIR / "install.log"
CUSTOM_DIR  = CONFIG_DIR / "custom_tools"

CONFIG_DIR.mkdir(exist_ok=True)
CUSTOM_DIR.mkdir(exist_ok=True)

# --- KNOWN TOOLS DB ---
# Curated list to prevent false positives
KNOWN_TOOLS = {
    # ── RECON ──────────────────────────────────────────────────────────────
    "nmap":             ("recon",    "Network port scanner and host discovery"),
    "masscan":          ("recon",    "Fast internet-scale port scanner"),
    "rustscan":         ("recon",    "Modern port scanner — finds ports fast then pipes to nmap"),
    "naabu":            ("recon",    "Fast port scanner written in Go"),
    "subfinder":        ("recon",    "Fast passive subdomain enumeration tool"),
    "amass":            ("recon",    "In-depth DNS enumeration and mapping"),
    "assetfinder":      ("recon",    "Find related domains and subdomains"),
    "sublist3r":        ("recon",    "Fast subdomains enumeration tool"),
    "sudomy":           ("recon",    "Subdomain enumeration with automated reconnaissance"),
    "bbot":             ("recon",    "Recursive internet scanner for OSINT and attack surface"),
    "dnsx":             ("recon",    "Fast DNS toolkit for bulk resolution and enumeration"),
    "dnsrecon":         ("recon",    "DNS enumeration script"),
    "dnsenum":          ("recon",    "DNS enumeration — zone transfers, brute force, google scraping"),
    "dnstracer":        ("recon",    "Trace DNS queries to source"),
    "fierce":           ("recon",    "DNS reconnaissance tool"),
    "whois":            ("recon",    "Domain WHOIS lookup utility"),
    "dig":              ("recon",    "DNS lookup and query tool"),
    "host":             ("recon",    "DNS lookup utility"),
    "nslookup":         ("recon",    "DNS name server lookup utility"),
    "traceroute":       ("recon",    "Network route tracing utility"),
    "fping":            ("recon",    "Quick ping sweep tool"),
    "netdiscover":      ("recon",    "Network address discovering tool"),
    "httpx":            ("recon",    "Fast and multi-purpose HTTP toolkit"),
    "httprobe":         ("recon",    "Probe a list of domains for working HTTP/S servers"),
    "waybackurls":      ("recon",    "Fetch URLs from the Wayback Machine for a domain"),
    "gau":              ("recon",    "Fetch known URLs from AlienVault, Wayback and Common Crawl"),
    "hakrawler":        ("recon",    "Fast Go web crawler for endpoint and asset discovery"),
    "gospider":         ("recon",    "Fast web spider written in Go"),
    "katana":           ("recon",    "Next-gen crawling and spidering framework"),
    "meg":              ("recon",    "Fetch many paths for many hosts efficiently"),
    "unfurl":           ("recon",    "Pull apart URLs into components for analysis"),
    "smbmap":           ("recon",    "SMB share enumeration tool"),
    "enum4linux":       ("recon",    "Enumerate info from Windows/Samba systems"),
    "enum4linux-ng":    ("recon",    "Modern rewrite of enum4linux with extra features"),
    "onesixtyone":      ("recon",    "Fast SNMP scanner"),
    "snmpwalk":         ("recon",    "Retrieve SNMP info from network devices"),
    "ldapsearch":       ("recon",    "LDAP directory query tool"),
    "ldapdomaindump":   ("recon",    "Active Directory information dumper via LDAP"),
    "netexec":          ("recon",    "Swiss army knife for network protocol enumeration (CME successor)"),
    "kerbrute":         ("recon",    "Kerberos username enumeration and password spraying"),
    "cloud-enum":       ("recon",    "Multi-cloud OSINT — enumerate public AWS, Azure and GCP resources"),
    "shodan":           ("recon",    "Shodan command-line utility"),
    "shodan-cli":       ("recon",    "Shodan command-line interface (pip install shodan)"),
    "censys":           ("recon",    "Censys CLI for internet-wide scanning data"),

    # ── BRUTE ──────────────────────────────────────────────────────────────
    "hydra":            ("brute",    "Network login brute forcer (SSH, FTP, HTTP...)"),
    "thc-hydra":        ("brute",    "Network login brute forcer (alternate binary name)"),
    "medusa":           ("brute",    "Parallel brute force login tool"),
    "ncrack":           ("brute",    "High-speed network authentication cracking"),
    "patator":          ("brute",    "Multi-purpose brute-forcer"),
    "crowbar":          ("brute",    "Brute forcing tool"),
    "spray":            ("brute",    "Password spraying tool"),
    "sprayhound":       ("brute",    "Password spraying tool integrated with BloodHound"),
    "ruler":            ("brute",    "Abuse Exchange services for password spraying/phishing"),
    "brutespray":       ("brute",    "Auto-brute-forces services found by nmap"),
    "gobuster":         ("brute",    "Directory/DNS brute force tool"),
    "ffuf":             ("brute",    "Fast web fuzzer written in Go"),
    "dirb":             ("brute",    "Web content scanner using wordlists"),
    "wfuzz":            ("brute",    "Web application fuzzer"),
    "dirsearch":        ("brute",    "Web path brute-force scanner"),
    "feroxbuster":      ("brute",    "Fast recursive content brute-forcer written in Rust"),
    "dnsmap":           ("brute",    "Subdomain brute-forcer with built-in or custom wordlists"),
    "altdns":           ("brute",    "Subdomain permutation and mutation brute-forcer"),
    "massdns":          ("brute",    "High-performance DNS stub resolver for bulk lookups"),
    "puredns":          ("brute",    "Fast domain resolver and subdomain bruteforcing tool"),
    "wordlistctl":      ("brute",    "Fetch, install and search wordlist archives"),

    # ── WEB ────────────────────────────────────────────────────────────────
    "sqlmap":           ("web",      "Automatic SQL injection exploitation"),
    "ghauri":           ("web",      "Advanced SQL injection detection and exploitation"),
    "sqlninja":         ("web",      "SQL injection tool targeting Microsoft SQL Server"),
    "nosqlmap":         ("web",      "NoSQL database enumeration and attack tool"),
    "nikto":            ("web",      "Web server vulnerability scanner"),
    "nuclei":           ("web",      "Targeted template-based vulnerability scanner"),
    "wpscan":           ("web",      "WordPress vulnerability scanner"),
    "joomscan":         ("web",      "OWASP Joomla vulnerability scanner"),
    "droopescan":       ("web",      "CMS vulnerability scanner — Drupal, SilverStripe etc."),
    "cmseek":           ("web",      "CMS detection and exploitation tool"),
    "whatweb":          ("web",      "Next-gen web scanner — identifies technologies"),
    "wafw00f":          ("web",      "Web Application Firewall fingerprinting"),
    "xsstrike":         ("web",      "Advanced XSS detection suite"),
    "dalfox":           ("web",      "XSS scanner and utility"),
    "commix":           ("web",      "Automated command injection exploiter"),
    "tplmap":           ("web",      "Server-side template injection detection and exploitation"),
    "smuggler":         ("web",      "HTTP request smuggling / desync testing tool"),
    "jwt-tool":         ("web",      "JWT testing toolkit for analysis and exploitation"),
    "graphqlmap":       ("web",      "GraphQL endpoint exploitation tool"),
    "graphw00f":        ("web",      "GraphQL server fingerprinting tool"),
    "403fuzzer":        ("web",      "Fuzz 403 forbidden pages for bypasses"),
    "byp4xx":           ("web",      "Bypass 40x HTTP errors with various techniques"),
    "paramspider":      ("web",      "Mine parameters from web archives for fuzzing"),
    "arjun":            ("web",      "HTTP parameter discovery suite"),
    "qsreplace":        ("web",      "Replace URL query string values for testing"),
    "cors-scanner":     ("web",      "Scan for CORS misconfigurations"),
    "hakcheckurl":      ("web",      "Check URLs for SSRF, open redirects and more"),
    "cariddi":          ("web",      "Crawler and scanner for endpoints, secrets and parameters"),
    "interactsh-client":("web",      "Client for out-of-band interaction testing (OAST)"),
    "gopherus":         ("web",      "Generate SSRF payloads for various services"),
    "burpsuite":        ("web",      "Web app proxy and testing suite"),
    "zaproxy":          ("web",      "OWASP ZAP — web application security scanner"),
    "zap":              ("web",      "OWASP Zed Attack Proxy (alias)"),
    "wapiti":           ("web",      "Web application vulnerability scanner"),
    "skipfish":         ("web",      "Active web application security reconnaissance tool"),
    "arachni":          ("web",      "Web application security scanner framework"),

    # ── EXPLOIT ────────────────────────────────────────────────────────────
    "metasploit":       ("exploit",  "The most popular exploitation framework"),
    "msfconsole":       ("exploit",  "Metasploit Framework console"),
    "msfvenom":         ("exploit",  "Payload generator and encoder"),
    "searchsploit":     ("exploit",  "Offline exploit search (ExploitDB)"),
    "beef-xss":         ("exploit",  "Browser Exploitation Framework"),
    "routersploit":     ("exploit",  "Exploitation Framework for Embedded Devices"),
    "responder":        ("exploit",  "LLMNR/NBT-NS/mDNS poisoner — active AD credential capture"),
    "impacket":         ("exploit",  "AD and protocol exploitation toolkit (Python)"),
    "crackmapexec":     ("exploit",  "Swiss army knife for AD lateral movement and exploitation"),
    "ntlmrelayx":       ("exploit",  "NTLM relay attack tool (part of Impacket)"),
    "mitm6":            ("exploit",  "IPv6 MITM attack tool targeting Windows AD environments"),
    "coercer":          ("exploit",  "Coerce Windows hosts to authenticate via MS-RPC methods"),
    "petitpotam":       ("exploit",  "Coerce Windows host authentication via MS-EFSRPC"),
    "printerbug":       ("exploit",  "Trigger Windows printer bug for auth coercion"),
    "dcsync":           ("exploit",  "DCSync attack to extract credentials from domain controllers"),
    "certipy":          ("exploit",  "Active Directory Certificate Services attack tool"),
    "sliver":           ("exploit",  "Open-source cross-platform adversary simulation C2 framework"),
    "havoc":            ("exploit",  "Modern C2 framework for red team operations"),
    "villain":          ("exploit",  "C2 framework for managing reverse TCP and HoaxShell shells"),
    "pwncat":           ("exploit",  "Bind/reverse shell handler with post-exploitation features"),
    "ysoserial":        ("exploit",  "Java deserialization RCE payload generator"),

    # ── POST-EXPLOITATION ──────────────────────────────────────────────────
    "linpeas":          ("post",     "Linux privilege escalation script"),
    "winpeas":          ("post",     "Windows privilege escalation script"),
    "mimikatz":         ("post",     "Extract passwords, hashes, and Kerberos tickets from memory"),
    "mimipenguin":      ("post",     "Dump login passwords from current Linux desktop user"),
    "lazagne":          ("post",     "Retrieve stored passwords from many applications"),
    "lazykatz":         ("post",     "Automated credential extraction from lsass"),
    "lsassy":           ("post",     "Extract credentials from lsass remotely"),
    "dploot":           ("post",     "DPAPI looting tool for remote credential extraction"),
    "bloodhound":       ("post",     "Active Directory attack path visualizer"),
    "sharphound":       ("post",     "BloodHound ingestor written in C#"),
    "adidnsdump":       ("post",     "Enumerate and dump Active Directory DNS records"),
    "bloodyad":         ("post",     "AD privilege escalation framework using LDAP"),
    "rubeus":           ("post",     "C# toolset for raw Kerberos interaction and abuse"),
    "empire":           ("post",     "PowerShell and Python post-exploitation agent"),
    "starkiller":       ("post",     "GUI front-end for the Empire C2 framework"),
    "covenant":         ("post",     ".NET C2 framework for red team operations"),
    "merlin":           ("post",     "Cross-platform post-exploitation HTTP/2 C2 server"),
    "nishang":          ("post",     "PowerShell offensive security framework"),
    "powersploit":      ("post",     "PowerShell post-exploitation framework"),
    "powercat":         ("post",     "PowerShell TCP/IP swiss army knife — netcat alternative"),
    "sharpup":          ("post",     "C# port of PowerUp — Windows privilege escalation checks"),
    "seatbelt":         ("post",     "C# security-oriented host survey/enumeration tool"),
    "evil-winrm":       ("post",     "WinRM shell for pentesting"),
    "manspider":        ("post",     "Spider SMB shares for sensitive files and credentials"),
    "chisel":           ("post",     "TCP/UDP tunneling over HTTP"),
    "ligolo":           ("post",     "Advanced tunneling tool"),
    "frp":              ("post",     "Fast reverse proxy to expose local servers through NAT"),
    "neo-regeorg":      ("post",     "Tunnel data via webshells using HTTP"),
    "pivotnacci":       ("post",     "Create pivoting connections using HTTP agents"),
    "microsocks":       ("post",     "Tiny SOCKS5 server for pivoting"),
    "revsocks":         ("post",     "Reverse SOCKS5 server for pivoting through firewalls"),
    "proxifier":        ("post",     "Redirect connections through SOCKS/HTTP proxies"),
    "mettle":           ("post",     "Lightweight Meterpreter for constrained environments"),
    "pspy":             ("post",     "Monitor linux processes without root permissions"),
    "pspy64":           ("post",     "Monitor Linux processes without root (64-bit)"),
    "pspy32":           ("post",     "Monitor Linux processes without root (32-bit)"),

    # ── PASSWORD ───────────────────────────────────────────────────────────
    "hashcat":          ("password", "GPU-accelerated password cracker"),
    "john":             ("password", "John the Ripper password cracker"),
    "ophcrack":         ("password", "Windows password cracker based on rainbow tables"),
    "hash-identifier":  ("password", "Tool to identify different types of hashes"),
    "name-that-hash":   ("password", "Modern hash identification tool"),
    "haiti":            ("password", "Hash type identifier"),
    "hashid":           ("password", "Identify hashing algorithms"),
    "crunch":           ("password", "Custom wordlist generator"),
    "cewl":             ("password", "Wordlist generator from websites"),
    "cupp":             ("password", "Common User Passwords Profiler"),
    "rsmangler":        ("password", "Wordlist mangling tool"),
    "mentalist":        ("password", "Graphical tool for custom wordlist generation"),
    "kwprocessor":      ("password", "Keyboard-walk wordlist generator for hashcat"),
    "maskprocessor":    ("password", "High-performance word generator with masks"),
    "princeprocessor":  ("password", "PRINCE algorithm wordlist generator"),
    "pass-station":     ("password", "Find default credentials for common network equipment"),

    # ── WIRELESS ───────────────────────────────────────────────────────────
    "aircrack-ng":      ("wireless", "WEP/WPA/WPA2 key cracking suite"),
    "airodump-ng":      ("wireless", "Packet capture for aircrack-ng"),
    "aireplay-ng":      ("wireless", "Packet injection for aircrack-ng"),
    "airbase-ng":       ("wireless", "Multi-purpose tool aimed at attacking wireless clients"),
    "airmon-ng":        ("wireless", "Enable/disable monitor mode on wireless interfaces"),
    "kismet":           ("wireless", "Wireless network detector, sniffer, and IDS"),
    "wifite":           ("wireless", "Automated wireless attack tool"),
    "wifiphisher":      ("wireless", "Rogue AP framework for phishing Wi-Fi credentials"),
    "eaphammer":        ("wireless", "Targeted WPA2-Enterprise credential theft and hostile portal attacks"),
    "hostapd-wpe":      ("wireless", "Rogue AP for WPA Enterprise credential capture"),
    "reaver":           ("wireless", "WPS brute force tool"),
    "bully":            ("wireless", "WPS brute force attack tool"),
    "wash":             ("wireless", "Scan for WPS enabled access points"),
    "pixiewps":         ("wireless", "Offline WPS PIN brute force tool"),
    "mdk4":             ("wireless", "Wi-Fi testing and deauthentication tool"),
    "hcxdumptool":      ("wireless", "Capture WiFi PMKID/handshakes for offline cracking"),
    "hcxtools":         ("wireless", "Convert and process captured WiFi handshakes"),
    "pyrit":            ("wireless", "WPA/WPA2-PSK cracking using GPU"),
    "wigle-wifi":       ("wireless", "WiGLE.net wireless network mapping tool"),
    "gqrx":             ("wireless", "Software defined radio receiver"),
    "rtl-sdr":          ("wireless", "Tools for RTL-SDR software defined radio"),

    # ── NETWORK ────────────────────────────────────────────────────────────
    "wireshark":        ("network",  "Graphical network protocol analyzer"),
    "tcpdump":          ("network",  "CLI packet capture"),
    "ettercap":         ("network",  "MITM attacks and sniffing"),
    "bettercap":        ("network",  "Modern network attack and monitor tool"),
    "arpspoof":         ("network",  "Intercept packets on a switched LAN"),
    "netcat":           ("network",  "TCP/UDP Swiss army knife"),
    "nc":               ("network",  "TCP/UDP Swiss army knife (netcat alias)"),
    "socat":            ("network",  "Advanced bidirectional data relay"),
    "scapy":            ("network",  "Python-based packet manipulation framework"),
    "hping3":           ("network",  "Active network smashing tool and packet crafter"),
    "mitmproxy":        ("network",  "Interactive TLS-capable intercepting proxy"),
    "mitmdump":         ("network",  "Command-line version of mitmproxy"),
    "proxychains":      ("network",  "Force TCP connections through proxy chains"),
    "proxychains4":     ("network",  "Force TCP connections through proxy chains (v4)"),
    "sshuttle":         ("network",  "Transparent proxy VPN over SSH"),
    "iodine":           ("network",  "DNS tunneling tool"),
    "ptunnel":          ("network",  "Tunnel TCP connections over ICMP packets"),
    "pwnat":            ("network",  "NAT to NAT client-server communication"),
    "dnschef":          ("network",  "DNS proxy for penetration testers"),
    "macchanger":       ("network",  "MAC address changer utility"),
    "yersinia":         ("network",  "Framework for layer 2 protocol attacks"),
    "netsed":           ("network",  "Network packet stream editor"),
    "tcpflow":          ("network",  "Capture and store TCP connections for analysis"),
    "ngrep":            ("network",  "Network-layer grep for packet inspection"),
    "dsniff":           ("network",  "Collection of password sniffers and network analysis tools"),
    "smbclient":        ("network",  "SMB client for accessing Windows shares"),
    "rpcclient":        ("network",  "MS-RPC client for Windows enumeration"),
    "snort":            ("network",  "Open-source network intrusion detection and prevention"),
    "zeek":             ("network",  "Network analysis framework for security monitoring"),

    # ── FORENSICS ──────────────────────────────────────────────────────────
    "autopsy":          ("forensics","Digital forensics platform"),
    "binwalk":          ("forensics","Firmware analysis and extraction"),
    "foremost":         ("forensics","Recover files based on their headers"),
    "scalpel":          ("forensics","Fast file carver based on header/footer patterns"),
    "bulk-extractor":   ("forensics","Extract features from disk images without parsing filesystem"),
    "testdisk":         ("forensics","Data recovery and partition repair tool"),
    "photorec":         ("forensics","Recover lost files from hard drives and memory cards"),
    "sleuthkit":        ("forensics","Collection of CLI tools for disk image analysis"),
    "volatility":       ("forensics","Memory forensics framework"),
    "rekall":           ("forensics","Memory analysis framework (Volatility fork)"),
    "log2timeline":     ("forensics","Timeline creation tool for log analysis"),
    "plaso":            ("forensics","Log2timeline super timeline framework"),
    "exiftool":         ("forensics","Metadata reader/writer for files"),
    "metagoofil":       ("forensics","Metadata extraction from public documents"),
    "pdf-parser":       ("forensics","Parse and analyse PDF documents for malicious content"),
    "oletools":         ("forensics","Tools to analyse Microsoft OLE2 files (Office docs)"),
    "olevba":           ("forensics","Extract and analyse VBA macros from Office documents"),
    "steghide":         ("forensics","Steganography tool"),
    "stegseek":         ("forensics","Steganography cracker"),
    "stegsolve":        ("forensics","Steganography analysis tool for images"),
    "zsteg":            ("forensics","Detect steganography in PNG and BMP files"),

    # ── REVERSING ──────────────────────────────────────────────────────────
    "radare2":          ("reversing","Reverse engineering framework and disassembler"),
    "ghidra":           ("reversing","NSA-developed software reverse engineering suite"),
    "cutter":           ("reversing","GUI for reverse engineering using radare2"),
    "binary-ninja":     ("reversing","Interactive binary analysis platform"),
    "retdec":           ("reversing","Machine-code decompiler based on LLVM"),
    "r2ghidra":         ("reversing","Ghidra decompiler integration for radare2"),
    "gdb":              ("reversing","GNU debugger for binary analysis"),
    "gdb-peda":         ("reversing","Python exploit development assistance for GDB"),
    "pwndbg":           ("reversing","Enhanced GDB for exploit development"),
    "peda":             ("reversing","Python exploit development assistance plugin for GDB"),
    "pwntools":         ("reversing","CTF framework and exploit development library"),
    "ropper":           ("reversing","Find gadgets and create ROP chains"),
    "ROPgadget":        ("reversing","Search for ROP/JOP/SYS gadgets in binaries"),
    "one-gadget":       ("reversing","Find one-gadget RCE in libc"),
    "checksec":         ("reversing","Check binary security properties (NX, PIE, RELRO)"),
    "angr":             ("reversing","Binary analysis and symbolic execution framework"),
    "objdump":          ("reversing","Display information from object files"),
    "nm":               ("reversing","List symbols from object files"),
    "readelf":          ("reversing","Display info about ELF binaries"),
    "ltrace":           ("reversing","Library call tracer"),
    "strace":           ("reversing","System call tracer"),
    "strings":          ("reversing","Print strings of printable characters in binary files"),
    "hexedit":          ("reversing","Hex editor for binary file inspection"),
    "xxd":              ("reversing","Hex dump utility"),

    # ── SOCIAL ENGINEERING ─────────────────────────────────────────────────
    "setoolkit":        ("social",   "Social Engineering Toolkit"),
    "gophish":          ("social",   "Open-Source Phishing Toolkit"),
    "evilginx2":        ("social",   "Standalone MITM phishing framework"),
    "evilginx":         ("social",   "MITM phishing framework for capturing 2FA tokens"),
    "modlishka":        ("social",   "Reverse proxy phishing with 2FA bypass"),
    "king-phisher":     ("social",   "Phishing campaign toolkit and server"),
    "zphisher":         ("social",   "Automated phishing tool with 30+ templates"),
    "blackeye":         ("social",   "Phishing tool with pre-built site templates"),
    "shellphish":       ("social",   "Phishing tool with 18+ social media templates"),
    "socialphish":      ("social",   "Phishing tool for capturing credentials via fake pages"),

    # ── CRYPTO / TLS ───────────────────────────────────────────────────────
    "sslscan":          ("crypto",   "SSL/TLS cipher scanner"),
    "testssl":          ("crypto",   "Testing TLS/SSL encryption"),
    "sslyze":           ("crypto",   "TLS/SSL configuration analyser"),
    "openssl":          ("crypto",   "Cryptography and SSL/TLS toolkit"),
    "rsactftool":       ("crypto",   "RSA public key recovery and decryption tool"),
    "xortool":          ("crypto",   "XOR cipher analysis tool"),
    "ciphey":           ("crypto",   "Auto-decrypt ciphertext using AI and frequency analysis"),
    "featherduster":    ("crypto",   "Automated cryptanalysis tool"),

    # ── CLOUD ──────────────────────────────────────────────────────────────
    "aws":              ("cloud",    "AWS command-line interface"),
    "awscli":           ("cloud",    "AWS command-line interface (package name)"),
    "gcloud":           ("cloud",    "Google Cloud SDK command-line tool"),
    "az":               ("cloud",    "Microsoft Azure command-line interface"),
    "pacu":             ("cloud",    "AWS exploitation framework for red teamers"),
    "weirdaal":         ("cloud",    "AWS offensive security tool collection"),
    "cloudmapper":      ("cloud",    "Analyse AWS environments for security issues"),
    "prowler":          ("cloud",    "AWS, GCP, Azure security best practices assessment tool"),
    "scoutsuite":       ("cloud",    "Multi-cloud security auditing tool"),
    "cloudsploit":      ("cloud",    "Cloud security configuration scanning"),
    "cloudbrute":       ("cloud",    "Cloud resource discovery and enumeration tool"),
    "enumerate-iam":    ("cloud",    "Enumerate IAM permissions without needing admin access"),
    "trufflehog":       ("cloud",    "Search Git repos for secrets and credentials"),
    "gitleaks":         ("cloud",    "Scan Git repos for hardcoded secrets"),
    "gitrob":           ("cloud",    "Reconnaissance tool targeting GitHub organisations"),
    "s3scanner":        ("cloud",    "Scan for open S3 buckets and dump their contents"),
    "gcpbucketbrute":   ("cloud",    "Enumerate GCP storage buckets"),
    "stormspotter":     ("cloud",    "Azure and AAD attack path visualizer"),
    "roadtools":        ("cloud",    "Azure AD exploration and token tool framework"),
    "azurehound":       ("cloud",    "BloodHound data collector for Azure and Azure AD"),

    # ── CONTAINER / KUBERNETES ─────────────────────────────────────────────
    "trivy":            ("container","Vulnerability scanner for containers and IaC"),
    "grype":            ("container","Container and filesystem vulnerability scanner"),
    "syft":             ("container","SBOM generator for containers and filesystems"),
    "dive":             ("container","Explore Docker image layers for secrets/misconfigs"),
    "dockle":           ("container","Container image linter for security best practices"),
    "falco":            ("container","Cloud-native runtime security and threat detection"),
    "kube-bench":       ("container","CIS Kubernetes benchmark compliance checker"),
    "kube-hunter":      ("container","Active/passive Kubernetes vulnerability hunting"),
    "kube-score":       ("container","Kubernetes manifest static code analysis"),
    "kubesec":          ("container","Security risk analysis for Kubernetes resources"),
    "popeye":           ("container","Live Kubernetes cluster sanitizer and linter"),
    "cdk":              ("container","Container escape and pivoting toolkit"),
    "amicontained":     ("container","Discover container runtime and available capabilities"),
    "deepce":           ("container","Docker enumeration, escalation and container escape tool"),

    # ── MOBILE ─────────────────────────────────────────────────────────────
    "apktool":          ("mobile",   "Reverse engineer Android APK files"),
    "jadx":             ("mobile",   "Java and Android APK decompiler"),
    "adb":              ("mobile",   "Android Debug Bridge — device control and shell"),
    "frida":            ("mobile",   "Dynamic instrumentation toolkit for apps"),
    "frida-tools":      ("mobile",   "CLI tools for the Frida instrumentation framework"),
    "objection":        ("mobile",   "Runtime mobile exploration powered by Frida"),
    "drozer":           ("mobile",   "Android security testing framework"),
    "mobsf":            ("mobile",   "Mobile Security Framework — static/dynamic analysis"),
    "apkleaks":         ("mobile",   "Scan APKs for URIs, endpoints and secrets"),
    "androbugs":        ("mobile",   "Android app vulnerability scanner"),
    "apkid":            ("mobile",   "Android application identifier — anti-tamper detection"),
    "aapt":             ("mobile",   "Android Asset Packaging Tool"),
    "baksmali":         ("mobile",   "Disassembler for the dex format"),
    "smali":            ("mobile",   "Assembler for dex format used in Android"),
    "ios-deploy":       ("mobile",   "Install and debug iOS apps from command line"),
    "ideviceinstaller": ("mobile",   "Manage iOS apps via libimobiledevice"),
    "bfinject":         ("mobile",   "Dylib injection tool for iOS apps"),
    "needle":           ("mobile",   "iOS security testing framework"),

    # ── OSINT ──────────────────────────────────────────────────────────────
    "recon-ng":         ("osint",    "Full-featured web reconnaissance framework"),
    "maltego":          ("osint",    "Visual link analysis and OSINT framework"),
    "spiderfoot":       ("osint",    "Automated OSINT reconnaissance framework"),
    "theharvester":     ("osint",    "Gather emails, names, subdomains and IPs from public sources"),
    "theHarvester":     ("osint",    "Gather emails, names, subdomains and IPs from public sources"),
    "photon":           ("osint",    "Fast crawler for OSINT data extraction"),
    "sherlock":         ("osint",    "Hunt down social media accounts by username"),
    "maigret":          ("osint",    "Collect a dossier on a person by username across 3000+ sites"),
    "holehe":           ("osint",    "Check if email is used on different sites"),
    "h8mail":           ("osint",    "Email OSINT and breach hunting tool"),
    "ghunt":            ("osint",    "Investigate Google accounts using internal API"),
    "phoneinfoga":      ("osint",    "Advanced information gathering for phone numbers"),
    "ignorant":         ("osint",    "Check if a phone number is used on services"),
    "pwnedornot":       ("osint",    "Find passwords for compromised emails"),
    "twint":            ("osint",    "Twitter intelligence tool — no API needed"),
    "osintgram":        ("osint",    "OSINT tool for Instagram accounts"),
    "social-analyzer":  ("osint",    "Find a person's profile across 1000+ sites"),
    "crosslinked":      ("osint",    "LinkedIn enumeration tool for username harvesting"),
    "linkedin2username":("osint",    "Generate username lists from LinkedIn company pages"),
    "userrecon":        ("osint",    "Find usernames on over 75 websites"),
    "email2phonenumber":("osint",    "OSINT tool to find phone number from email address"),
    "metagoofil":       ("osint",    "Metadata extraction from public documents"),

    # ── API SECURITY ───────────────────────────────────────────────────────
    "kiterunner":       ("api",      "Context-aware API discovery and wordlist bruteforce"),
    "astra":            ("api",      "REST API penetration testing tool"),
    "restler":          ("api",      "Stateful REST API fuzzer"),
    "swagger-jacker":   ("api",      "Exploit and enumerate Swagger/OpenAPI endpoints"),
    "automatic-api-attack-tool": ("api", "Imperva automatic API attack tool"),

    # ── EVASION ────────────────────────────────────────────────────────────
    "veil":             ("evasion",  "Generate Metasploit payloads bypassing AV solutions"),
    "shellter":         ("evasion",  "Dynamic shellcode injection and PE infector"),
    "unicorn":          ("evasion",  "PowerShell downgrade attack and shellcode injector"),
    "invoke-obfuscation":("evasion", "PowerShell obfuscator"),
    "defendercheck":    ("evasion",  "Identify bytes that trigger Windows Defender"),
    "pe-bear":          ("evasion",  "PE reversing tool and editor"),
    "nimcrypt2":        ("evasion",  "Nim-based PE packer and AV bypass"),
    "scarecrow":        ("evasion",  "Payload creation framework for EDR bypass"),
    "donut":            ("evasion",  "Position-independent shellcode from EXE/DLL"),
    "freeze":           ("evasion",  "Payload creation tool for bypassing EDRs"),
    "sgn":              ("evasion",  "Cypher shellcode encoder with polymorphic features"),
    "msfpc":            ("evasion",  "MSFvenom payload creator — automates payload generation"),

    # ── ICS / SCADA ────────────────────────────────────────────────────────
    "plcscan":          ("ics",      "PLC scanner for detecting Siemens and other PLCs"),
    "redpoint":         ("ics",      "ICS/SCADA assessment Metasploit modules"),
    "s7scan":           ("ics",      "Scanner for Siemens S7 PLCs"),
    "modscan":          ("ics",      "Modbus scanner for ICS enumeration"),
    "mbtget":           ("ics",      "Modbus TCP client for reading/writing registers"),
    "isf":              ("ics",      "Industrial exploitation framework"),
    "conpot":           ("ics",      "ICS honeypot for detection and intelligence"),
    "gridlabd":         ("ics",      "Smart grid simulation and analysis tool"),
}
CAT_COLORS = {
    "recon":     C.BLUE,
    "brute":     C.RED,
    "web":       C.GREEN,
    "exploit":   C.MAGENTA,
    "password":  C.YELLOW,
    "wireless":  C.CYAN,
    "network":   C.BLUE,
    "post":      C.MAGENTA,
    "forensics": C.GRAY,
    "social":    C.RED,
    "crypto":    C.CYAN,
    "cloud":     C.GREEN,
    "reversing": C.YELLOW,
    "container": C.CYAN,
    "mobile":    C.GREEN,
    "osint":     C.BLUE,
    "ics":       C.YELLOW,
    "api":       C.GREEN,
    "evasion":   C.MAGENTA,
    "custom":    C.WHITE,
    "unknown":   C.GRAY,
}

KEYWORDS = {
    "recon":     ["enumeration", "subdomain", "dns", "scanner", "discovery", "recon", "osint", "footprint"],
    "brute":     ["brute force", "bruteforce", "crack", "login", "spray", "password spray"],
    "web":       ["web", "xss", "sql", "fuzzer", "directory", "http", "graphql", "api", "request smuggling"],
    "exploit":   ["exploit", "cve", "payload", "shellcode", "buffer overflow", "rop"],
    "password":  ["password", "hash", "wordlist", "dictionary", "rainbow"],
    "wireless":  ["wifi", "wpa", "wep", "wireless", "802.11", "handshake", "beacon"],
    "network":   ["packet", "mitm", "sniff", "pcap", "tcp", "udp", "proxy", "socks", "pivot"],
    "post":      ["privilege escalation", "privesc", "post-exploitation", "tunnel", "lateral movement", "persistence", "c2", "command and control"],
    "forensics": ["forensic", "steganography", "memory", "extract", "carve", "artifact", "disk image"],
    "social":    ["phishing", "social engineering", "credential harvesting", "pretexting"],
    "crypto":    ["crypto", "ssl", "tls", "certificate", "cipher", "rsa", "xor", "decrypt"],
    "cloud":     ["aws", "azure", "gcp", "cloud", "s3", "bucket", "iam", "lambda", "kubernetes", "container"],
    "reversing": ["reverse engineering", "disassemble", "decompile", "binary", "elf", "pe", "rop", "gadget", "exploit dev"],
    "container": ["container", "docker", "kubernetes", "k8s", "pod", "image layer", "cgroup", "namespace"],
    "mobile":    ["android", "ios", "apk", "ipa", "frida", "smali", "dalvik", "mobile app"],
    "osint":     ["osint", "open source intelligence", "username", "email", "social media", "person lookup"],
    "ics":       ["ics", "scada", "plc", "modbus", "dnp3", "industrial", "ot security"],
    "api":       ["api", "rest", "graphql", "openapi", "swagger", "endpoint", "json"],
    "evasion":   ["bypass", "edr", "av bypass", "antivirus", "obfuscation", "shellcode", "payload generation"],
}

# --- CONFIG & DB ---
def load_db():
    if DB_FILE.exists():
        try: return json.loads(DB_FILE.read_text())
        except: pass
    return {"tools": {}, "custom": {}, "last_scan": None}

def save_db(db):
    DB_FILE.write_text(json.dumps(db, indent=2))

def load_config():
    if CONFIG_FILE.exists():
        try: return json.loads(CONFIG_FILE.read_text())
        except: pass
    return {
        "github_token": None,
        "token_expiry": None,
        "pip_mode": None, # "venv" or "system"
        "install_path": "/opt",
        "aliases": {}
    }

def save_config(config):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))
    # Restrict config file to owner-only (rw-------).
    # config.json stores the GitHub API token in plaintext — this chmod
    # prevents other users on the same system from reading it.
    # Do NOT remove this line.
    os.chmod(CONFIG_FILE, 0o600)

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

# --- TOKEN MANAGEMENT ---
def check_token_expiry(config):
    expiry = config.get("token_expiry")
    if not expiry:
        return
    try:
        exp_date = datetime.strptime(expiry, "%Y-%m-%d")
        now = datetime.now()
        diff = (exp_date - now).days
        
        if diff < 0:
            print(c(C.BG_RED + C.WHITE, f" [!] CRITICAL: Your GitHub token has expired on {expiry}! Please update it. "))
            print()
        elif diff <= 3:
            print(c(C.YELLOW, f" [!] WARNING: Your GitHub token will expire in {diff} days ({expiry})."))
            print()
    except ValueError:
        pass

def cmd_config(config, args):
    if not args:
        print(c(C.CYAN, "\n  [ Config Options ]"))
        print(f"  config token set      - Set GitHub token and expiry")
        print(f"  config token modify   - Modify GitHub token")
        print(f"  config token show     - Show current token details")
        print(f"  config token remove   - Remove GitHub token")
        print(f"  config pip-mode       - Set default pip mode (venv/system/prompt)")
        print(f"  config install-path   - Set default install path (e.g. /opt)")
        print(f"  config show           - Show all config settings\n")
        return

    sub = args[0].lower()
    if sub == "token":
        if len(args) < 2:
            print(c(C.RED, "  [!] Usage: config token <set|modify|show|remove>"))
            return
        act = args[1].lower()
        if act in ("set", "modify"):
            token = input(c(C.CYAN, "  Enter GitHub Token: ")).strip()
            expiry = input(c(C.CYAN, "  Enter Expiry Date (YYYY-MM-DD) or leave blank: ")).strip()
            config["github_token"] = token
            if expiry: config["token_expiry"] = expiry
            save_config(config)
            print(c(C.GREEN, "  [+] Token saved."))
        elif act == "show":
            tok = config.get("github_token")
            exp = config.get("token_expiry", "None")
            if tok:
                masked = tok[:4] + "*"*10 + tok[-4:] if len(tok)>8 else "***"
                print(c(C.WHITE, f"\n  Token:  {masked}"))
                print(c(C.WHITE, f"  Expiry: {exp}\n"))
            else:
                print(c(C.YELLOW, "  [~] No token configured."))
        elif act == "remove":
            config["github_token"] = None
            config["token_expiry"] = None
            save_config(config)
            print(c(C.GREEN, "  [+] Token removed."))
    elif sub == "pip-mode":
        mode = input(c(C.CYAN, "  Set default pip mode (venv/system/prompt): ")).strip().lower()
        if mode in ("venv", "system"):
            config["pip_mode"] = mode
            save_config(config)
            print(c(C.GREEN, f"  [+] Pip mode set to {mode}."))
        elif mode == "prompt":
            config["pip_mode"] = None
            save_config(config)
            print(c(C.GREEN, f"  [+] Pip mode set to prompt."))
        else:
            print(c(C.RED, "  [!] Invalid mode."))
    elif sub == "install-path":
        path = input(c(C.CYAN, "  Set default install path (e.g. /opt): ")).strip()
        config["install_path"] = path
        save_config(config)
        print(c(C.GREEN, f"  [+] Install path set to {path}."))
    elif sub == "show":
        print(c(C.CYAN, "\n  [ Current Configuration ]"))
        print(json.dumps({k:v for k,v in config.items() if k!="github_token"}, indent=2))
        print()

# --- GITHUB API ---
def fetch_github_info(url, token=None):
    # url: https://github.com/owner/repo
    parts = url.rstrip("/").split("/")
    if len(parts) < 2: return "unknown", "Custom tool"
    owner, repo = parts[-2], parts[-1].replace(".git", "")
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    readme_url = f"{api_url}/readme"
    
    headers = {"User-Agent": "PenKit"}
    if token:
        headers["Authorization"] = f"token {token}"
        
    desc = "Custom tool"
    cat = "unknown"
    
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get("description"):
                desc = data["description"]
    except Exception as e:
        log(f"GitHub API Error (Repo): {e}")

    try:
        headers["Accept"] = "application/vnd.github.v3.raw"
        req = urllib.request.Request(readme_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            readme = response.read().decode().lower()
            
            # Analyze README for category
            best_cat = "unknown"
            max_matches = 0
            for k, words in KEYWORDS.items():
                matches = sum(readme.count(w) for w in words)
                if matches > max_matches:
                    max_matches = matches
                    best_cat = k
            if max_matches > 0:
                cat = best_cat
    except Exception as e:
        log(f"GitHub API Error (README): {e}")

    return cat, desc

def search_github_for_tool(query, token=None):
    api_url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc"
    headers = {"User-Agent": "PenKit"}
    if token:
        headers["Authorization"] = f"token {token}"
        
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("items", [])[:5]
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(c(C.RED, "\n  [!] GitHub API rate limit exceeded. Please configure a token: config token set"))
        else:
            print(c(C.RED, f"\n  [!] GitHub Search Error: {e}"))
        return []
    except Exception as e:
        print(c(C.RED, f"\n  [!] GitHub Search Error: {e}"))
        return []

# --- SCANNER ---
def scan_system(silent=False, existing=None):
    if not silent:
        print(c(C.CYAN, "\n  [*] Scanning system for known pentest tools..."))
        
    found = {}
    for name, (cat, desc) in KNOWN_TOOLS.items():
        path = shutil.which(name)
        if path:
            # Preserve any tag the user manually set via the tag command
            if existing and name in existing and existing[name].get("manually_tagged"):
                cat = existing[name]["category"]
            found[name] = {
                "path": path,
                "category": cat,
                "desc": desc,
                "source": "system",
                "manually_tagged": existing.get(name, {}).get("manually_tagged", False) if existing else False,
                "added": datetime.now().isoformat()
            }
            
    if not silent:
        print(c(C.GREEN, f"  [+] Found {len(found)} known pentest tools.\n"))
    return found

# --- ALIASES ---
def cmd_alias(config, args):
    if len(args) < 2:
        print(c(C.RED, "  [!] Usage: alias <name> \"<command>\""))
        return
    name = args[0]
    cmd = " ".join(args[1:]).strip('"').strip("'")
    config.setdefault("aliases", {})[name] = cmd
    save_config(config)
    print(c(C.GREEN, f"  [+] Alias '{name}' -> '{cmd}' created."))

def cmd_unalias(config, args):
    if not args: return
    name = args[0]
    if name in config.get("aliases", {}):
        del config["aliases"][name]
        save_config(config)
        print(c(C.GREEN, f"  [+] Alias '{name}' removed."))

def cmd_aliases(config):
    aliases = config.get("aliases", {})
    if not aliases:
        print(c(C.YELLOW, "  [~] No aliases defined."))
        return
    print(c(C.CYAN, "\n  [ Aliases ]"))
    for k, v in aliases.items():
        print(f"  {c(C.WHITE, k):<15} -> {c(C.GRAY, v)}")
    print()

# --- HEALTH CHECK ---
def cmd_check(db, args):
    if not args:
        print(c(C.RED, "  [!] Usage: check <tool>"))
        return
    name = args[0]
    tools = {**db.get("tools",{}), **db.get("custom",{})}
    if name not in tools:
        print(c(C.RED, f"  [!] Tool '{name}' not found."))
        return
        
    path = tools[name]["path"]
    print(c(C.CYAN, f"\n  [*] Checking health for {name} ({path})..."))
    
    works = False
    output = ""
    for flag in ["--version", "-V", "--help", "-h"]:
        try:
            res = subprocess.run([path, flag], capture_output=True, text=True, timeout=5)
            if res.returncode in (0, 1):
                works = True
                output = (res.stdout or res.stderr).split('\n')[0]
                break
        except Exception:
            pass
            
    if works:
        print(c(C.GREEN, f"  [+] OK. Output: {output[:60]}..."))
    else:
        print(c(C.RED, f"  [-] Check failed or tool unresponsive."))
    print()

# --- INSTALLER ---
def ensure_sudo():
    """Ensure sudo credentials are cached so capture_output doesn't hang"""
    res = subprocess.run(["sudo", "-n", "true"], capture_output=True)
    if res.returncode != 0:
        print(c(C.YELLOW, "\n  [*] PenKit requires root privileges for system-wide operations."))
        subprocess.run(["sudo", "-v"])

def run_sudo(cmd_list):
    """Run command with sudo"""
    return subprocess.run(["sudo"] + cmd_list, capture_output=True, text=True)

def run_sudo_interactive(cmd_list):
    """Run command with sudo interactively"""
    return subprocess.run(["sudo"] + cmd_list)

def check_and_install_dependencies():
    deps = {
        "go": "golang",
        "python3": "python3 python3-pip python3-venv",
        "ruby": "ruby",
        "cargo": "cargo",
        "make": "make",
        "git": "git"
    }
    
    missing = []
    for cmd, pkg in deps.items():
        if not shutil.which(cmd):
            missing.append(pkg)
            
    if missing:
        print(c(C.CYAN, "\n  [*] PenKit relies on build tools for installing from GitHub."))
        print(c(C.YELLOW, f"  [!] Missing dependencies detected: {', '.join(missing)}"))
        print(c(C.CYAN, "  [?] Would you like to install them now via 'sudo apt'? (y/n)"))
        ans = input("  > ").strip().lower()
        if ans == 'y':
            print(c(C.CYAN, "  [*] Running 'sudo apt update'..."))
            run_sudo_interactive(["apt", "update"])
            print(c(C.CYAN, f"  [*] Installing packages..."))
            pkgs = " ".join(missing).split()
            run_sudo_interactive(["apt", "install", "-y"] + pkgs)
            print(c(C.GREEN, "  [+] Dependencies installed successfully!\n"))
        else:
            print(c(C.YELLOW, "  [~] Skipping dependency installation.\n"))

def create_symlink(src, dest):
    print(c(C.CYAN, f"  [*] Creating symlink: {dest} -> {src}"))
    res = run_sudo(["ln", "-sf", src, dest])
    if res.returncode != 0:
        print(c(C.RED, f"  [!] Symlink failed: {res.stderr}"))

def detect_and_build(target_dir, config, tool_name):
    """Detect language and build"""
    # Python
    if (target_dir / "setup.py").exists() or (target_dir / "requirements.txt").exists():
        mode = config.get("pip_mode")
        if not mode:
            print()
            print(c(C.CYAN, "  [?] Python dependencies detected. Install mode:"))
            print("      1) System-wide (--break-system-packages)")
            print("      2) Virtual environment (venv)")
            ans = input("  > ").strip()
            mode = "system" if ans == "1" else "venv"
            
        if mode == "system":
            print(c(C.CYAN, "  [*] Installing Python dependencies system-wide..."))
            req = target_dir / "requirements.txt"
            if req.exists():
                run_sudo(["pip3", "install", "-r", str(req), "--break-system-packages"])
            if (target_dir / "setup.py").exists():
                subprocess.run(["sudo", "pip3", "install", ".", "--break-system-packages"], cwd=target_dir)
        else:
            print(c(C.CYAN, "  [*] Creating venv..."))
            subprocess.run(["python3", "-m", "venv", ".venv"], cwd=target_dir)
            pip = target_dir / ".venv/bin/pip"
            req = target_dir / "requirements.txt"
            if req.exists():
                subprocess.run([str(pip), "install", "-r", str(req)], cwd=target_dir)
            if (target_dir / "setup.py").exists():
                subprocess.run([str(pip), "install", "."], cwd=target_dir)
                
            # Create a wrapper script
            wrapper = target_dir / f"{tool_name}_wrapper.sh"
            wrapper.write_text(f"#!/bin/bash\nsource {target_dir}/.venv/bin/activate\nexec python3 {target_dir}/{tool_name}.py \"$@\"\n")
            wrapper.chmod(0o755)
            return str(wrapper)

    # Go
    elif (target_dir / "go.mod").exists():
        print(c(C.CYAN, "  [*] Go project detected. Locating main package..."))
        if shutil.which("go"):
            main_files = list(target_dir.rglob("main.go"))
            if not main_files:
                print(c(C.RED, "  [!] Could not find any main.go files. Build skipped."))
                return None
                
            # Prioritize 'cmd' folders, then shortest path depth
            main_files.sort(key=lambda x: ('cmd' not in x.parts, len(x.parts)))
            main_dir = main_files[0].parent
            
            print(c(C.CYAN, f"  [*] Compiling from {main_dir.relative_to(target_dir)}... (fetching modules, please wait)"))
            
            # We don't capture output and use -v so the user sees live progress
            res = subprocess.run(["go", "build", "-v", "-o", str(target_dir / tool_name), "."], cwd=main_dir)
            
            if res.returncode == 0 and (target_dir / tool_name).exists():
                return str(target_dir / tool_name)
            else:
                print(c(C.RED, "  [!] Go build failed."))
                return None
        else:
            print(c(C.RED, "  [!] 'go' not found. Please install golang. Build skipped."))
            return None
            
    # Rust
    elif (target_dir / "Cargo.toml").exists():
        print(c(C.CYAN, "  [*] Rust project detected. Building..."))
        if shutil.which("cargo"):
            subprocess.run(["cargo", "build", "--release"], cwd=target_dir)
            bin_path = target_dir / "target/release" / tool_name
            if bin_path.exists(): return str(bin_path)
            else:
                print(c(C.RED, "  [!] Cargo build failed."))
                return None
        else:
            print(c(C.RED, "  [!] 'cargo' not found. Please install rust. Build skipped."))
            return None
            
    # Make
    elif (target_dir / "Makefile").exists():
        print(c(C.CYAN, "  [*] Makefile detected. Running make..."))
        subprocess.run(["make"], cwd=target_dir)
        
    # Find executable fallback
    for candidate in [tool_name, f"{tool_name}.py", f"{tool_name}.sh", "main.py", "main.sh", "run.sh"]:
        p = target_dir / candidate
        if p.exists() and os.access(str(p), os.X_OK) and not p.is_dir():
            return str(p)
            
    # Last resort find first executable
    for f in target_dir.rglob("*"):
        if ".git" in f.parts: continue
        if f.is_file() and os.access(str(f), os.X_OK) and f.suffix not in {".so", ".conf", ".md", ".txt"}:
            return str(f)
            
    return str(target_dir) # Just the directory

def cmd_install(db, config, url):
    if not url:
        print(c(C.RED, "  [!] Usage: install <github_url|url|path>"))
        return
        
    opt_dir = config.get("install_path", "/opt")
    bin_dir = "/usr/local/bin"
    ensure_sudo()
    
    if url.startswith("http") and "github.com" in url:
        repo_name = url.rstrip("/").split("/")[-1].replace(".git", "")
        target = Path(opt_dir) / repo_name
        
        print(c(C.CYAN, f"\n  [*] Cloning {repo_name} to {target}..."))
        # Using sudo because /opt usually requires root
        res = run_sudo(["git", "clone", url, str(target)])
        if res.returncode != 0:
            print(c(C.RED, f"  [!] Clone failed: {res.stderr}"))
            return
            
        # Give current user ownership so we can build without sudo if needed
        run_sudo(["chown", "-R", f"{os.getuid()}:{os.getgid()}", str(target)])
        
        # Build
        exe_path = detect_and_build(target, config, repo_name)
        
        if not exe_path or exe_path == str(target):
            print(c(C.RED, f"  [!] Could not build or find a valid executable for {repo_name}."))
            print(c(C.YELLOW, "  [~] Rolling back install..."))
            run_sudo(["rm", "-rf", str(target)])
            return
        
        # Symlink
        if os.path.isfile(exe_path):
            symlink_path = f"{bin_dir}/{repo_name}"
            create_symlink(exe_path, symlink_path)
            final_path = symlink_path
        else:
            final_path = exe_path
            
        # Fetch GitHub details — honour KNOWN_TOOLS first so curated entries
        # (e.g. fierce) are never mis-categorised by README keyword analysis
        cat, desc = fetch_github_info(url, config.get("github_token"))
        if repo_name.lower() in KNOWN_TOOLS:
            cat = KNOWN_TOOLS[repo_name.lower()][0]
        
        db.setdefault("custom", {})[repo_name] = {
            "path": final_path,
            "category": cat,
            "desc": desc,
            "source": "github",
            "repo_url": url,
            "install_dir": str(target),
            "added": datetime.now().isoformat()
        }
        save_db(db)
        print(c(C.GREEN, f"  [+] '{repo_name}' installed and registered.\n"))

    elif url.endswith((".zip", ".tar.gz", ".tar.bz2")):
        # Direct archive URL or file path
        fp = Path(url)
        if url.startswith("http"):
            import tempfile
            fp = Path(tempfile.gettempdir()) / url.split("/")[-1]
            print(c(C.CYAN, f"\n  [*] Downloading {url}..."))
            urllib.request.urlretrieve(url, fp)
            
        if not fp.exists():
            print(c(C.RED, f"  [!] File not found: {fp}"))
            return
            
        name = fp.name.split(".")[0]
        target = Path(opt_dir) / name
        run_sudo(["mkdir", "-p", str(target)])
        run_sudo(["chown", "-R", f"{os.getuid()}:{os.getgid()}", str(target)])
        
        print(c(C.CYAN, f"  [*] Extracting to {target}..."))
        try:
            if fp.name.endswith(".zip"):
                with zipfile.ZipFile(fp) as z: z.extractall(target)
            else:
                with tarfile.open(fp) as t: t.extractall(target)
                
            exe_path = detect_and_build(target, config, name)
            if not exe_path or exe_path == str(target):
                print(c(C.RED, f"  [!] Could not build or find a valid executable for {name}."))
                print(c(C.YELLOW, "  [~] Rolling back install..."))
                run_sudo(["rm", "-rf", str(target)])
                return
                
            if os.path.isfile(exe_path):
                symlink_path = f"{bin_dir}/{name}"
                create_symlink(exe_path, symlink_path)
                final_path = symlink_path
            else:
                final_path = exe_path
                
            db.setdefault("custom", {})[name] = {
                "path": final_path,
                "category": "unknown",
                "desc": "Installed from archive",
                "source": "archive",
                "install_dir": str(target),
                "added": datetime.now().isoformat()
            }
            save_db(db)
            print(c(C.GREEN, f"  [+] '{name}' installed.\n"))
        except Exception as e:
            print(c(C.RED, f"  [!] Extraction failed: {e}"))
    else:
        # Treat as search query
        print(c(C.CYAN, f"\n  [*] Searching GitHub for '{url}'..."))
        results = search_github_for_tool(url, config.get("github_token"))
        if not results:
            print(c(C.YELLOW, "  [~] No results found or search failed."))
            return
            
        print(c(C.CYAN, "  [ Search Results ]"))
        for idx, r in enumerate(results):
            name = r.get("full_name")
            stars = r.get("stargazers_count")
            desc = (r.get("description") or "No description").replace('\n', ' ')
            print(f"  {c(C.WHITE, str(idx+1))}) {c(C.GREEN, name)} {c(C.YELLOW, '⭐ ' + str(stars))} - {c(C.GRAY, desc[:60])}")
            
        print(c(C.CYAN, "\n  [?] Select a number to install (or enter to cancel): "))
        choice = input("  > ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(results):
            print(c(C.YELLOW, "  [~] Cancelled."))
            return
            
        selected_repo = results[int(choice)-1]["html_url"]
        
        # Recursively call install with the selected repo URL
        cmd_install(db, config, selected_repo)

# --- UNINSTALLER ---
def cmd_uninstall(db, config, args):
    if not args: return
    name = args[0]
    
    if name not in db.get("custom", {}):
        print(c(C.RED, f"  [!] Tool '{name}' not found in custom arsenal."))
        return
        
    info = db["custom"][name]
    
    print(c(C.CYAN, f"\n  [?] How would you like to uninstall '{name}'?"))
    print("      1) Arsenal only (remove from PenKit DB, keep files)")
    print("      2) System-wide  (remove files and symlinks like apt remove)")
    ans = input("  > ").strip()
    
    if ans == "1":
        del db["custom"][name]
        save_db(db)
        print(c(C.GREEN, f"  [+] '{name}' removed from Arsenal."))
    elif ans == "2":
        ensure_sudo()
        inst_dir = info.get("install_dir")
        if inst_dir and os.path.exists(inst_dir):
            print(c(C.CYAN, f"  [*] Removing {inst_dir}..."))
            run_sudo(["rm", "-rf", inst_dir])
        
        symlink = f"/usr/local/bin/{name}"
        if os.path.exists(symlink) or os.path.islink(symlink):
            print(c(C.CYAN, f"  [*] Removing symlink {symlink}..."))
            run_sudo(["rm", "-f", symlink])
            
        del db["custom"][name]
        save_db(db)
        print(c(C.GREEN, f"  [+] '{name}' uninstalled system-wide.\n"))
        print(c(C.CYAN, "  [*] Rescanning system to update tool list..."))
        db["tools"] = scan_system(silent=True)
        save_db(db)
        print(c(C.GREEN, "  [+] Tool list updated.\n"))
    else:
        print(c(C.YELLOW, "  [~] Aborted."))

# --- UPDATER ---
def update_tool(name, info, config):
    if info.get("source") != "github":
        return False
    inst_dir = info.get("install_dir")
    if not inst_dir or not os.path.exists(inst_dir):
        return False
        
    print(c(C.CYAN, f"\n  [*] Updating {name} in {inst_dir}..."))
    res = subprocess.run(["git", "pull"], cwd=inst_dir, capture_output=True, text=True)
    if res.returncode == 0:
        if "Already up to date." in res.stdout:
            print(c(C.GREEN, "  [+] Already up to date."))
        else:
            print(c(C.GREEN, "  [+] Pulled latest changes."))
            detect_and_build(Path(inst_dir), config, name)
    else:
        print(c(C.RED, f"  [!] Git pull failed: {res.stderr}"))
        
    return True

def cmd_update(db, config, args):
    if not args:
        print(c(C.RED, "  [!] Usage: update <tool> or update --all"))
        return
        
    ensure_sudo()
    target = args[0]
    if target == "--all":
        count = 0
        for name, info in db.get("custom", {}).items():
            if update_tool(name, info, config):
                count += 1
        print(c(C.GREEN, f"\n  [+] Completed updates for {count} tools.\n"))
    else:
        info = db.get("custom", {}).get(target)
        if info:
            update_tool(target, info, config)
            print()
        else:
            print(c(C.RED, f"  [!] Tool '{target}' not found in custom arsenal."))

# --- RUNNER ---
def execute_tool(db, config, cmd, args):
    # Check aliases first
    aliases = config.get("aliases", {})
    if cmd in aliases:
        aliased = aliases[cmd].split()
        cmd = aliased[0]
        args = aliased[1:] + args
        
    tools = {**db.get("tools", {}), **db.get("custom", {})}
    
    if cmd in tools:
        path = tools[cmd]["path"]
        # If it's a symlink or command name
        full_cmd = [path] + args
        print(c(C.GREEN, f"  [>] Running: {' '.join(full_cmd)}\n"))
        try:
            subprocess.run(full_cmd)
        except KeyboardInterrupt:
            print(c(C.YELLOW, "\n  [~] Interrupted."))
        except Exception as e:
            print(c(C.RED, f"  [!] Error executing tool: {e}"))
        print()
        return True
    return False

# --- UI COMMANDS ---
def _print_table(tools, title):
    if not tools:
        print(c(C.YELLOW, "\n  [~] No tools found.\n"))
        return
    print()
    
    W = 83
    name_w = 25
    cat_w = 15
    desc_w = 41
    
    title_len = len(title)
    count_str = str(len(tools))
    dash_count = max(0, 79 - title_len - len(count_str))
    
    print(c(C.CYAN, f"  ╭─ {title} ({count_str}) {'─'*dash_count}╮"))
    print(c(C.CYAN, "  │ ") + c(C.BOLD, f"{'NAME':<{name_w}} {'CATEGORY':<{cat_w}} {'DESCRIPTION':<{desc_w}}") + c(C.CYAN, " │"))
    print(c(C.CYAN, "  ├" + "─"*(W+2) + "┤"))
    
    sorted_tools = sorted(tools.items(), key=lambda item: (item[1].get("category", "unknown"), item[0]))
    for name, info in sorted_tools:
        cat = info.get("category", "unknown")
        col = CAT_COLORS.get(cat, C.GRAY)
        desc = info.get("desc", "")
        
        desc_lines = textwrap.wrap(desc, width=desc_w)
        if not desc_lines:
            desc_lines = [""]
            
        name_pad = f"{name:<{name_w}}"
        cat_pad = f"{cat:<{cat_w}}"
        desc_pad = f"{desc_lines[0]:<{desc_w}}"
        
        row = f"{c(C.WHITE, name_pad)} {c(col, cat_pad)} {c(C.WHITE, desc_pad)}"
        print(c(C.CYAN, "  │ ") + row + c(C.CYAN, " │"))
        
        for line in desc_lines[1:]:
            row2 = f"{' ':<{name_w}} {' ':<{cat_w}} {c(C.WHITE, f'{line:<{desc_w}}')}"
            print(c(C.CYAN, "  │ ") + row2 + c(C.CYAN, " │"))
            
    print(c(C.CYAN, "  ╰" + "─"*(W+2) + "╯\n"))

def cmd_search(db, query):
    if not query: return
    tools = {**db.get("tools", {}), **db.get("custom", {})}
    q = query.lower()
    res = {n: i for n, i in tools.items() if q in n.lower() or q in i.get("desc", "").lower() or q in i.get("category", "").lower()}
    _print_table(res, f"Search Results: {query}")

def cmd_list(db, cat=None):
    tools = {**db.get("tools", {}), **db.get("custom", {})}
    if cat:
        tools = {n: i for n, i in tools.items() if i.get("category", "").lower() == cat.lower()}
        _print_table(tools, f"Category: {cat}")
    else:
        _print_table(tools, "Loaded Arsenal")

def cmd_info(db, name):
    tools = {**db.get("tools", {}), **db.get("custom", {})}
    info = tools.get(name)
    if not info:
        print(c(C.RED, f"\n  [!] Tool '{name}' not found.\n"))
        return
    cat = info.get("category", "unknown")
    col = CAT_COLORS.get(cat, C.GRAY)
    print()
    print(c(C.CYAN, "  ╔════════════════════════════════════════════════════════════════╗"))
    print(c(C.CYAN, "  ║ ") + c(C.WHITE + C.BOLD, f"{name:<62}") + c(C.CYAN, " ║"))
    print(c(C.CYAN, "  ╠════════════════════════════════════════════════════════════════╣"))
    for k, v in [
        ("Category", c(col, cat)),
        ("Path", info.get("path", "n/a")),
        ("Source", info.get("source", "n/a")),
        ("Desc", info.get("desc", "n/a")),
        ("Repo", info.get("repo_url", "n/a")),
        ("Added", info.get("added", "n/a")[:16].replace("T", " "))
    ]:
        # Strip ansi to get visible length
        clean_v = re.sub(r'\033\[[0-9;]*m', '', str(v))
        padding = max(0, 51 - len(clean_v))
        print(c(C.CYAN, "  ║ ") + c(C.GRAY, f"{k:<10} ") + f"{v}{' '*padding}" + c(C.CYAN, " ║"))
    print(c(C.CYAN, "  ╠════════════════════════════════════════════════════════════════╣"))

    # Live --help output (first 8 lines, stripped of color for readability)
    tool_path = info.get("path", name)
    help_output = None
    for flag in ["--help", "-h"]:
        try:
            res = subprocess.run(
                [tool_path, flag],
                capture_output=True, text=True, timeout=5
            )
            raw = (res.stdout or res.stderr or "").strip()
            if raw:
                help_output = raw
                break
        except Exception:
            pass

    print(c(C.CYAN, "  ║ ") + c(C.GRAY, f"{'Help':<10} ") + c(C.DIM, f"{'live output':<51}") + c(C.CYAN, " ║"))
    if help_output:
        lines = help_output.splitlines()[:8]
        for line in lines:
            clean = re.sub(r'\033\[[0-9;]*m', '', line)[:60]
            padding = max(0, 61 - len(clean))
            print(c(C.CYAN, "  ║ ") + f"  {c(C.GRAY, clean)}{' '*padding}" + c(C.CYAN, "║"))
    else:
        print(c(C.CYAN, "  ║ ") + c(C.GRAY, f"  {'No --help output available':<61}") + c(C.CYAN, "║"))

    print(c(C.CYAN, "  ╚════════════════════════════════════════════════════════════════╝\n"))

def cmd_categories(db):
    tools = {**db.get("tools", {}), **db.get("custom", {})}
    cats = {}
    for i in tools.values():
        c_ = i.get("category", "unknown")
        cats[c_] = cats.get(c_, 0) + 1
    print(c(C.CYAN, "\n  [ Categories ]"))
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        col = CAT_COLORS.get(cat, C.GRAY)
        bar = "█" * min(count, 30)
        print(f"  {c(col, f'{cat:<15}')} {c(C.GRAY, bar)} {c(C.WHITE, count)}")
    print()

def cmd_add(db, args):
    if len(args) < 2: return
    name, cmd = args[0], " ".join(args[1:])
    db.setdefault("custom", {})[name] = {
        "path": cmd, "category": "custom", "desc": "Manually added tool",
        "source": "manual", "added": datetime.now().isoformat()
    }
    save_db(db)
    print(c(C.GREEN, f"  [+] '{name}' registered.\n"))

def cmd_tag(db, args):
    if len(args) < 2: return
    name, cat = args[0], args[1]
    for store in ("tools", "custom"):
        if name in db.get(store, {}):
            db[store][name]["category"] = cat
            db[store][name]["manually_tagged"] = True
            save_db(db)
            print(c(C.GREEN, f"  [+] '{name}' tagged as '{cat}'.\n"))
            return
    print(c(C.RED, f"  [!] Tool '{name}' not found.\n"))

def cmd_help():
    print(c(C.CYAN, "\n  [ Commands ]"))
    commands = [
        ("<tool> [args...]", "Run a tool directly"),
        ("search <query>", "Search tools by name/desc/category"),
        ("list [category]", "List tools"),
        ("info <tool>", "Show tool details"),
        ("scan", "Rescan system for known tools"),
        ("install <url>", "Install tool from GitHub or URL"),
        ("update <tool/--all>","Update GitHub-installed tool(s)"),
        ("uninstall <tool>", "Uninstall a custom tool"),
        ("check <tool>", "Health check a tool"),
        ("add <name> <cmd>", "Add a manual tool entry"),
        ("remove <tool>", "Remove tool from DB only"),
        ("categories", "Show categories and counts"),
        ("tag <tool> <cat>", "Change tool category"),
        ("alias <name> <cmd>", "Create an alias"),
        ("aliases", "List aliases"),
        ("unalias <name>", "Remove alias"),
        ("config", "Manage settings and tokens"),
        ("history", "Show command history"),
        ("clear", "Clear screen"),
        ("exit", "Quit"),
    ]
    for cmd, desc in commands:
        print(f"  {c(C.GREEN, cmd.ljust(20))} {c(C.GRAY, desc)}")
    print()

def cmd_history():
    print(c(C.CYAN, "\n  [ Command History ]"))
    if readline:
        for i in range(1, readline.get_current_history_length() + 1):
            print(f"  {i:3d}  {readline.get_history_item(i)}")
    else:
        print(c(C.YELLOW, "  [!] History not supported on this OS."))
    print()

# --- MAIN & CLI ---
def load_history():
    if readline and HISTORY_FILE.exists():
        readline.read_history_file(str(HISTORY_FILE))

def save_history():
    if readline:
        readline.write_history_file(str(HISTORY_FILE))

def setup_autocomplete(db, config):
    if not readline: return
    cmds = ["search", "list", "info", "scan", "install", "update", "uninstall", 
            "check", "add", "remove", "categories", "tag", "alias", "aliases", 
            "unalias", "config", "history", "clear", "help", "exit"]
    tools = list(db.get("tools", {}).keys()) + list(db.get("custom", {}).keys())
    aliases = list(config.get("aliases", {}).keys())
    options = cmds + tools + aliases
    
    def completer(text, state):
        matches = [c for c in options if c.startswith(text)]
        try: return matches[state]
        except IndexError: return None
        
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

def get_remote_version(url):
    """Fetch the VERSION string from the remote file without downloading the whole thing."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PenKit-AutoUpdate"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            for line in resp:
                decoded = line.decode("utf-8", errors="ignore").strip()
                if decoded.startswith("VERSION"):
                    parts = decoded.split("=")
                    if len(parts) == 2:
                        return parts[1].strip().strip("\"' ")
                if resp.tell() > 4096:
                    break
    except Exception:
        pass
    return None


def do_self_update(url, current_file):
    """Download remote file and replace the running script."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PenKit-AutoUpdate"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            new_src = resp.read()
        tmp = current_file + ".tmp"
        with open(tmp, "wb") as f:
            f.write(new_src)
        os.replace(tmp, current_file)
        return True
    except Exception:
        return False


def check_for_update(config, current_file):
    """
    Background thread: check GitHub for a newer version once per week.
    Prints a one-line notice if an update was applied; silent otherwise.
    """
    last_check = config.get("last_update_check")
    if last_check:
        try:
            delta = datetime.now() - datetime.fromisoformat(last_check)
            if delta.days < UPDATE_CHECK_INTERVAL_DAYS:
                return
        except Exception:
            pass

    remote_ver = get_remote_version(UPDATE_URL)

    config["last_update_check"] = datetime.now().isoformat()
    save_config(config)

    if not remote_ver:
        return

    if remote_ver == VERSION:
        return

    success = do_self_update(UPDATE_URL, current_file)
    if success:
        print(c(C.GREEN, f"\n  [+] PenKit auto-updated {VERSION} → {remote_ver}. Restart to apply.\n"))


def spawn_update_check(config):
    """Launch the update check in a daemon background thread."""
    current_file = os.path.abspath(__file__)
    t = threading.Thread(
        target=check_for_update,
        args=(config, current_file),
        daemon=True
    )
    t.start()


def interactive_loop(db, config):
    banner_gradient(db)
    check_token_expiry(config)
    
    tc = len(db.get("tools",{})) + len(db.get("custom",{}))
    ls = db.get("last_scan", "never")[:16].replace("T", " ")
    print(c(C.GRAY, f"  Loaded Arsenal: {c(C.WHITE, tc)} tools  |  Last Scan: {c(C.WHITE, ls)}\n"))
    
    setup_autocomplete(db, config)
    load_history()
    
    prompt = c(C.RED, "pk") + c(C.WHITE, " > ")
    
    while True:
        try:
            raw = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print(c(C.CYAN, "\n  [*] Exiting... Stay ethical.\n"))
            break
            
        if not raw: continue
        parts = raw.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd in ("exit", "quit"):
            print(c(C.CYAN, "\n  [*] Exiting... Stay ethical.\n"))
            break
            
        elif cmd == "run" and args: execute_tool(db, config, args[0], args[1:])
        elif cmd == "help": cmd_help()
        elif cmd == "search": cmd_search(db, " ".join(args))
        elif cmd == "list": cmd_list(db, args[0] if args else None)
        elif cmd == "info": cmd_info(db, args[0] if args else "")
        elif cmd == "scan": 
            db["tools"] = scan_system(existing=db.get("tools"))
            db["last_scan"] = datetime.now().isoformat()
            save_db(db)
        elif cmd == "install": cmd_install(db, config, args[0] if args else "")
        elif cmd == "update": cmd_update(db, config, args)
        elif cmd == "uninstall": cmd_uninstall(db, config, args)
        elif cmd == "check": cmd_check(db, args)
        elif cmd == "add": cmd_add(db, args)
        elif cmd == "remove": 
            if args and args[0] in db.get("custom", {}):
                del db["custom"][args[0]]
                save_db(db)
                print(c(C.GREEN, "  [+] Removed from arsenal."))
        elif cmd == "categories": cmd_categories(db)
        elif cmd == "tag": cmd_tag(db, args)
        elif cmd == "alias": cmd_alias(config, args)
        elif cmd == "unalias": cmd_unalias(config, args)
        elif cmd == "aliases": cmd_aliases(config)
        elif cmd == "config": cmd_config(config, args)
        elif cmd == "history": cmd_history()
        elif cmd == "clear": banner_gradient(db)
        else:
            # Try to execute as tool
            if not execute_tool(db, config, cmd, args):
                print(c(C.RED, f"  [!] Unknown command or tool: '{cmd}'"))
                
    save_history()

def main():
    parser = argparse.ArgumentParser(description=f"PenKit v{VERSION} CLI  |  {AUTHOR}")
    parser.add_argument("--scan", action="store_true", help="Scan system for tools")
    parser.add_argument("--install", type=str, help="Install tool from URL")
    parser.add_argument("--update-all", action="store_true", help="Update all custom tools")
    parser.add_argument("--list", type=str, nargs="?", const="all", help="List tools")
    
    args, unknown = parser.parse_known_args()
    
    db = load_db()
    config = load_config()

    # Kick off background update check (non-blocking, once per week)
    spawn_update_check(config)

    first_run = not db.get("tools")
    if first_run:
        print(c(C.YELLOW, "\n  [*] First run detected. Checking system environment..."))
        check_and_install_dependencies()
        
    # If any arg is passed that interactive loop doesn't handle, we exit after
    if args.scan or args.install or args.update_all or args.list:
        if args.scan:
            db["tools"] = scan_system(existing=db.get("tools"))
            db["last_scan"] = datetime.now().isoformat()
            save_db(db)
        if args.install:
            cmd_install(db, config, args.install)
        if args.update_all:
            cmd_update(db, config, ["--all"])
        if args.list:
            cmd_list(db, args.list if args.list != "all" else None)
        return

    # First run interactive scan
    if first_run:
        print(c(C.YELLOW, "  [*] Running initial scan..."))
        db["tools"] = scan_system()
        db["last_scan"] = datetime.now().isoformat()
        save_db(db)

    interactive_loop(db, config)

if __name__ == "__main__":
    main()
