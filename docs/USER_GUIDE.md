# 📖 StegoBox User Guide

**Complete step-by-step instructions for using StegoBox**

---

## 📑 Table of Contents

1. [🚀 Getting Started](#-getting-started)
2. [🖥️ GUI Interface Guide](#️-gui-interface-guide)
3. [⌨️ Command Line Interface](#️-command-line-interface)
4. [🔐 Hiding Data (Embedding)](#-hiding-data-embedding)
5. [🔓 Extracting Data](#-extracting-data)
6. [🛡️ Security Best Practices](#️-security-best-practices)
7. [📊 Method Comparison](#-method-comparison)
8. [🔧 Troubleshooting](#-troubleshooting)
9. [💡 Tips & Tricks](#-tips--tricks)

---

## 🚀 Getting Started

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher (if running from source)
- **RAM**: Minimum 2GB (4GB recommended for large files)
- **Storage**: 50MB free space minimum

### Installation Options

#### Option A: Standalone Executable (Recommended)
1. Download `StegoBox.exe` from the [Releases page](../../releases)
2. No installation required - just double-click to run
3. Windows may show a security warning - click "More info" → "Run anyway"

#### Option B: Python Source
```bash
# Clone the repository
git clone https://github.com/Risterz/StegoBox.git
cd StegoBox

# Install dependencies
pip install -r requirements.txt

# Launch GUI
python stegobox_gui.py
```

#### Option C: Development Setup
```bash
# Install additional dev dependencies
pip install pyinstaller

# Run interactive demo
cd examples
python demo.py

# Build your own executable
cd build
python build.py
```

---

## 🖥️ GUI Interface Guide

### Main Window Layout

The StegoBox GUI features a modern, intuitive design with the following components:

#### Left Sidebar
- **🎨 Theme Selector**: Switch between Dark, Light, and System themes
- **⚙️ Method Selection**: Choose between Append and LSB steganography
- **ℹ️ Method Information**: Real-time guidance for selected method

#### Main Content Area
- **📂 Hide Data Tab**: For embedding files/folders into images
- **📤 Extract Data Tab**: For recovering hidden data from images
- **📊 Progress Indicators**: Real-time operation feedback
- **📱 Status Bar**: Current operation status and helpful messages

### Navigation Tips
- **Tab Switching**: Click between "Hide Data" and "Extract Data" tabs
- **File Selection**: Use "Browse" buttons or drag-and-drop (where supported)
- **Method Switching**: Change methods anytime via the sidebar
- **Theme Changes**: Apply instantly without restart

---

## ⌨️ Command Line Interface

### Basic Syntax
```bash
cd src
python example.py [command] [options]
```

### Available Commands

#### Hide Data
```bash
# Hide a folder in an image
python example.py hide cover.png secret_folder/ output.png

# Hide a ZIP file with LSB method
python example.py hide --method lsb cover.png data.zip output.png

# Hide with password encryption
python example.py hide --method lsb --encrypt cover.png data.zip output.png
```

#### Extract Data
```bash
# Extract hidden data
python example.py extract stego.png recovered.zip

# Extract with password
python example.py extract --password stego.png recovered.zip

# Force specific extraction method
python example.py extract --method append stego.png recovered.zip
```

#### Utility Commands
```bash
# Check LSB capacity of an image
python example.py capacity image.png

# Get help for specific command
python example.py hide --help
```

### Environment Variables
```bash
# Set default password (not recommended for security)
export STEGOBOX_PASSWORD="your_password"

# Enable debug output
export STEGOBOX_DEBUG=1
```

---

## 🔐 Hiding Data (Embedding)

### Step-by-Step Process

#### 1. Select Method
**Append Mode**:
- ✅ Fastest processing
- ✅ Unlimited capacity
- ❌ Easily detectable
- ❌ Increases file size significantly

**LSB Mode**:
- ✅ Invisible to casual inspection
- ✅ No file size change
- ✅ Supports encryption
- ❌ Limited capacity
- ❌ Requires lossless formats

#### 2. Choose Cover Image

**For LSB Mode** (Recommended formats):
- **PNG**: Best choice - lossless, widely supported
- **BMP**: Excellent - uncompressed, maximum capacity
- **TIFF**: Good - lossless with compression options
- ❌ **JPEG**: Not recommended - lossy compression destroys hidden data

**For Append Mode** (Any format):
- **PNG, JPEG, BMP, GIF, TIFF**: All supported
- File format doesn't affect hiding capability

#### 3. Select Data to Hide

**Folder Selection**:
- Choose any folder - it will be automatically compressed to ZIP
- Supports nested folders and all file types
- Maintains original folder structure and permissions

**ZIP File Selection**:
- Must be a valid ZIP archive
- Can contain any files and folder structures
- Pre-compressed files save processing time

#### 4. Configure Security (LSB Only)

**Password Protection**:
- ✅ Check "Encrypt with password" for maximum security
- Enter a strong password (minimum 8 characters recommended)
- Uses AES-256 encryption with PBKDF2 key derivation
- **⚠️ Warning**: Lost passwords cannot be recovered!

**Password Best Practices**:
- Use a combination of letters, numbers, and symbols
- Avoid dictionary words or personal information
- Consider using a password manager
- Test password entry before final embedding

#### 5. Choose Output Location
- Select destination for the stego image
- Use `.png` extension for maximum compatibility
- Avoid overwriting the original cover image
- Choose a location with sufficient disk space

#### 6. Execute Embedding
- Click "🔒 Hide Data" to start the process
- Monitor progress bar for operation status
- Wait for completion confirmation
- Verify the output file was created successfully

### Capacity Planning

#### LSB Capacity Calculator
```
Capacity (bytes) = (Width × Height × 3) ÷ 8 - Header_Size
```

#### Common Image Capacities
| Resolution | Dimensions | Capacity | Typical Use |
|------------|------------|----------|-------------|
| HD Ready | 1280×720 | ~345 KB | Documents, small archives |
| Full HD | 1920×1080 | ~780 KB | Photo collections, medium files |
| 4K UHD | 3840×2160 | ~3.1 MB | Large documents, small videos |
| 5K | 5120×2880 | ~5.5 MB | Extensive archives, datasets |

#### Optimization Tips
- **Compress before hiding**: ZIP with maximum compression
- **Use efficient formats**: Avoid redundant files
- **Split large data**: Use multiple cover images if needed
- **Choose appropriate resolution**: Match capacity to data size

---

## 🔓 Extracting Data

### Extraction Process

#### 1. Select Stego Image
- Choose the image containing hidden data
- Both original formats and converted images work
- Ensure the image hasn't been re-compressed (for LSB)

#### 2. Determine Method
**Automatic Detection** (Default):
- StegoBox automatically detects the embedding method
- Tries both Append and LSB methods
- Shows which method was successful

**Manual Method Selection**:
- Use CLI `--method` flag if auto-detection fails
- Helpful when you know the specific method used

#### 3. Enter Password (If Required)
- Only needed if data was encrypted during embedding
- Enter the exact password used for embedding
- Leave blank if data wasn't encrypted
- **Case-sensitive**: Ensure correct capitalization

#### 4. Choose Output Location
- Select where to save the extracted ZIP file
- Use `.zip` extension for compatibility
- Ensure sufficient disk space for extracted data

#### 5. Execute Extraction
- Click "🔓 Extract Data" to begin
- Monitor progress and status messages
- Verify extraction completion
- Check the extracted ZIP file integrity

### Post-Extraction

#### Verify Extracted Data
```bash
# Check ZIP file integrity
unzip -t extracted_data.zip

# Extract and verify contents
unzip extracted_data.zip -d extracted_folder/
```

#### Common Extraction Scenarios

**Successful Extraction**:
- Progress completes to 100%
- Status shows "Data extracted successfully!"
- Valid ZIP file created at output location

**Password Required**:
- Error: "Password required to decrypt"
- Solution: Enter the correct password and retry

**No Data Found**:
- Error: "No hidden data found"
- Possible causes: Wrong image, corrupted data, modified image

**Corrupted Data**:
- Extraction completes but ZIP is invalid
- Possible causes: Image was re-compressed, partial corruption

---

## 🛡️ Security Best Practices

### Embedding Security

#### Password Management
- **Use unique passwords** for each embedding operation
- **Store passwords securely** using a password manager
- **Never reuse** passwords across different hidden datasets
- **Consider passphrases** for better security and memorability

#### Cover Image Selection
- **Use original, unprocessed images** when possible
- **Avoid images with existing metadata** that might conflict
- **Choose high-quality source images** to maximize capacity
- **Don't use copyrighted images** for distribution

#### Data Preparation
- **Compress sensitive data** before embedding for efficiency
- **Remove metadata** from files before archiving
- **Organize folder structures** for easy extraction
- **Test archive integrity** before embedding

### Distribution Security

#### Safe Sharing Practices
- **Use secure channels** for sharing stego images
- **Don't announce** that images contain hidden data
- **Consider additional encryption** for extra security layers
- **Verify recipient identity** before sharing encrypted content

#### Operational Security (OpSec)
- **Use different cover images** for different recipients
- **Vary embedding methods** to avoid pattern detection
- **Clean metadata** from stego images before sharing
- **Monitor for unauthorized access** to your stego images

### Detection Avoidance

#### LSB Mode Best Practices
- **Use PNG or BMP formats** exclusively
- **Avoid post-processing** stego images
- **Don't resize or compress** after embedding
- **Keep file sizes reasonable** relative to image resolution

#### Append Mode Considerations
- **Accept higher detection risk** for convenience
- **Use for non-sensitive applications** only
- **Consider file size increases** when sharing
- **Don't use for covert communications**

---

## 📊 Method Comparison

### Detailed Feature Comparison

| Feature | Append Mode | LSB Mode |
|---------|-------------|----------|
| **Hiding Speed** | Very Fast | Moderate |
| **Extraction Speed** | Very Fast | Moderate |
| **Data Capacity** | Unlimited | Limited by image size |
| **File Size Change** | Significant increase | No change |
| **Detection Difficulty** | Easy to detect | Very difficult |
| **Format Requirements** | Any image format | PNG, BMP, TIFF only |
| **Encryption Support** | No | Yes (AES-256) |
| **Lossy Compression** | Survives | Destroys hidden data |
| **Visual Changes** | None | Minimal/invisible |
| **Forensic Resistance** | Very low | High |

### When to Use Each Method

#### Choose Append Mode When:
- **Speed is priority** over stealth
- **Data size exceeds** LSB capacity
- **Convenience matters** more than security
- **Detection isn't a concern**
- **Using various image formats**

#### Choose LSB Mode When:
- **Stealth is critical** for your use case
- **Data fits within** image capacity
- **You need encryption** for sensitive data
- **Recipients might inspect** file properties
- **Using PNG/BMP images** exclusively

### Performance Benchmarks

#### Processing Times (Approximate)
| Operation | Append Mode | LSB Mode |
|-----------|-------------|----------|
| 1MB data → 1920×1080 PNG | 0.5 seconds | 2-3 seconds |
| 5MB data → 4K PNG | 1.5 seconds | 8-12 seconds |
| 100MB data → Any image | 3-5 seconds | Not possible |

#### Memory Usage
- **Append Mode**: Minimal memory overhead
- **LSB Mode**: Requires loading full image into memory
- **Encryption**: Additional 10-20% memory for crypto operations

---

## 🔧 Troubleshooting

### Common Error Messages

#### "Payload too large for this image"
**Cause**: Data exceeds LSB capacity of the selected image
**Solutions**:
1. Use a larger, higher-resolution image
2. Compress your data more aggressively
3. Switch to Append mode for unlimited capacity
4. Split data across multiple images

#### "Password required to decrypt"  
**Cause**: Data was encrypted but no password provided
**Solutions**:
1. Enter the correct password used during embedding
2. Verify password spelling and case sensitivity
3. Try extracting without password (data might not be encrypted)

#### "No hidden data found"
**Cause**: Image doesn't contain hidden data or data is corrupted
**Solutions**:
1. Verify you're using the correct stego image
2. Check if image was modified after embedding
3. Try both extraction methods manually
4. Ensure image format is compatible

#### "Permission denied" or "File in use"
**Cause**: Operating system restrictions or file locks
**Solutions**:
1. Run StegoBox as administrator (Windows)
2. Close other programs using the target files
3. Check file permissions and ownership
4. Ensure sufficient disk space

#### GUI doesn't start
**Cause**: Missing dependencies or Python environment issues
**Solutions**:
1. Install all requirements: `pip install -r requirements.txt`
2. Update Python to version 3.8 or higher
3. Try running from command line to see error messages
4. Use the standalone executable instead

### Platform-Specific Issues

#### Windows
- **Antivirus software** may flag the executable as suspicious
- **Windows Defender** might quarantine the file
- **Solution**: Add StegoBox to antivirus exceptions

#### macOS
- **Gatekeeper** may prevent execution of unsigned apps
- **Solution**: Right-click → "Open" → "Open anyway"
- **Alternative**: Run from Terminal to bypass Gatekeeper

#### Linux
- **File permissions** might prevent execution
- **Solution**: `chmod +x StegoBox` for executable files
- **Dependencies**: Install system packages for GUI support

### Performance Issues

#### Slow Processing
**Causes and Solutions**:
- **Large images**: Use smaller images or more powerful hardware
- **Low memory**: Close other applications to free RAM
- **Old hardware**: Consider using Append mode for speed
- **Network drives**: Process files locally when possible

#### Memory Errors
**Solutions**:
- **Reduce image size** or data payload
- **Close unnecessary applications**
- **Use 64-bit Python** for larger memory access
- **Process files in smaller batches**

---

## 💡 Tips & Tricks

### Efficiency Tips

#### Optimize Your Workflow
1. **Batch Operations**: Process multiple files in sequence
2. **Keyboard Shortcuts**: Learn CLI commands for frequent tasks
3. **Template Images**: Keep high-quality cover images ready
4. **Organized Folders**: Maintain clear directory structures

#### Data Preparation
- **Pre-compress archives** with 7-Zip or WinRAR for better compression
- **Remove unnecessary files** before archiving
- **Use meaningful filenames** for easy identification
- **Test archives** before embedding to ensure integrity

### Advanced Techniques

#### Multiple Layer Hiding
1. Hide data in image using LSB mode
2. Hide the stego image in another image using Append mode
3. Creates double-layer protection with different detection profiles

#### Steganographic Chains
- Hide small data in multiple images
- Reference each part in a master index
- Provides redundancy and distributed hiding

#### Custom Workflows
```bash
# Automated batch processing script
for image in *.png; do
    python example.py hide "$image" "data/" "stego_$image"
done
```

### Security Enhancements

#### Additional Encryption Layers
- Encrypt files **before** creating ZIP archive
- Use tools like 7-Zip with AES encryption
- Provides defense-in-depth security model

#### Metadata Removal
```bash
# Remove EXIF data from images (Linux/macOS)
exiftool -all= cover_image.png

# Windows alternative
# Use tools like ExifPurge or GIMP
```

#### Secure Deletion
- **Overwrite original files** securely after embedding
- Use tools like `sdelete` (Windows) or `shred` (Linux)
- **Clear clipboard** and temporary files
- **Empty recycle bin/trash** thoroughly

### Testing and Validation

#### Verify Hidden Data Integrity
```bash
# Test embedding and extraction cycle
python example.py hide test.png data/ stego.png
python example.py extract stego.png recovered.zip
diff -r data/ extracted_data/
```

#### Capacity Testing
```bash
# Find maximum capacity for an image
python example.py capacity image.png

# Test with various data sizes
python example.py hide image.png small_data/ test1.png
python example.py hide image.png large_data/ test2.png
```

#### Security Testing
- **Password strength**: Test with various password complexities
- **Format compatibility**: Verify extraction after format conversion
- **Corruption resistance**: Test with slightly modified stego images

### Professional Usage

#### Documentation
- **Keep detailed records** of embedding operations
- **Document password policies** and recovery procedures
- **Maintain inventory** of stego images and their contents
- **Create standard procedures** for your organization

#### Compliance Considerations
- **Understand legal requirements** in your jurisdiction
- **Follow organizational policies** for data handling
- **Implement audit trails** for sensitive operations
- **Train users** on proper steganography practices

---

## 📞 Need Help?

### Support Channels
- 📚 **Documentation**: Check all guides in the `docs/` folder
- 💬 **Community**: Join discussions at [GitHub Discussions](../../discussions)
- 🐛 **Bug Reports**: Submit issues at [GitHub Issues](../../issues)
- 📧 **Contact**: Reach out to [@Risterz](https://github.com/Risterz)

### Before Seeking Help
1. **Read error messages** carefully and completely
2. **Check this guide** for your specific issue
3. **Try the interactive demo** to verify basic functionality
4. **Test with sample data** to isolate the problem
5. **Note your environment** (OS, Python version, etc.)

### When Reporting Issues
Include the following information:
- **Operating System** and version
- **Python version** (if running from source)
- **StegoBox version** or commit hash
- **Complete error message** and stack trace
- **Steps to reproduce** the issue
- **Sample files** (if not sensitive)

---

*This guide is continuously updated. Check the [latest version](../../docs/USER_GUIDE.md) for the most current information.*