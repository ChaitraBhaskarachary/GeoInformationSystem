import os 
#Acquire image and name file based on date-time 
os.chdir('/media/usb/webcam/') 
os.system('kill $(pgrep raspistill)') 
os.system('raspistill -o timelapse1%04d.jpg -q 90 -w 1024 -h 768 580000 -tl 10000 -vf -hf -ex auto -awb auto -n'); 
#acquire image 
path='/media/usb/webcam/timelapse*jpg'
