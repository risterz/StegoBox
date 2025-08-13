# 👨‍💻 StegoBox Developer Guide

**Complete technical documentation for developers and contributors**

---

## 📑 Table of Contents

1. [🏗️ Architecture Overview](#️-architecture-overview)
2. [📁 Project Structure](#-project-structure)
3. [🔧 Development Setup](#-development-setup)
4. [📚 API Reference](#-api-reference)
5. [🧪 Testing Framework](#-testing-framework)
6. [🔨 Building & Distribution](#-building--distribution)
7. [🤝 Contributing Guidelines](#-contributing-guidelines)
8. [🔍 Code Standards](#-code-standards)
9. [🚀 Deployment](#-deployment)

---

## 🏗️ Architecture Overview

### System Design

StegoBox follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────┐
│                 GUI Layer                   │
│            (gui_app.py)                     │
├─────────────────────────────────────────────┤
│               Core Engine                   │
│            (example.py)                     │
├─────────────────────────────────────────────┤
│              Utilities                      │
│         (Crypto, Image, File I/O)          │
├─────────────────────────────────────────────┤
│            External Libraries               │
│    (Pillow, Cryptography, CustomTkinter)   │
└─────────────────────────────────────────────┘
```

### Key Components

#### 1. Core Engine (`src/example.py`)
- **Steganography algorithms**: LSB and Append implementations
- **Cryptographic functions**: AES encryption with PBKDF2
- **File operations**: ZIP handling and payload management
- **CLI interface**: Command-line argument parsing and execution

#### 2. GUI Application (`src/gui_app.py`)
- **Modern interface**: CustomTkinter-based responsive UI
- **Threading**: Non-blocking operations with progress feedback
- **State management**: Method selection and configuration persistence
- **Error handling**: User-friendly error messages and validation

#### 3. Main Launcher (`stegobox_gui.py`)
- **Entry point**: Application initialization and path management
- **Dependency handling**: Graceful fallback to CLI if GUI unavailable
- **Error recovery**: Import error handling and user guidance

### Data Flow

#### Embedding Process
```
Input Data → ZIP Compression → Optional Encryption → 
Steganographic Embedding → Output Stego Image
```

#### Extraction Process
```
Stego Image → Method Detection → Data Extraction → 
Optional Decryption → ZIP Output
```

---

## 📁 Project Structure

### Directory Layout
```
StegoBox/
├── 🎯 src/                    # Core application code
│   ├── example.py             # Steganography engine & CLI
│   ├── gui_app.py             # GUI application
│   ├── setup.py               # Installation utilities
│   └── requirements.txt       # Python dependencies
├── 📚 docs/                   # Documentation
│   ├── USER_GUIDE.md          # End-user documentation
│   ├── DEVELOPER_GUIDE.md     # This file
│   └── CHANGELOG.md           # Version history
├── 🎨 assets/                 # Static resources
│   ├── custom_icon.ico        # Application icon
│   ├── custom_icon.png        # High-res icon
│   └── screenshots/           # Demo images
├── 🧪 examples/               # Testing and demos
│   ├── demo.py                # Interactive demonstration
│   ├── create_icon.py         # Icon generation
│   └── convert_custom_icon.py # Icon utilities
├── 🔨 build/                  # Build system
│   ├── build.py               # Executable builder
│   ├── StegoBox.spec          # PyInstaller config
│   ├── version_info.txt       # Version metadata
│   └── dist/                  # Built executables
├── stegobox_gui.py            # Main application launcher
├── requirements.txt           # Root dependencies
└── README.md                  # Project overview
```

### File Responsibilities

| File | Purpose | Dependencies |
|------|---------|--------------|
| `src/example.py` | Core steganography algorithms, CLI interface | Pillow, cryptography |
| `src/gui_app.py` | Modern GUI with CustomTkinter | CustomTkinter, threading |
| `stegobox_gui.py` | Main launcher and path management | None (graceful fallback) |
| `build/build.py` | Automated executable generation | PyInstaller |
| `examples/demo.py` | Interactive testing and demonstration | All core dependencies |

---

## 🔧 Development Setup

### Prerequisites

#### Required Software
- **Python 3.8+**: Core runtime environment
- **Git**: Version control and repository management
- **Code Editor**: VS Code, PyCharm, or preferred IDE

#### Optional Tools
- **PyInstaller**: For creating standalone executables
- **Virtual Environment**: Isolated development environment
- **Linter**: flake8, black, or preferred code formatter

### Environment Setup

#### 1. Clone Repository
```bash
git clone https://github.com/Risterz/StegoBox.git
cd StegoBox
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pyinstaller pytest black flake8
```

#### 4. Verify Installation
```bash
# Test CLI functionality
cd src
python example.py --help

# Test GUI launch
cd ..
python stegobox_gui.py

# Run comprehensive demo
cd examples
python demo.py
```

### Development Workflow

#### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/new-algorithm

# Make changes and test
python examples/demo.py

# Commit changes
git add .
git commit -m "Add new steganography algorithm"
```

#### 2. Testing
```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
cd examples
python demo.py

# Manual testing
python stegobox_gui.py
```

#### 3. Code Quality
```bash
# Format code
black src/ examples/ build/

# Check linting
flake8 src/ examples/ build/

# Type checking (if using mypy)
mypy src/
```

---

## 📚 API Reference

### Core Functions (`src/example.py`)

#### Steganography Functions

##### `append_embed(cover_path, payload, output_path)`
Embeds data using the append method.

**Parameters:**
- `cover_path` (str): Path to cover image
- `payload` (bytes): Data to hide
- `output_path` (str): Output stego image path

**Returns:** None

**Raises:**
- `FileNotFoundError`: If cover image doesn't exist
- `IOError`: If unable to write output file

```python
# Example usage
with open('secret.zip', 'rb') as f:
    payload = f.read()
append_embed('cover.png', payload, 'stego.png')
```

##### `append_extract(stego_path)`
Extracts data using the append method.

**Parameters:**
- `stego_path` (str): Path to stego image

**Returns:** `bytes` - Extracted payload

**Raises:**
- `ValueError`: If no hidden data found
- `struct.error`: If data is corrupted

```python
# Example usage
try:
    payload = append_extract('stego.png')
    with open('recovered.zip', 'wb') as f:
        f.write(payload)
except ValueError:
    print("No hidden data found")
```

##### `lsb_embed(cover_path, payload, output_path)`
Embeds data using LSB steganography.

**Parameters:**
- `cover_path` (str): Path to cover image (PNG/BMP recommended)
- `payload` (bytes): Data to hide (must fit in image capacity)
- `output_path` (str): Output stego image path

**Returns:** None

**Raises:**
- `ValueError`: If payload too large for image
- `PIL.UnidentifiedImageError`: If image format unsupported

```python
# Example usage with capacity check
capacity = lsb_capacity('cover.png')
if len(payload) <= capacity:
    lsb_embed('cover.png', payload, 'stego.png')
else:
    print(f"Payload too large: {len(payload)} > {capacity}")
```

##### `lsb_extract(stego_path)`
Extracts data using LSB steganography.

**Parameters:**
- `stego_path` (str): Path to stego image

**Returns:** `bytes` - Extracted payload

**Raises:**
- `ValueError`: If no valid LSB data found
- `struct.error`: If header is corrupted

##### `lsb_capacity(image_path)`
Calculates LSB embedding capacity of an image.

**Parameters:**
- `image_path` (str): Path to image file

**Returns:** `int` - Maximum payload size in bytes

```python
# Example capacity calculation
capacity = lsb_capacity('image.png')
print(f"Image can hide {capacity:,} bytes ({capacity/1024:.1f} KB)")
```

#### Cryptographic Functions

##### `encrypt_payload(payload, password)`
Encrypts payload using AES-256 with PBKDF2.

**Parameters:**
- `payload` (bytes): Data to encrypt
- `password` (str): Encryption password

**Returns:** `bytes` - Encrypted payload with salt

**Security:**
- Uses PBKDF2-HMAC-SHA256 with 200,000 iterations
- 16-byte cryptographically secure random salt
- AES-256 encryption via Fernet

```python
# Example encryption
encrypted = encrypt_payload(b"secret data", "strong_password")
```

##### `decrypt_payload(encrypted_payload, password)`
Decrypts payload encrypted with `encrypt_payload()`.

**Parameters:**
- `encrypted_payload` (bytes): Encrypted data with salt
- `password` (str): Decryption password

**Returns:** `bytes` - Decrypted original payload

**Raises:**
- `cryptography.fernet.InvalidToken`: If password incorrect
- `ValueError`: If encrypted data format invalid

#### Utility Functions

##### `zip_folder_to_bytes(folder_path)`
Compresses a folder to ZIP format in memory.

**Parameters:**
- `folder_path` (str): Path to folder to compress

**Returns:** `bytes` - ZIP archive data

**Features:**
- Preserves folder structure and file permissions
- Uses compression for efficiency
- Handles large directories gracefully

##### `load_payload(file_path)`
Loads payload from file or folder.

**Parameters:**
- `file_path` (str): Path to file or folder

**Returns:** `bytes` - Payload data (ZIP if folder, raw if file)

### GUI Classes (`src/gui_app.py`)

#### `StegoBoxGUI(ctk.CTk)`
Main GUI application class.

##### Key Methods

##### `__init__()`
Initializes the GUI application with modern styling.

##### `create_interface()`
Builds the complete user interface with sidebar and tabs.

##### `hide_data()`
Starts data hiding operation in background thread.

##### `extract_data()`
Starts data extraction operation in background thread.

##### `method_changed(value)`
Handles steganography method selection changes.

**Parameters:**
- `value` (str): Selected method ("append" or "lsb")

### Constants and Configuration

#### Magic Numbers
```python
APPEND_MAGIC = b"STEGOBX\x00APPEND\x00"  # Append method identifier
LSB_MAGIC = b"STEGOBX\x00LSB\x00"        # LSB method identifier
VERSION = 1                               # File format version
```

#### Cryptographic Parameters
```python
PBKDF2_ITERATIONS = 200000  # Key derivation iterations
SALT_SIZE = 16              # Salt size in bytes
KEY_SIZE = 32               # Encryption key size (AES-256)
```

---

## 🧪 Testing Framework

### Test Structure

#### Unit Tests
Located in `tests/` directory (create if doesn't exist):
```
tests/
├── test_steganography.py    # Core algorithm tests
├── test_crypto.py           # Encryption/decryption tests
├── test_gui.py              # GUI component tests
└── test_integration.py      # End-to-end tests
```

#### Test Categories

##### 1. Algorithm Tests
```python
import pytest
from src.example import append_embed, append_extract, lsb_embed, lsb_extract

def test_append_roundtrip():
    """Test append method embed/extract cycle"""
    payload = b"test data"
    append_embed('test_cover.png', payload, 'test_stego.png')
    recovered = append_extract('test_stego.png')
    assert recovered == payload

def test_lsb_capacity():
    """Test LSB capacity calculation"""
    capacity = lsb_capacity('test_image.png')
    assert capacity > 0
    assert isinstance(capacity, int)
```

##### 2. Cryptographic Tests
```python
def test_encryption_roundtrip():
    """Test encryption/decryption cycle"""
    original = b"sensitive data"
    password = "test_password"
    
    encrypted = encrypt_payload(original, password)
    decrypted = decrypt_payload(encrypted, password)
    
    assert decrypted == original
    assert encrypted != original

def test_wrong_password():
    """Test incorrect password handling"""
    encrypted = encrypt_payload(b"data", "correct")
    
    with pytest.raises(Exception):
        decrypt_payload(encrypted, "wrong")
```

#### Interactive Testing (`examples/demo.py`)

The demo script provides comprehensive testing:

##### 1. Basic Functionality Test
```python
def test_basic_functionality():
    """Test core embedding and extraction"""
    # Create test data
    test_data = create_test_files()
    
    # Test both methods
    for method in ['append', 'lsb']:
        print(f"Testing {method} method...")
        
        # Test embedding
        success = test_embedding(method, test_data)
        assert success, f"{method} embedding failed"
        
        # Test extraction
        recovered = test_extraction(method)
        assert recovered == test_data, f"{method} extraction failed"
```

##### 2. Performance Benchmarking
```python
def benchmark_performance():
    """Benchmark steganography performance"""
    import time
    
    test_sizes = [1024, 10240, 102400]  # 1KB, 10KB, 100KB
    
    for size in test_sizes:
        data = os.urandom(size)
        
        # Benchmark append method
        start = time.time()
        append_embed('test.png', data, 'stego_append.png')
        append_time = time.time() - start
        
        # Benchmark LSB method
        start = time.time()
        lsb_embed('test.png', data, 'stego_lsb.png')
        lsb_time = time.time() - start
        
        print(f"Size: {size} bytes")
        print(f"Append: {append_time:.3f}s")
        print(f"LSB: {lsb_time:.3f}s")
```

### Running Tests

#### Automated Testing
```bash
# Run all unit tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_steganography.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

#### Manual Testing
```bash
# Run interactive demo
cd examples
python demo.py

# Test specific functionality
python -c "from src.example import *; print(lsb_capacity('test.png'))"
```

#### Continuous Integration

Create `.github/workflows/test.yml`:
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest tests/ --cov=src
```

---

## 🔨 Building & Distribution

### Build Configuration

#### PyInstaller Specification (`build/StegoBox.spec`)
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../stegobox_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../src/example.py', 'src'),
        ('../src/gui_app.py', 'src'),
        ('../src/requirements.txt', 'src'),
        ('../assets/custom_icon.ico', 'assets'),
    ],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='StegoBox',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../assets/custom_icon.ico',
)
```

#### Automated Build Script (`build/build.py`)

The build script handles:
- Dependency verification
- PyInstaller configuration
- Icon and version info integration
- Cross-platform compatibility
- Error handling and cleanup

### Build Process

#### 1. Prepare Build Environment
```bash
# Navigate to build directory
cd build

# Verify all dependencies
python -c "import src.example, src.gui_app; print('Dependencies OK')"

# Clean previous builds
rm -rf dist/ build/ *.spec
```

#### 2. Execute Build
```bash
# Run automated build
python build.py

# Manual build (alternative)
pyinstaller --onefile --windowed --name StegoBox \
    --icon="../assets/custom_icon.ico" \
    --add-data="../src/example.py;src" \
    --add-data="../src/gui_app.py;src" \
    "../stegobox_gui.py"
```

#### 3. Test Executable
```bash
# Test basic functionality
./dist/StegoBox.exe

# Verify file integrity
file dist/StegoBox.exe
```

### Distribution

#### Release Packaging
```bash
# Create release directory
mkdir StegoBox-v1.0.0

# Copy executable and documentation
cp dist/StegoBox.exe StegoBox-v1.0.0/
cp README.md StegoBox-v1.0.0/
cp docs/USER_GUIDE.md StegoBox-v1.0.0/

# Create archive
zip -r StegoBox-v1.0.0.zip StegoBox-v1.0.0/
```

#### Code Signing (Optional)
```bash
# Windows code signing
signtool sign /f certificate.pfx /p password /t http://timestamp.verisign.com/scripts/timstamp.dll StegoBox.exe

# macOS code signing
codesign --force --verify --verbose --sign "Developer ID Application: Your Name" StegoBox.app
```

---

## 🤝 Contributing Guidelines

### Getting Started

#### 1. Fork and Clone
```bash
# Fork repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/StegoBox.git
cd StegoBox

# Add upstream remote
git remote add upstream https://github.com/Risterz/StegoBox.git
```

#### 2. Create Feature Branch
```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

#### 3. Development Process
- Write clean, documented code
- Follow existing code style and conventions
- Add tests for new functionality
- Update documentation as needed
- Test thoroughly before submitting

#### 4. Submit Pull Request
```bash
# Push feature branch
git push origin feature/your-feature-name

# Create pull request on GitHub
# Provide clear description of changes
# Reference any related issues
```

### Code Review Process

#### Review Criteria
- **Functionality**: Does the code work as intended?
- **Testing**: Are there adequate tests with good coverage?
- **Documentation**: Is the code well-documented?
- **Style**: Does it follow project conventions?
- **Security**: Are there any security implications?
- **Performance**: Is the code efficient?

#### Review Checklist
- [ ] Code compiles without warnings
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Follows coding standards
- [ ] Backwards compatibility maintained

### Issue Guidelines

#### Bug Reports
Include the following information:
- **Environment**: OS, Python version, StegoBox version
- **Steps to reproduce**: Clear, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Complete error output
- **Sample files**: If relevant and non-sensitive

#### Feature Requests
Provide this information:
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Other possible approaches
- **Implementation**: Technical considerations
- **Breaking changes**: Impact on existing functionality

---

## 🔍 Code Standards

### Python Style Guide

#### Follow PEP 8
- Line length: 88 characters (Black formatter default)
- Indentation: 4 spaces
- Imports: Grouped and sorted
- Naming: snake_case for functions/variables, PascalCase for classes

#### Docstring Format
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of function.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: When this exception is raised
    
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        Expected output
    """
    # Implementation here
    pass
```

#### Type Hints
```python
from typing import Optional, List, Dict, Union
import pathlib

def process_files(
    file_paths: List[pathlib.Path],
    output_dir: Optional[pathlib.Path] = None,
    options: Dict[str, Union[str, int]] = None
) -> bool:
    """Process multiple files with optional configuration."""
    pass
```

### Code Organization

#### File Structure
```python
#!/usr/bin/env python3
"""
Module docstring describing the file's purpose.
"""

# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
from PIL import Image
import customtkinter as ctk

# Local imports
from .utils import helper_function

# Constants
MAGIC_NUMBER = b"STEGOBX"
DEFAULT_ITERATIONS = 200000

# Classes and functions follow
```

#### Error Handling
```python
def robust_function(file_path: str) -> bytes:
    """Example of proper error handling."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except PermissionError:
        logger.error(f"Permission denied: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error reading {file_path}: {e}")
        raise
```

### Security Considerations

#### Input Validation
```python
def validate_image_path(path: str) -> pathlib.Path:
    """Validate and sanitize image file path."""
    path_obj = pathlib.Path(path).resolve()
    
    # Check if file exists
    if not path_obj.exists():
        raise FileNotFoundError(f"Image file not found: {path}")
    
    # Check file extension
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
    if path_obj.suffix.lower() not in allowed_extensions:
        raise ValueError(f"Unsupported image format: {path_obj.suffix}")
    
    # Check file size (prevent DoS)
    max_size = 100 * 1024 * 1024  # 100MB
    if path_obj.stat().st_size > max_size:
        raise ValueError(f"Image file too large: {path_obj.stat().st_size} bytes")
    
    return path_obj
```

#### Secure Memory Handling
```python
import secrets
from cryptography.hazmat.primitives import hashes

def secure_password_hash(password: str, salt: bytes = None) -> tuple:
    """Create secure password hash with salt."""
    if salt is None:
        salt = secrets.token_bytes(16)
    
    # Use PBKDF2 for password hashing
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
    )
    
    key = kdf.derive(password.encode('utf-8'))
    
    # Clear password from memory (Python limitation)
    password = None
    
    return key, salt
```

### Performance Guidelines

#### Memory Efficiency
```python
def process_large_file(file_path: str, chunk_size: int = 8192) -> None:
    """Process large files in chunks to manage memory."""
    with open(file_path, 'rb') as input_file:
        with open(f"{file_path}.processed", 'wb') as output_file:
            while True:
                chunk = input_file.read(chunk_size)
                if not chunk:
                    break
                
                processed_chunk = process_chunk(chunk)
                output_file.write(processed_chunk)
```

#### Algorithm Optimization
```python
def optimized_lsb_embed(image_array: np.ndarray, data: bytes) -> np.ndarray:
    """Optimized LSB embedding using NumPy operations."""
    # Flatten image for vectorized operations
    flat_image = image_array.flatten()
    
    # Convert data to binary
    binary_data = ''.join(format(byte, '08b') for byte in data)
    
    # Vectorized LSB modification
    for i, bit in enumerate(binary_data):
        if i >= len(flat_image):
            raise ValueError("Data too large for image")
        
        # Clear LSB and set new bit
        flat_image[i] = (flat_image[i] & 0xFE) | int(bit)
    
    # Reshape back to original dimensions
    return flat_image.reshape(image_array.shape)
```

---

## 🚀 Deployment

### Release Process

#### 1. Version Management
```bash
# Update version in relevant files
# - src/example.py (VERSION constant)
# - build/version_info.txt
# - README.md badges
# - setup.py

# Create version tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

#### 2. Build Release
```bash
# Clean environment
rm -rf build/dist/ build/build/

# Build executable
cd build
python build.py

# Test executable
./dist/StegoBox.exe --version
```

#### 3. Create Release Package
```bash
# Create release directory
mkdir releases/v1.0.0

# Copy files
cp build/dist/StegoBox.exe releases/v1.0.0/
cp README.md releases/v1.0.0/
cp docs/*.md releases/v1.0.0/docs/

# Create archives
cd releases
zip -r StegoBox-v1.0.0-Windows.zip v1.0.0/
tar -czf StegoBox-v1.0.0-Source.tar.gz ../src/ ../docs/ ../examples/
```

#### 4. GitHub Release
```bash
# Create release on GitHub with:
# - Release notes
# - Binary attachments
# - Source code archives
# - Checksums

# Generate checksums
sha256sum StegoBox-v1.0.0-Windows.zip > checksums.txt
```

### Continuous Integration

#### GitHub Actions Workflow
```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build executable
      run: |
        cd build
        python build.py
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: StegoBox-Windows
        path: build/dist/StegoBox.exe
    
    - name: Create Release
      if: startsWith(github.ref, 'refs/tags/')
      uses: softprops/action-gh-release@v1
      with:
        files: build/dist/StegoBox.exe
```

### Distribution Channels

#### 1. GitHub Releases
- Primary distribution method
- Includes source code and binaries
- Version tracking and release notes
- Community downloads and feedback

#### 2. Python Package Index (PyPI)
```bash
# Prepare package
python setup.py sdist bdist_wheel

# Upload to PyPI
twine upload dist/*

# Install via pip
pip install stegobox
```

#### 3. Alternative Channels
- **Chocolatey** (Windows package manager)
- **Homebrew** (macOS package manager)
- **Snap** (Linux universal packages)
- **Docker Hub** (containerized distribution)

### Security Considerations

#### Code Signing
- Windows: Authenticode signing for trust
- macOS: Developer ID for Gatekeeper compatibility
- Linux: GPG signatures for package integrity

#### Supply Chain Security
- Pin dependency versions
- Use virtual environments
- Scan dependencies for vulnerabilities
- Maintain security update process

#### Release Integrity
- Generate and publish checksums
- Sign release artifacts
- Use secure distribution channels
- Monitor for unauthorized modifications

---

## 📞 Developer Support

### Getting Help

#### Internal Resources
- **Code comments**: Inline documentation for complex logic
- **Docstrings**: Function and class documentation
- **Type hints**: Parameter and return type information
- **Examples**: Practical usage demonstrations

#### External Resources
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Community questions and ideas
- **Documentation**: Comprehensive guides and references
- **Code Reviews**: Peer feedback and improvements

### Contributing to Documentation

#### Documentation Standards
- **Clear language**: Write for diverse audiences
- **Practical examples**: Include working code samples
- **Current information**: Keep documentation updated
- **Cross-references**: Link related sections

#### Documentation Tools
- **Markdown**: Primary documentation format
- **Sphinx**: API documentation generation
- **MkDocs**: Website documentation hosting
- **Diagrams**: Architecture and flow illustrations

---

*This developer guide is continuously updated. Check the [latest version](../../docs/DEVELOPER_GUIDE.md) for current information.*