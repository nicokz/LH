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

### ***Architecture and Programming Strategy***

**"while True"** vs **Threading** buttons control

1. **CPU** Usage

**while True loop**: This version constantly polls the button states and performs simple calculations within each loop. Although it’s straightforward, the constant polling can be CPU-intensive since it doesn’t release control back to the main program unless specifically told to (via time.sleep()).
- CPU Load: Higher because the CPU spends more time actively in the button-monitoring loop.
- Latency: Button checks are very fast and have minimal latency.
- Efficiency: Good for time-sensitive applications that prioritize real-time button monitoring over multitasking.
**uasyncio version**: With uasyncio, we achieve cooperative multitasking by yielding control with await asyncio.sleep(). This lets other tasks run while the button state check “waits” briefly.
- CPU Load: Lower because it doesn’t block the CPU continuously in a loop. Other tasks can be performed during await periods, reducing the need for continuous polling.
- Latency: Slightly higher than the while True loop, since it depends on the await asyncio.sleep() delay. However, this is often negligible unless the delay is long.
- Efficiency: Better for multitasking, especially when there are other tasks that need to run alongside button monitoring.

2. **Memory** Usage

**while True loop**: This version uses minimal memory because it only needs a few variables and no additional overhead for task management.
- Memory Footprint: Minimal, as it relies on direct calls and simple control flow.
- Scalability: Can become harder to manage as additional features are added since each new feature would be managed within the same while True loop, which could get messy.
**uasyncio version**: The use of uasyncio introduces some additional memory overhead, particularly for the coroutine management and the event loop.
- Memory Footprint: Higher than while True due to the extra structures created by uasyncio, such as task management and stack frames for each async function.
- Scalability: Much better, as you can add more asyncio tasks to perform other background tasks without overcomplicating the main loop.

3. Summary and Recommendation for RP2040

If Real-Time Responsiveness Is Critical (e.g., quick reaction to button inputs with low latency), the while True loop version is simpler, uses less memory, and has minimal latency.
If Multitasking and Code Readability Are Important (e.g., if you need to add other tasks like display updates, sensor monitoring, etc.), then the uasyncio version is better despite a bit more memory use and slightly higher latency.
Typical Usage on RP2040
For projects that are more button-driven and don’t require multitasking, go with the while True version for simplicity and performance. If you want your button monitoring to coexist smoothly with other concurrent tasks, then the uasyncio version is worth the tradeoff in memory usage.

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
