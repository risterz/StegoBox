# 🎨 StegoBox Assets

This directory contains all visual assets, icons, and branding materials for StegoBox.

## Directory Structure

```
assets/
├── custom_icon.ico         # Windows application icon
├── custom_icon.png         # High-resolution PNG icon
├── screenshots/            # Application screenshots
│   ├── gui/               # GUI interface examples
│   ├── demo/              # Demo and workflow images
│   └── README.md          # Screenshot guidelines
└── README.md              # This file
```

## Asset Files

### Icons

| File | Purpose | Format | Size |
|------|---------|--------|------|
| `custom_icon.ico` | Windows executable icon | ICO | Multi-size (16px-256px) |
| `custom_icon.png` | High-resolution icon | PNG | 512×512 or higher |

### Icon Usage

The icons are used in:
- **Windows executable** (`StegoBox.exe`)
- **Build configuration** (`build/StegoBox.spec`)
- **Documentation** (README headers and guides)
- **GitHub repository** (social preview and branding)

### Design Guidelines

#### Icon Design Principles
- **Spy/Detective theme** - Represents steganography
- **Magnifying glass motif** - Symbolizes hidden data discovery
- **Modern aesthetic** - Clean, professional appearance
- **High contrast** - Visible in various contexts
- **Scalable design** - Works at all sizes (16px to 512px)

#### Color Palette
- **Primary**: Deep blue (#3B82F6)
- **Background**: Dark gray (#2D3748)
- **Accent**: Light blue (#93C5FD)
- **Text**: White (#FFFFFF)

## File Generation

### Creating Icons

Icons can be generated using the provided utilities:

```bash
# Generate basic icon programmatically
cd examples
python create_icon.py

# Convert custom artwork to ICO format
python convert_custom_icon.py
```

### Icon Requirements

For Windows executables:
- **ICO format** with multiple sizes embedded
- **Sizes**: 16×16, 32×32, 48×48, 64×64, 128×128, 256×256
- **Color depth**: 32-bit with alpha transparency
- **File size**: Under 1MB for optimal loading

## Screenshot Standards

See [`screenshots/README.md`](screenshots/README.md) for detailed guidelines.

### Categories
- **GUI Interface** - Application windows and dialogs
- **Workflow Examples** - Step-by-step processes
- **Feature Demonstrations** - Core functionality in action
- **Theme Variations** - Dark and light mode examples

## Asset Optimization

### File Size Guidelines
- **Icons**: Under 100KB each
- **Screenshots**: Under 500KB each
- **Total directory**: Under 5MB

### Optimization Tools
- **PNG**: Use tools like TinyPNG or ImageOptim
- **ICO**: Optimize individual sizes before combining
- **Compression**: Balance quality vs. file size

## Usage Rights

### Original Assets
All original StegoBox assets are:
- **Created by**: [@Risterz](https://github.com/Risterz)
- **License**: MIT (same as project)
- **Usage**: Free for any purpose with attribution

### Third-Party Assets
If using external assets:
- Ensure proper licensing
- Include attribution in this README
- Respect copyright and usage terms

## Contributing Assets

### Adding New Assets
1. **Create/source** the asset following guidelines
2. **Optimize** file size while maintaining quality
3. **Place** in appropriate subdirectory
4. **Update** this README with details
5. **Reference** in relevant documentation

### Asset Review Process
- Assets should be professional and brand-appropriate
- File sizes should be optimized
- Naming should follow project conventions
- Quality should meet project standards

## Branding Guidelines

### Logo Usage
- Use official icons for professional contexts
- Maintain aspect ratio when resizing
- Don't modify colors without approval
- Include proper attribution when required

### Visual Identity
- Consistent color scheme across materials
- Professional, technical aesthetic
- Spy/security theme elements
- Modern, approachable design

---

*For the complete StegoBox project, visit the [main repository](../README.md)*