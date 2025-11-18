# Certificate Generator Pro

![Certificate Generator Pro](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.7%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B)

A modern, user-friendly web application for generating professional certificates in bulk. Built with Streamlit and Python, this tool allows you to easily create and customize certificates with names from an Excel or CSV file.

## ✨ Features

- 🖼️ Upload custom certificate templates (PNG, JPG, JPEG)
- 📊 Import recipient data from Excel or CSV files
- 🔄 Multiple name formatting options:
  - Single column
  - Combine two columns with custom separators
  - Combine three columns with custom separators
- 🎨 Customizable text positioning and styling
- 💾 Download all generated certificates as a ZIP file
- 🎯 Real-time preview of the certificate
- 🌓 Dark mode interface

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GauravKesh/certificate-generator.git
   cd certificate-generator-pro
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. In the sidebar:
   - Upload your certificate template image
   - Upload your Excel/CSV file with recipient data
   - Configure name formatting and positioning

4. Preview and download your certificates

## 🛠️ Dependencies

- Streamlit - Web application framework
- Pillow (PIL Fork) - Image processing
- Pandas - Data manipulation
- OpenPyXL - Excel file support

## 📂 Project Structure

```
certificate-generator/
├── app.py               # Main application code
├── requirements.txt     # Python dependencies
└── fonts/              # Font files for certificate text
    ├── Roboto-Italic-VariableFont_wdth,wght.ttf
    └── Roboto-Regular.ttf
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

For any questions or feedback, please open an issue on the GitHub repository.

---


  Made with ❤️ using Streamlit and Python

