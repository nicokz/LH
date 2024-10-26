# **LH**

## **Raspberry Pi RP2040 Watch**

This is an experimental MicroPython codebase for the Raspberry Pi RP2040, specifically designed for hardware featuring the GC9A01 display and the QMIC88658 module.

![Full color TFT screen](https://github.com/nicokz/LH/blob/master/docs/img/rp2040-w-color_bg.jpg)

## **Introduction**

The **Raspberry Pi RP2040 Watch** is a DIY smartwatch project aimed at exploring the capabilities of the RP2040 microcontroller. Leveraging the power of MicroPython, this project integrates a vibrant full-color TFT display with customizable features.

In this project, you'll find experimental code that showcases various functionalities such as screen rotation, custom pixel manipulation, and opacity effects that enhance visual aesthetics. This is an ideal starting point for anyone looking to develop their own wearable tech or learn more about MicroPython on the RP2040 platform.

## **Installation**

[TBD]

## **Usage**

[TBD]

### ***New Functions***

Using opacity effects on full-color screens can add a visually striking element, but implementing this with MicroPython's FrameBuffer and RGB565 format presents challenges.

The default `pixel()` function in FrameBuffer often leads to inconsistent color representation, prompting the creation of custom functions—`setPixel()` and `getPixel()`—to ensure accurate color handling. Additionally, a universal `color()` function has been introduced to interpret 16-bit RGB565 color formats effectively. This setup also incorporates opacity functions that enable smooth blending effects on the screen, elevating the visual experience of your smartwatch.

## **Contributing**

[TBD]

## **License**

The Raspberry Pi RP2040 Watch code is released under the MIT License. See the **[LICENSE](https://www.blackbox.ai/share/LICENSE)** file for details.

## **Authors and Acknowledgments**

This project was created by **Nicholas Schreiner** ([nicokz](https://github.com/nicokz)).

Additional contributors include:

N/A

## **Code of Conduct**

[TBD]

## **FAQ**

[TBD]

## **Changelog**

- **0.1.0:** Initial release with screen rotation example.

## **Contact**

If you have any questions or comments about the Raspberry Pi RP2040 Watch, please reach out to **nico** at **service@lighthunter.ws**.
