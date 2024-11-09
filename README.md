# **LH**

## **Raspberry Pi RP2040 Watch**

This is an experimental MicroPython codebase for the Raspberry Pi RP2040, specifically designed for hardware featuring the GC9A01 display and the QMIC88658 module.

![Full color TFT screen](https://github.com/nicokz/LH/blob/master/docs/img/rp2040-w-color_bg.jpg)

## **Introduction**

The **Raspberry Pi RP2040 Watch** is a DIY smartwatch project aimed at exploring the capabilities of the RP2040 microcontroller. Leveraging the power of MicroPython, this project integrates a vibrant full-color TFT display with customizable features.

In this project, you'll find experimental code that showcases various functionalities such as screen rotation, custom pixel manipulation, and opacity effects that enhance visual aesthetics. This is an ideal starting point for anyone looking to develop their own wearable tech or learn more about MicroPython on the RP2040 platform.

The Raspberry Pi RP2040 Watch project demonstrates the potential of the RP2040 microcontroller as the core of a smartwatch. With a full-color TFT display and support for a range of visual effects, this project introduces custom functionality while highlighting MicroPython’s flexibility for wearable devices.

Key features:

- Color screen manipulation and blending effects
- Custom display functions, including pixel management
- Framework for adding your features and visual elements

Whether you’re looking to create your own smartwatch or dive into MicroPython programming, this project offers a versatile foundation.

## **Project Structure**
(will be updated)
```
├── docs                     # Documentation and media
├── examples                 # Example scripts demonstrating key features
│   ├── sleep_mode_and_rtc.py    # Sleep mode and RTC integration
│   └── sprite_and_gyro.py       # Sprite movement and gyro usage
├── fonts                    # Font binary data for efficient rendering
├── images                   # Background and UI images for the display
├── main.py                  # Main script to initialize and run the watch
├── README.md                # Project documentation
├── utils                    # Utility scripts for image conversion and font processing
└── watch                    # Core watch functionality

```

## **Installation**

[TBD]

## **Libraries Overview**

The project primarily relies on two custom libraries:
1. **RP2040watch.py** – Manages display, battery status, buttons, sensor integration, and sprites for animation opportunity.

2. **Fonts.py** – Provides font rendering with advanced text positioning and blending features.

### **Dependencies**
Ensure the following dependencies are available:
- [Pi Pico RP2040 1.28-inch TFT display watch board](https://www.tindie.com/products/adz1122/pi-pico-rp2040-128-inch-tft-display-watch-board/)
- **MicroPython** for RP2040
- [Thonny Python IDE](https://thonny.org/)

## **Examples**

### **1. Basic Watch Library Information**

This code is located in the end of **/watch/RP2040watch.py** library and initializes the **GC9A01 display** and draws essential information such as battery level, device info, and a moving sprite. Can be executed by running **RP2040watch.py** on the watch directly. Use this example to verify button inputs, battery status, and basic sprite movement.

```python
...

if __name__=='__main__':
    LCD = GC9A01()
    LCD.set_bl_pwm(65535)  # Max brightness
    buttons = Buttons()
    battery = Battery()
    volts = battery.volts()
    level = battery.level()
    
    LCD.fill(LCD.black)
    LCD.fill_rect(0, 0, 240, 40, LCD.red)
    LCD.text("RP2040-LCD-1.28", 60, 25, LCD.green)
    LCD.text(f"Bat.: {level:.0f}% ({volts:.2f}V)", 40, 55, LCD.white)
    LCD.text("MicroPython GC9A01", 30, 90, LCD.green)
    LCD.text("(C) 2024, Nicholas Schreiner", 10, 145, LCD.green)
    
    sprite = Sprite("/images/python_100x60.rgba565", LCD)
    sprite.move(int((LCD.width - sprite.width)/2), 165)
    
    while True:
        volts = battery.volts()
        level = battery.level()
        LCD.fill_rect(0, 51, 240, 16, LCD.blue)
        LCD.text(f"Bat.: {level:3.0f}% ({volts:4.2f}V)", 40, 55, LCD.white)
        b_state = buttons.isPressed()
        # Update sprite position or perform other actions...
```

### **2. Fonts and Text Example**
This code is located in the end of **/watch/fonts.py** library and demonstrates text rendering and alignment with different colors and safe zones. Can be executed by running **fonts.py** on the watch directly. This example uses the fonts.py library to draw text aligned on the GC9A01 screen.

```python
if __name__=='__main__':
    screen = Screen()  # Initialize display
    screen.loadRGB565background('/images/rp2040_bg.rgb565')  # Load background
    font = Font(screen)
    text = Text(font)
    text.safe_zone(True)
    text.draw("LEFT", screen.color(110,200,110), text.ALIGN_LEFT, text.ALIGN_TOP)
    text.draw("RIGHT", screen.color(110,200,110), text.ALIGN_RIGHT, text.ALIGN_BOTTOM)
    screen.show()
```
### **3. Sleep Mode and RTC Example**
Demonstrates low-power sleep mode and the use of the RTC. The device can switch between sleep and wake-up mode by pressing **S1**. 

```python
from watch.RP2040watch import GC9A01 as Screen
from watch.RP2040watch import ButtonsIRQ as Buttons
from watch.fonts import Font, Text

rtc = machine.RTC()
rtc.datetime((2024, 11, 8, 4, 16, 29, 0, 0))  # Set initial datetime

screen = Screen()
screen.set_bl_pwm(65535)
buttons = Buttons()

def wake_up(pin):
    if isSleeping:
        text.draw("WOKE UP FROM SLEEP!", screen.color(255, 255, 255), text.CENTER, text.CENTER, True, 128)
        screen.sleep_mode(False)
        isSleeping = False
    else:
        text.draw("Zzzzzz...", screen.color(255, 255, 255), text.CENTER, text.CENTER, True, 128)
        screen.sleep_mode(True)
        isSleeping = True
    # Optional: Implement smooth dimming and more...
...
```

Full code is in **/examples/sleep_mode_and_rtc.py**

### **4. Sprite Animation with Gyroscope Example**
In this example, the sprite is moved based on data from the QMI8658 gyroscope. The IMU readings control the sprite's direction, creating interactive motion-based control.

```python
from watch.RP2040watch import GC9A01 as Screen, QMI8658, Sprite

qmi8658 = QMI8658()
screen = Screen()
screen.set_bl_pwm(65535)
screen.loadRGB565background('/images/rp2040_bg.rgb565')
sprite = Sprite("/images/lenorko.rgba565", screen)

sprite.move(int((screen.width - sprite.width) / 2), int((screen.height - sprite.height) / 2))

while True:
    xyz = qmi8658.Read_XYZ()
    stepX = -int(xyz[3])
    stepY = int(xyz[4])
    if 0 <= (stepX + sprite.posX) < (screen.width - sprite.width) and 0 <= (stepY + sprite.posY) < (screen.height - sprite.height):
        sprite.restore()
        sprite.backup()
        sprite.draw()
        screen.show()
        sprite.move(stepX, stepY)
...

```
Full code is in **/examples/sprite_and_gyro.py**

### **Additional Notes**
- **Utilities**: The /utils directory provides scripts for converting images to RGB565 and RGBA565 formats for efficient display usage and fonts generation scripts.
- **Power Consumption**: In sleep mode, power usage drops significantly, useful for battery conservation.
- **RTC Setup**: Adjust the RTC datetime in /examples/sleep_mode_and_rtc.py for correct time functionality.
- 

### ***New Functions***

Using opacity effects on full-color screens can add a visually striking element, but implementing this with MicroPython's FrameBuffer and RGB565 format presents challenges.

The default `pixel()` function in FrameBuffer often leads to inconsistent color representation, prompting the creation of custom functions—`setPixel()` and `getPixel()`—to ensure accurate color handling. Additionally, a universal `color()` function has been introduced to interpret 16-bit RGB565 color formats effectively. This setup also incorporates opacity functions that enable smooth blending effects on the screen, elevating the visual experience of your smartwatch.

**No MicroPython FrameBuffer useage**

### ***Architecture and Programming Strategy***

**"while True"** vs **Threading** Buttons Control

---

#### 1. **CPU Usage**

**while True loop**: This version constantly polls the button states and performs simple calculations within each loop. Although it’s straightforward, the constant polling can be CPU-intensive since it doesn’t release control back to the main program unless specifically told to (via `time.sleep()`).
- **CPU Load**: Higher because the CPU spends more time actively in the button-monitoring loop, potentially blocking other tasks.
- **Latency**: Button checks are fast and have minimal latency as they occur on every loop iteration.
- **Efficiency**: Good for time-sensitive applications that prioritize real-time button monitoring over multitasking.

**uasyncio version**: With uasyncio, we achieve cooperative multitasking by yielding control with `await asyncio.sleep()`. This allows other tasks to run while the button state check “waits” briefly, making it less CPU-intensive.
- **CPU Load**: Lower because it doesn't block the CPU. Other tasks can be executed during await periods, reducing the need for constant polling.
- **Latency**: Slightly higher than the while True loop, as the button check depends on the `await asyncio.sleep()` delay. This increase is generally negligible unless the delay is unusually long.
- **Efficiency**: Better for multitasking, especially when there are other concurrent tasks (e.g., display updates, sensor monitoring).

---

#### 2. **Memory Usage**

**while True loop**: This approach uses minimal memory because it only requires a few variables and doesn’t involve task management overhead.
- **Memory Footprint**: Minimal, relying on direct calls and simple control flow.
- **Scalability**: As the project grows and more features are added, the `while True` loop may become harder to manage. Each new feature would add complexity within the same loop, potentially making it harder to scale.

**uasyncio version**: The use of uasyncio introduces additional memory overhead, particularly for managing the coroutine and event loop.
- **Memory Footprint**: Higher than the `while True` loop due to the creation of additional structures such as task management and stack frames for each asynchronous function.
- **Scalability**: Much better than `while True`, as new asyncio tasks can be added without complicating the main loop. This is ideal for applications requiring multiple concurrent tasks.

**IRQ Buttons Control**: Using **IRQ (Interrupt Request)** for button presses provides a very efficient way to handle button input events with minimal memory overhead. Rather than constantly polling for button states, IRQ interrupts the normal flow only when a button is pressed, allowing for an asynchronous response.
- **Memory Footprint**: Very low, as it only requires memory to store the interrupt handler function and pin configuration. No need for continuous polling or an event loop.
- **Scalability**: Highly scalable because multiple buttons can be managed with separate interrupt handlers. Adding new features, such as long press or double press detection, does not significantly impact memory usage or the main loop.

---

#### 3. **Summary and Recommendation for RP2040**

- **If Real-Time Responsiveness Is Critical** (e.g., immediate reaction to button presses with low latency), the `while True` loop version is simpler, uses less memory, and has minimal latency.
  
- **If Multitasking and Code Readability Are Important** (e.g., if you need to run other tasks like display updates, sensor monitoring, etc.), the `uasyncio` version is better, despite its higher memory use and slightly increased latency.

---

#### Typical Usage on RP2040

- For projects that are primarily button-driven and don’t require multitasking, the **`while True` loop** is a good choice for simplicity and low memory consumption.
  
- If you need your button monitoring to run concurrently with other tasks, the **`uasyncio` version** is worth considering, even with the slight tradeoff in memory usage.
  
- If you require efficient button handling with minimal memory overhead, the **IRQ Buttons Control** is ideal, especially when real-time responsiveness and scalability are key factors.


## **Magic of `@micropython.viper` on RP2040-based Devices**

Your current `Sprite` class is quite comprehensive for sprite manipulation, including loading, drawing, moving, and handling backups of the screen buffer. To enhance the performance of your animation tasks, especially when dealing with drawing and restoring sprites, you can leverage `@micropython.viper` to make these operations faster by using direct memory access with pointers (`ptr8`). 

### 1. **Using `@micropython.viper` for Optimization**

The `@micropython.viper` decorator allows you to compile your Python code into machine code, greatly increasing the execution speed of your functions. This is particularly useful for sprite and animation tasks where performance is crucial, such as moving sprites, updating the screen, and restoring backgrounds efficiently. By using `viper`, you avoid the overhead of Python’s dynamic type system, making operations like drawing and restoring sprites much faster.

- **`restore()`**: When restoring the background pixels to the screen, this function uses `ptr8` to access both the sprite's backup buffer and the screen buffer directly in memory. The loop is optimized with `viper` for efficient background restoration.

- **`backup()`**: Similarly, the `backup()` function uses `ptr8` to backup the screen data before the sprite is drawn. This is critical for correctly restoring the background when the sprite is moved or erased.

- **`draw()`**: The `draw()` function uses `ptr8` to directly manipulate the screen buffer and sprite buffer, allowing for fast drawing of sprite pixels. The `@micropython.viper` decorator ensures that each pixel is placed on the screen as quickly as possible.

### 2. **How This Relates to Animation and Sprite Manipulation**
In animation, where you need to update the screen multiple times per second, efficiency is key. By utilizing `@micropython.viper`, you can ensure that critical operations like moving and drawing sprites don’t bottleneck your animations. The combination of fast `restore()`, `backup()`, and `draw()` methods ensures that the screen is updated in real time without introducing unnecessary delays.

For example, when animating a sprite, you typically:
1. **Backup** the background where the sprite will be drawn.
2. **Draw** the sprite in its new position.
3. After some time or movement, **Restore** the background to erase the sprite from its previous position.
4. Then, **draw** the sprite in the new position.

This loop repeats many times during animation. Without `viper`, these operations might cause performance issues due to Python's dynamic memory handling. But with `viper`, the performance improves significantly, allowing for smoother animations even with limited resources.

### 3. **Example of How to Use It in Animation**
Here’s an example of how you might integrate this into an animation loop:

```python
import time
import watch.RP2040watch

...
# Assuming screen is already defined and initialized
sprite = Sprite("/path/to/sprite.rgba565", screen)
...
# Move sprite in a loop
while True:
    sprite.backup()        # Backup the background where the sprite will be
    sprite.move(2, 0)      # Move sprite 2 pixels right
    sprite.draw()          # Draw the sprite at its new position
    time.sleep(0.05)       # Wait for a short time (for animation speed)
    sprite.restore()       # Restore the background from backup (erase sprite)
...
```
For detailed working code, see run code of /watch/RP2040watch.py or example in /examples/sprite_and_gyro.py

### 4. **Benefits of Using @micropython.viper for RP2040 Watch Animations**
- **Speed**: Sprite manipulations (moving, drawing, restoring) happen at much higher speeds, ensuring smooth animations.
- **Memory Efficiency**: Direct memory manipulation with pointers allows you to avoid unnecessary memory allocations and copying, which is essential for embedded systems with limited memory like the RP2040.
- **Real-Time Performance**: Animations, especially with real-time inputs or sensor data, can be performed without noticeable delays, improving the responsiveness of your watch’s UI.
- **Scalability**: As your project grows (e.g., more complex animations or more sprites), using viper ensures that performance doesn’t degrade with added complexity.

### 5. **Additional Optimizations**
You can continue improving the performance of your animation logic by using viper in any other method that requires intensive calculations or operations, such as:

- Collision detection (e.g., if you add interactive elements to your animations).
- Sensor-based adjustments (e.g., changing sprite positions based on accelerometer input or time).

### **Conclusion**
By applying the **@micropython.viper** decorator to the core methods of your Sprite class, such as restore(), backup(), and draw(), you greatly enhance the performance of your sprite animations. This makes your RP2040-based watch capable of handling smooth, real-time animations and interactions, even with limited processing power and memory. This approach ensures that the watch's UI remains responsive and efficient, even as the complexity of your animations increases.

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
- **0.1.1:** Code base line is updated. Animation, fonts and text functionality is added. Examples are added.

## **Contact**

If you have any questions or comments about the Raspberry Pi RP2040 Watch, please reach out to **nico** at **service@lighthunter.ws**.
