from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from emotiveeyes import EmotiveEyes

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)
eyes = EmotiveEyes(device)

# Affiche l'expression "happy" pendant 3 secondes
#eyes.animate_expression("neutral", duration=3)
#eyes.animate_expression("happy", duration=3)
#eyes.animate_expression("glee", duration=3)
#eyes.animate_expression("sad", duration=3)
#eyes.animate_expression("worried", duration=3)
#eyes.animate_expression("focused", duration=3)
#eyes.animate_expression("annoyed", duration=3)
#eyes.animate_expression("surprised", duration=3)
#eyes.animate_expression("skeptic", duration=3)
#eyes.animate_expression("angry", duration=3)
#eyes.animate_expression("loving", duration=3)


#eyes.animate_expression("loving", duration=3)
#eyes.blink(original_expression="loving")
#eyes.animate_expression("loving", duration=2)


eyes.animate_expression("loving", duration=10)
