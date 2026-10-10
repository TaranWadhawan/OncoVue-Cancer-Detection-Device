### `prerequisite.md`

````markdown
# OncoVue Diagnostic System Installation Guide

This guide details the complete system environment setup, driver configurations, local mail server setup, and desktop autostart configuration for the OncoVue Diagnostic System on a Raspberry Pi 5 running Raspberry Pi OS (Debian Bookworm, 64-bit).

---

## 1. Operating System & Base Dependencies

Ensure your Raspberry Pi 5 is running the official 64-bit Raspberry Pi OS with Desktop. Open a terminal and update your base system libraries:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install build-essential cmake pkg-config -y
```
````

---

## 2. Python Environment & Pip Installation

Debian Bookworm enforces PEP 668, which blocks global `pip` installations. Since you are using a dedicated system Python 3.13 installation (`/usr/bin/python3.13`), use the `--break-system-packages` flag to install the required libraries globally for that specific version:

```bash
/usr/bin/python3.13 -m pip install --upgrade pip --break-system-packages
/usr/bin/python3.13 -m pip install --break-system-packages -r requirements.txt
```

---

## 3. Raspberry Pi 5 HQ Camera & GStreamer Pipeline Setup

The Raspberry Pi 5 uses the new `libcamera` and PiSP pipeline architecture. For OpenCV to access your IMX477 HQ Camera module hardware-accelerated outside of VS Code (on startup and standard terminals), you must install the native GStreamer plug-ins:

```bash
sudo apt install libcamera-apps -y
sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-tools -y
```

### Grant Hardware Permissions

Add your logged-in user to the system `video` group so the script can access `/dev/video0` and `/dev/media0` directly:

```bash
sudo usermod -aG video oncovue
```

---

## 4. Arduino Serial Controller Setup

To allow Python to communicate with the dual-servo Arduino hardware controller over USB without needing root privileges:

1. Add your user to the `dialout` group:
   ```bash
   sudo usermod -aG dialout oncovue
   ```
2. Reboot your Raspberry Pi for group permissions to take effect.

---

## 5. Local Postfix Mail Relay (Offline/Early Boot Queueing)

To prevent the application from hanging or throwing connection errors during startup when Wi-Fi is still connecting, configure a local Postfix mail relay on port 25. Python will hand off the email locally, and Postfix will automatically deliver it to Gmail as soon as the internet connects.

### Step A: Install Postfix and SASL Authentication

```bash
sudo apt install postfix mailutils libsasl2-modules ca-certificates -y
```

_(Select **Internet Site** when prompted during installation)._

### Step B: Append Gmail Configuration to Postfix

Open the main Postfix configuration file:

```bash
sudo nano /etc/postfix/main.cf
```

Append the following lines to the bottom of the file:

```ini
relayhost = [smtp.gmail.com]:587
smtp_use_tls = yes
smtp_sasl_auth_enable = yes
smtp_sasl_security_options = noanonymous
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
```

### Step C: Configure Gmail App Password

Create the password file:

```bash
sudo nano /etc/postfix/api_passwd
```

Paste the following line (replace with your actual Gmail and 16-character App Password):

```text
[smtp.gmail.com]:587 oncovuevision@gmail.com:hfix fxjp nvhh diwe
```

Build the lookup database, secure the file, and restart the service:

```bash
sudo chmod 600 /etc/postfix/sasl_passwd
sudo postmap /etc/postfix/sasl_passwd
sudo systemctl restart postfix
```

---

## 6. XDG Autostart Kiosk Setup

To launch the system automatically when the Raspberry Pi 5 boots:

1. Create the autostart folder:
   ```bash
   mkdir -p /home/oncovue/.config/autostart
   ```
2. Create your desktop launcher entry:
   ```bash
   nano /home/oncovue/.config/autostart/oncovue.desktop
   ```
3. Paste the following configuration:
   ```ini
   [Desktop Entry]
   Type=Application
   Name=OncoVue Application
   Exec=/bin/bash /home/oncovue/Downloads/Final_application/launcher.sh
   Terminal=false
   NoDisplay=false
   X-GNOME-Autostart-enabled=true
   ```
4. Verify your `launcher.sh` script is marked as executable:
   ```bash
   chmod +x /home/oncovue/Downloads/Final_application/launcher.sh
   ```

````

---

### `requirements.txt`

```text
PyQt6==6.6.1
opencv-python==4.9.0.80
openpyxl==3.1.2
moviepy==1.0.3
pygame==2.5.2
pypdf==4.0.1
reportlab==4.1.0
google-api-python-client==2.118.0
google-auth-httplib2==0.2.0
google-auth-oauthlib==1.2.0
pillow==10.2.0
numpy==1.26.4
psutil==5.9.8
pyserial==3.5
tflite-runtime==2.14.0
````
