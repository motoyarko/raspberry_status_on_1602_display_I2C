# raspberry_status_on_1602_display_I2C
Simple project to displaying system info on 1602 display connected by I2C

to run program by startup the pi
1. sudo nano /etc/rc.local
2. Add before the "exit 0" line "/home/pi/LCD/sys_info_to_1602_lcd.py &"
(The ampersand allows the command to run in a separate process and continue booting with the main process running.)
