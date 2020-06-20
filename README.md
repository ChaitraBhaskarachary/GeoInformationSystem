# GeoInformationSystem - Raspberry PI Volcano Monitoring Based NOIR Camera

Script 1: Fast Time-Lapse Acquisition
Fast time lapse takes several pictures per minute and slow time lapse take an image per second. We have used this script to acquire images every 20 seconds. Fast time lapse script uses script 3 to acquire the incoming images.


Script 2: Slow Time-Lapse Acquisition
This scheme is meant to take single image every few minute. This script acquires single image along with the image file time ,which is given by NTP(Network Time Protocol) using GPS unit or network connection. Longitude, Latitude and time syncing is stamped on the image acquired. The acquired image is then stored in form of JPEG file with file name as date and time when image was taken, the file name will be in the format of year-month-day-hour.

Script 3: Archive Fast Time Lapse Images
This script is schedules by cron to run every minute to acquire the images from script 1 along with timestamp.

Script 4: Get GPS Position
This script pulls first 30 NMEA sentences from GPS serial output, which determines the GPS location and longitude and latitude is recorded, which is passed to script 2 and script 3 to be directly stamped onto the images.

Script 5 and 6
This script checks if NTP timeserver is setting system time correctly from GPS unit.

Script 7 : 
This script creates video clip using default function raspivid. During the recording of video it temporarily suspends the cron scheduler only till duration of video clip so that overlapping requests are not made to the camera module. The script renames the video file with start date and time and moves it to the date-based folder structure which is used by time lapse images. Final output of this script is the metadata file which contains the gps coordinates and time synchronization status of video.
