# AI Food Allergen Checker

A simple AI-powered app to scan food labels, detect allergens, and suggest safe alternatives.


## 🚀 Overview
The **AI Food Allergen Checker** is an IoT-based solution designed to predict and prevent chain failures in mechanical systems.  
It measures **current**, **RPM**, and **friction** using various sensors and indicates the chain’s condition through a connected smart device.

---

## ⚙️ Features
- Real-time monitoring of chain health  
- Measures current, RPM, and vibration parameters  
- Predictive maintenance alerts  
- IoT dashboard visualization  
- Hardware prototype with Arduino  

---

## 🧩 Tech Stack
| Layer | Components |
|-------|-------------|
| **Sensors** | ACS712 (Current), IR Sensor (RPM), LM35 (Temperature), Vibration Sensor |
| **Controller** | Arduino UNO / ESP32 |
| **Connectivity** | Wi-Fi (ESP8266) / Bluetooth (HC-05) |
| **Cloud & Visualization** | Blynk / ThingSpeak Dashboard |
| **Languages** | C / Embedded C |

---

## 📊 Workflow
1. Understanding parameters affecting the chain  
2. Measuring real-time parameters  
3. Processing data in microcontroller  
4. Displaying condition on IoT dashboard  

---

## 📸 Preview
![Tech Stack](Images/tech_stack.png)
![Dashboard](Images/output_dashboard.jpg)

---

## 👩‍💻 Author
**Nainam Hodiwala**  
🎓 3rd Year, Computer Engineering  
📍 GH Patel College of Engineering & Technology  
🔗 [LinkedIn](https://linkedin.com/in/nainamhodiwala)

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).


## 🚀 Quick Start

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

streamlit run src/app.py
