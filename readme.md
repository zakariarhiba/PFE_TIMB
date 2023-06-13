# **Development of an IoT Application for Remote Medical Monitoring**

<img src="./QtApp/assets/images/welcome.png"
     alt="Markdown Monster icon"
     style="float: start; margin-left: 1em; width:100%;" />

> Realized by : RHIBA Zakaria et TAKILI Youssef

> Pr MUSTAPHA El HANINE

## Abstract : 

As part of this final year project, we have developed an innovative desktop application using PyQt5
in Python. This application provides the ability to remotely monitor and study patients parameters
progress in a more general context, beyond just the intensive care unit.
We have also designed a small monitor using the ESP8266 microcontroller, capable of measuring es-
sential data such as oxygen saturation (SpO2), temperature, and heart rate. This monitor transmits
this data via the MQTT protocol to the desktop application.
The application offers a user-friendly and intuitive interface, allowing healthcare professionals to view
real-time patient data and monitor their progress accurately. Additionally, predefined thresholds are
set for each monitored parameter. If these thresholds are reached, automatic email alerts are sent to
the responsible doctor, informing them of the critical condition of the patient.
The goal of this solution is to assist healthcare professionals in making informed and precise decisions
by providing real-time data, even when they are not physically present with the patient. It facilitates
remote monitoring and contributes to proactive patient care.
With our developed desktop application and small monitor, we aim to enhance the quality of medical
care by providing an efficient and convenient solution for remote patient monitoring

## Documentation : 

The Code is divided in 3 parties, first one is [Desktop Application code](/./QtApp/main.py), then secondly the hardware application code which is also have two subfolders one for the  [Arduino Uno Code](./hardware_code/carte_graphique_uno/carte_graphique_uno.ino) in side the other one for [Esp8266 Code](./hardware_code/esp_code/esp_code.ino), the final part is used for the serial communication between the [esp to arduino code](./hardware_code/Serial_Communication/).

The application can easily run in windows without any installation of librarys or any program at all, all what you need is to download [Healthcare Connect Application](https://drive.google.com/drive/folders/1nnBlWNXi7suOYNn0KuVTA4CRGyBPYQkj?usp=sharing) and then execute the application from **"Healthcare connect.exe"**.

> Before Execute the application make sure that your PC is connected to the Internet.

> There is only one user account for the moment  : 

> Username : Admin  &  Password : 123

