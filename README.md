# 🕵️ StegoBox - Advanced Steganography Tool

<div align="center">

![StegoBox Logo](assets/custom_icon.png)

**Hide your secrets in plain sight with military-grade steganography**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com)

*Created with ❤️ by [@Risterz](https://github.com/Risterz) for the security and privacy community*

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🎮 Demo](#-demo) • [🔒 Security](#-security) • [🤝 Contributing](#-contributing)

</div>

---

## 🌟 Overview

StegoBox is a modern, user-friendly steganography tool that allows you to hide folders and ZIP files inside images with a beautiful GUI interface. Perfect for secure data storage, confidential file transfer, and digital privacy protection.

### ✨ Key Features

🔐 **Dual Steganography Methods**
- **Append Mode**: Lightning-fast hiding with simple concatenation
- **LSB Mode**: Invisible hiding using Least Significant Bit embedding

🎨 **Modern Interface** 
- Beautiful dark/light theme support
- Intuitive tabbed design for embedding and extraction
- Real-time progress tracking with visual feedback
- Smart file dialogs with format recommendations

🛡️ **Military-Grade Security**
- AES-256 encryption with PBKDF2 key derivation
- 200,000 security iterations for maximum protection
- Cryptographically secure random salt generation
- Password strength validation

📦 **Zero-Installation Distribution**
- Single-file Windows executable (.exe)
- Portable and completely standalone
- No dependencies or installation required

## 📁 Project Structure

```
StegoBox/
├── 🎯 src/                    # Core application source code
│   ├── example.py             # Steganography engine & CLI interface
│   ├── gui_app.py             # Modern GUI application (CustomTkinter)
│   ├── setup.py               # Automated setup and installation
│   └── requirements.txt       # Python dependencies
├── 📚 docs/                   # Comprehensive documentation
│   ├── USER_GUIDE.md          # Step-by-step user instructions
│   ├── DEVELOPER_GUIDE.md     # Developer API and architecture
│   └── CHANGELOG.md           # Version history and updates
├── 🎨 assets/                 # Icons, images, and branding
│   ├── custom_icon.ico        # Windows application icon
│   ├── custom_icon.png        # High-resolution PNG icon
│   └── screenshots/           # Demo images and screenshots
├── 🧪 examples/               # Demo scripts and utilities
│   ├── demo.py                # Interactive demonstration
│   ├── create_icon.py         # Icon generation utility
│   └── convert_custom_icon.py # Icon format conversion
├── 🔨 build/                  # Build system and distribution
│   ├── build.py               # Automated executable builder
│   ├── StegoBox.spec          # PyInstaller configuration
│   └── dist/                  # Generated executables
├── stegobox_gui.py            # Main application launcher
└── requirements.txt           # Root dependencies file
```

## 🚀 Quick Start

### 🖥️ Option 1: Ready-to-Use Executable
1. **Download** the latest `StegoBox.exe` from [Releases](../../releases)
2. **Double-click** to launch - no installation needed!
3. **Start hiding** your secrets immediately

### 🐍 Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/Risterz/StegoBox.git
cd StegoBox

# Install dependencies
pip install -r requirements.txt

# Launch the GUI
python stegobox_gui.py
```

### ⚡ Option 3: Command Line Interface
```bash
# Navigate to source directory
cd src

# See all available options
python example.py --help

# Hide a folder in an image
python example.py hide image.png secret_folder/ output.png

# Extract hidden data
python example.py extract stego_image.png recovered_data.zip
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [📋 User Guide](docs/USER_GUIDE.md) | Complete step-by-step instructions |
| [👨‍💻 Developer Guide](docs/DEVELOPER_GUIDE.md) | API reference and architecture |
| [📝 Changelog](docs/CHANGELOG.md) | Version history and updates |

## 🎮 Demo

Experience StegoBox in action with our interactive demonstration:

```bash
cd examples
python demo.py
```

**Demo Features:**
- ✅ Live demonstration of both steganography methods
- ✅ Password encryption and security testing
- ✅ Capacity calculation examples
- ✅ File format compatibility verification
- ✅ Performance benchmarking
- ✅ Error handling demonstration

## 🛡️ Security Features

### 🔐 Encryption Specifications (LSB Mode)

| Feature | Specification |
|---------|---------------|
| **Encryption Algorithm** | AES-256 via Fernet |
| **Key Derivation** | PBKDF2-HMAC-SHA256 |
| **Security Iterations** | 200,000 (configurable) |
| **Salt Generation** | 16 bytes cryptographically secure |
| **Password Policy** | User-defined strength validation |

### 🕵️ Detection Resistance

| Method | Stealth Level | Detection Risk | File Size Impact |
|--------|---------------|----------------|------------------|
| **Append Mode** | ⚠️ Low | High (easily detected) | Significant increase |
| **LSB Mode** | 🛡️ Very High | Minimal (virtually invisible) | No change |

### 📊 Capacity Guidelines

| Image Resolution | LSB Capacity | Recommended Use |
|------------------|-------------|-----------------|
| 1920×1080 (Full HD) | ~780 KB | Documents, small files |
| 3840×2160 (4K) | ~3.1 MB | Photo collections, archives |
| 5000×5000 (High Res) | ~9.5 MB | Large datasets, videos |

**Capacity Formula**: `(width × height × 3) ÷ 8` bytes

## 🎯 Use Cases

### 👔 Professional Applications
- **Secure Document Archival**: Long-term storage with invisible protection
- **Digital Watermarking**: Copyright protection for creative works
- **Confidential Communications**: Secure file transfer without detection
- **Evidence Storage**: Forensic data preservation with integrity

### 🎓 Educational Purposes  
- **Cryptography Demonstrations**: Hands-on steganography learning
- **Security Awareness Training**: Privacy protection education
- **Digital Forensics**: Investigative technique practice
- **Research Projects**: Privacy technology development

### 🏠 Personal Use
- **Private Photo Protection**: Hidden metadata in family photos
- **Secure File Sharing**: No-cloud confidential transfers
- **Digital Time Capsules**: Future message embedding
- **Creative Projects**: Artistic hidden content creation

## 🔨 Building from Source

### Prerequisites
```bash
# Install Python 3.8+
python --version

# Install build dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### Create Executable
```bash
# Navigate to build directory
cd build

# Run automated build
python build.py

# Your executable will be in build/dist/StegoBox.exe
```

### Custom Icon (Optional)
```bash
# Generate custom icon
cd examples
python create_icon.py

# Convert to Windows format
python convert_custom_icon.py
```

## ⚖️ Legal & Ethical Guidelines

### ✅ Appropriate Uses
- Personal data protection and privacy
- Educational demonstrations and research
- Legitimate business security applications
- Creative and artistic projects
- Authorized security testing

### ❌ Prohibited Uses
- Unauthorized data hiding on systems you don't own
- Bypassing organizational security policies
- Illegal content distribution or storage
- Copyright or intellectual property violations
- Circumventing lawful investigations

**⚠️ Important**: Users are solely responsible for complying with all applicable laws and regulations in their jurisdiction.

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Bug Reports
1. Check existing [issues](../../issues) first
2. Create detailed bug report with reproduction steps
3. Include system information and error messages

### 💡 Feature Requests
1. Search existing [discussions](../../discussions) 
2. Propose new features with clear use cases
3. Consider implementation complexity and user benefit

### 🔧 Code Contributions
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### 🧪 Testing
- Run `python examples/demo.py` to verify functionality
- Test on multiple operating systems when possible
- Include test cases for new features

## 📞 Support & Troubleshooting

### 🆘 Common Issues

<details>
<summary><strong>"Payload too large for this image"</strong></summary>

**Solutions:**
- Use a larger, higher-resolution image
- Compress your data before hiding (zip with maximum compression)
- Switch to Append mode for unlimited capacity
- Use PNG or BMP format for maximum LSB capacity
</details>

<details>
<summary><strong>"Password required to decrypt"</strong></summary>

**Solutions:**
- The data was encrypted during embedding - enter the correct password
- Try extracting without a password first (data might not be encrypted)
- Verify you're using the exact same password as during embedding
</details>

<details>
<summary><strong>"No hidden data found"</strong></summary>

**Solutions:**
- Verify the image actually contains hidden data
- Try both extraction methods (auto-detection should work)
- Check if the image was modified after embedding
- Ensure the image format supports the embedding method used
</details>

<details>
<summary><strong>GUI won't start</strong></summary>

**Solutions:**
- Install all dependencies: `pip install -r requirements.txt`
- Update Python to 3.8+ if needed
- Try running: `python stegobox_gui.py` from command line
- Check for specific error messages in terminal output
</details>

### 📧 Getting Help
- 💬 [GitHub Discussions](../../discussions) - Community support and questions
- 🐛 [Issue Tracker](../../issues) - Bug reports and feature requests
- 📖 [Documentation](docs/) - Comprehensive guides and references

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### 🛠️ Built With
- **[Python](https://python.org)** - Core programming language
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern GUI framework
- **[Pillow (PIL)](https://pillow.readthedocs.io/)** - Image processing library
- **[Cryptography](https://cryptography.io/)** - Security and encryption
- **[PyInstaller](https://pyinstaller.org/)** - Executable generation

### 🌟 Special Thanks
- The open-source community for inspiring this project
- Security researchers advancing steganography techniques
- Beta testers who provided valuable feedback
- Contributors who helped improve the codebase

---

<div align="center">

**🔒 Protect Your Digital Privacy with StegoBox**

*Made with ❤️ by [@Risterz](https://github.com/Risterz)*

**[⭐ Star this project](../../stargazers) • [🍴 Fork it](../../fork) • [📢 Share it](../../)**

*"The best place to hide something is in plain sight"*

</div>