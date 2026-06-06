#!/usr/bin/env bash
# PenKit v1.0 Installer

RED='\033[38;5;196m'
GREEN='\033[38;5;46m'
CYAN='\033[38;5;51m'
YELLOW='\033[38;5;226m'
RESET='\033[0m'

echo -e "${CYAN}"
echo "  ██████╗ ███████╗███╗   ██╗██╗  ██╗██╗████████╗"
echo "  ██╔══██╗██╔════╝████╗  ██║██║ ██╔╝██║╚══██╔══╝"
echo "  ██████╔╝█████╗  ██╔██╗ ██║█████╔╝ ██║   ██║   "
echo "  ██╔═══╝ ██╔══╝  ██║╚██╗██║██╔═██╗ ██║   ██║   "
echo "  ██║     ███████╗██║ ╚████║██║  ██╗██║   ██║   "
echo "  ╚═╝     ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝   ╚═╝   "
echo "                                            Installer v1.0    "
echo -e "${RESET}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.penkit"
BIN_PATH="/usr/local/bin/penkit"

# Check Python3
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[!] Python3 is required but not found.${RESET}"
    exit 1
fi

echo -e "${GREEN}[+] Python3 found: $(python3 --version)${RESET}"

# Create config dir
mkdir -p "$INSTALL_DIR/custom_tools"
echo -e "${GREEN}[+] Config directory: $INSTALL_DIR${RESET}"

# Copy main script
cp "$SCRIPT_DIR/penkit.py" "$INSTALL_DIR/penkit.py"
chmod +x "$INSTALL_DIR/penkit.py"

# Create launcher in /usr/local/bin
echo -e "${CYAN}[*] Installing system-wide launcher...${RESET}"

cat > /tmp/penkit_launcher << 'LAUNCHER'
#!/usr/bin/env bash
exec python3 "$HOME/.penkit/penkit.py" "$@"
LAUNCHER

sudo mv /tmp/penkit_launcher "$BIN_PATH"
sudo chmod +x "$BIN_PATH"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[+] Installed to $BIN_PATH${RESET}"
else
    # Fallback: install to ~/.local/bin
    mkdir -p "$HOME/.local/bin"
    cp /tmp/penkit_launcher "$HOME/.local/bin/penkit" 2>/dev/null || true
    chmod +x "$HOME/.local/bin/penkit" 2>/dev/null || true
    echo -e "${YELLOW}[~] Installed to ~/.local/bin/penkit (add to PATH if needed)${RESET}"
fi

echo ""
echo -e "${GREEN}✔  Done! Run 'penkit' to launch your arsenal.${RESET}"
echo ""
