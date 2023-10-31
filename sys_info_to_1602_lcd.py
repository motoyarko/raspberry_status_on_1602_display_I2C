#! /usr/bin/env python

import smbus
import time
import psutil

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address, if any error, change this address to 0x27
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
 # Initialise display
 lcd_byte(0x33,LCD_CMD) # 110011 Initialise
 lcd_byte(0x32,LCD_CMD) # 110010 Initialise
 lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
 lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
 lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
 lcd_byte(0x01,LCD_CMD) # 000001 Clear display
 time.sleep(E_DELAY)

def lcd_byte(bits, mode):
 # Send byte to data pins
 # bits = the data
 # mode = 1 for data
 #        0 for command
 bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
 bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

 # High bits
 bus.write_byte(I2C_ADDR, bits_high)
 lcd_toggle_enable(bits_high)

 # Low bits
 bus.write_byte(I2C_ADDR, bits_low)
 lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
 # Toggle enable
 time.sleep(E_DELAY)
 bus.write_byte(I2C_ADDR, (bits | ENABLE))
 time.sleep(E_PULSE)
 bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
 time.sleep(E_DELAY)

def lcd_string(message,line):
 # Send string to display

 message = message.ljust(LCD_WIDTH," ")

 lcd_byte(line, LCD_CMD)

 for i in range(LCD_WIDTH):
   lcd_byte(ord(message[i]),LCD_CHR)

def get_system_info():
 # Get cpu statistics
 # cpu = str(psutil.cpu_percent()) + '%'
 cpu = psutil.getloadavg()
 cpu = str(round(cpu[0],1)) + " " + str(round(cpu[1],1)) + " " + str(round(cpu[2],1))

 # Calculate memory information
 memory = psutil.virtual_memory()
 # Convert Bytes to MB (Bytes -> KB -> MB)
 available = round(memory.available/1024.0/1024.0)
 total = round(memory.total/1024.0/1024.0)
 used = round(memory.used/1024.0/1024.0)
 mem_info = str(total) + "  " + str(used) # + 'MB' #( ' + str(memory.percent) + '% )'

 # Calculate swap
 swap = psutil.swap_memory()
 used_swap = round(swap.used/1024.0/1024.0)
 total_swap = round(swap.total/1024.0/1024.0)
 swap_mem_info = str(total_swap) + "  " + str(used_swap)

 # Calculate disk information
 disk = psutil.disk_usage('/media/myCloudDrive')
 # Convert Bytes to GB (Bytes -> KB -> MB -> GB)
 free = round(disk.free/1024.0/1024.0/1024.0)
 total = round(disk.total/1024.0/1024.0/1024.0)
 used = round(disk.used/1024.0/1024.0/1024.0)
 disk_info = str(total) + " " + str(used) # 'GB free / ' + str(total) + 'GB total ( ' + str(disk.percent) + '% )'

 #print("CPU Info–> ", cpu)
 #print("Memory Info–>", mem_info)
 #print("Disk Info–>", disk_info)

 return([cpu, mem_info, swap_mem_info, disk_info])

def main():
 # Main program block

 # Initialise display
 lcd_init()

 while True:
   # Get system information
   sys_info = get_system_info()
   cpu = sys_info[0]
   mem = sys_info[1]
   swap_mem = sys_info[2]
   disk = sys_info[3]


   # Send some test
   lcd_string("Time:  " + time.strftime("%H:%M", time.localtime()),LCD_LINE_1)
   lcd_string("Cpu  " + cpu,LCD_LINE_2)
   time.sleep(5)
   lcd_string("Mem  Total Used ",LCD_LINE_1)
   lcd_string("     " + mem,LCD_LINE_2)
   time.sleep(5)
   lcd_string("Swap Total Used ",LCD_LINE_1)
   lcd_string("     " + swap_mem,LCD_LINE_2)
  time.sleep(5) # Send some more text lcd_string("> Tutorial Url:",LCD_LINE_1)
   lcd_string("HDD  Total Used ",LCD_LINE_1)
   lcd_string("     " + disk,LCD_LINE_2)
   time.sleep(5)

if __name__ == '__main__':

 try:
   main()
 except KeyboardInterrupt:
   pass
 finally:
   lcd_byte(0x01, LCD_CMD)
