Raspbian Weather Station
========================

Raspberry Pi-based front end for an Airmar 200WX.

### Bill of Materials

|  # | Description                                            | $ (est) |
|----|--------------------------------------------------------|---------|
|  1 | [Airmar 200WX][bom-200]                                |  [1300] |
|  2 | [Aimar 0183 NMEA cable][bom-cbl]                       |    [65] |
|  3 | [RS485-to-RS232 serial converter][bom-232]             |     75* |
|  4 | [Barrel jack, 5.5mm X 2.1mm, DC power][bom-jck]        |      -  |
|  5 | [Power supply, 12Vdc @ 2A][bom-12v]                    |      6  |
|  6 | [Buck converter to 5V][bom-5dc]                        |     12  |
|  7 | [Nulsom male RS232-to-TTL serial converter][bom-ttl]   |      9  |
|  8 | [Raspberry Pi Model B+][bom-rpi]                       |     32  |
|  9 | [microSD card, 4GB][bom-usd]                           |      5  |
| 10 | [Panel mount Ethernet extension][bom-pme]              |      3  |
| 11 | [Momentary button][bom-btn]                            |      1  |
| 12 | [Enclosure][bom-enc]                                   |      7  |
|  - | Female-female jumper wires                             |      -  |
|    | *Total (excluding 200WX & cable)*                      |    105  |

Substitutions may apply. Links are provided for completeness; we're not here
to endorse products or vendors.

*(\*) We had this item on-hand but should you choose a less inexpensive model,
it might be wise to invest in an opto-isolated model. A mid-range price for such
a converter is ~$75 as I write this.*

  [bom-200]: https://duckduckgo.com/?q=airmar+200wx
  [bom-cbl]: https://duckduckgo.com/?q=airmar+nmea+0183+cable
  [bom-232]: http://www.digikey.com/product-detail/en/SCP311T-DFTB3/1165-1055-ND/3045941
  [bom-jck]: https://www.amazon.com/Generic-5-5mmx2-1mm-Supply-Adapter-Socket/dp/B00EQ1UWX4
  [bom-12v]: https://www.amazon.com/RockBirds-12V-Switching-Supply-Adapter/dp/B00VM292AO
  [bom-5dc]: https://www.amazon.com/Waterproof-Converter-Voltage-Module-Interface/dp/B00CGQME5U
  [bom-ttl]: https://www.amazon.com/Ultra-Compact-RS232-Converter-Male/dp/B00OPU2QJ4
  [bom-rpi]: https://www.amazon.com/Raspberry-Pi-Model-512MB-Computer/dp/B00LPESRUK
  [bom-usd]: https://www.amazon.com/Sandisk-MicroSDHC-Memory-Card-Adapter/dp/B000SMVQK8
  [bom-pme]: https://www.amazon.com/JoyliveStore-Female-Ethernet-Network-Extension/dp/B00WLYRPI8
  [bom-btn]: https://www.amazon.com/uxcell-Momentary-Pushbutton-Switch-DS-425/dp/B00HG7GWRK
  [bom-enc]: https://www.amazon.com/Hammond-1591ESBK-ABS-Project-Black/dp/B0002BSRIO


### Usage

> **TODO**

* administration
    * access/login/security (change password, add/remove SSH keys)
    * time (set the timezone, update NTP time sources)
    * keeping things up to date (apt-get updates, git clone kplex?)
* getting data
    * TCP socket: view real-time data with NMEA-viewer app (NavMonPC)
    * files: retrieved via SMB share
        * raw NMEA files (GPS, weather, etc)
        * parsed-out 1Hz weather
        * reduced data sets (TODO: produce minutely, half-hourly and daily data set)
    * CONTAM-compatible weather files via webpage (TODO)
* ????


### Setup

#### Assembly


**TODO: block diagram**


**TODO: picture of enclosure, opened up**


#### SD Card Preparation

Starting from a clean operating system is not required, but highly recommended.
There are many guides available online describing the process of writing an image
to SD card so won't cover that explicitly here. 

We use [Raspbian Jessie Lite](https://www.raspberrypi.org/downloads/raspbian/) as
the base OS (release 2016-03-18 to be exact, though you should use the latest).
In addition, we move the OS partition from the SD card to a USB flash drive for
performance and longevity reasons. You can certainly skip that step if you'd like
but it's not that difficult:

1. Flash the Raspbian image to the USB flash drive (ex:
   `sudo dd bs=4M if=Downloads/2016-03-18-raspbian-latest of=/dev/sdb`)
2. Format an SD card in FAT32 (we used GParted)
3. Copy the boot partition from the USB flash drive to the SD card (ex:
   `sudo cp -a /media/username/boot/* /media/username/0D05-45A2` where
   the flash drive boot partition is mounted to `/media/username/boot` and
   the SD card is `/media/username/0D05-45A2`)
4. Edit the SD card's copy of `cmdline.txt` to specify `root=/dev/sda2`
5. Insert SD card and USB flash drive into Raspberry Pi (*remove other flash
   drives, if present!*) then provide power to the Pi
6. Resize the flash drive partition by deleting the partition with `fdisk`
   and creating a new, larger one (see resources below).

**TODO**

* specify disk UUID in `cmdline.txt` argument (ie `root=/dev/disk/by-uuid/...`)

Relevant Resources:

* online search: "install raspbian to flash drive"
* https://www.stewright.me/2013/05/install-and-run-raspbian-from-a-usb-flash-drive/
  mostly comprehensive, but missing UUID-related improvements
* https://samhobbs.co.uk/2013/10/speed-up-your-pi-by-booting-to-a-usb-flash-drive
  beyond above, has UUID-related fix but could be better still
* https://lists.debian.org/debian-user/2011/05/msg00721.html
  has improvement on above entry
* https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=99493 [response 20150210T2200]
  confirms first source above w.r.t resizing file system
* http://zeroset.mnim.org/2012/10/03/move-an-existing-raspbian-installation-from-memory-sd-card-to-usb-flash-drive-stick/
  moves existing installation instead of starting fresh



#### Initial OS Setup

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\FIXME

Run `sudo raspi-config` after logging in (`pi`/`raspberry`) to start the
initial setup utility.

> *If you have already connected the device to the Pi, you may see horrible
> errors covering your screen after boot. Try pressing 'Enter' several
> times to get a visible login prompt.*

* ~~Expand Filesystem~~ If you followed along and have the OS on a flash
  drive, then *raspi-config* won't know how to expand the file system. Use
  the resources listed above.
* Change User Password
    * Yes
* Internationalization
    * Set your preferred locale (we use `en_US.UTF-8`)
    * Set your time zone (we use `GMT+8` for Pacific Standard Time year-round;
      the inverted sign (+8) is a POSIX quirk)
    * Set your keyboard (we use US English)
* Advanced Options
    * Set the hostname (we use `airmar200wx`)
    * Enable SSH
    * Disable serial shell/kernel messages (to repurpose UART for serial input)
* Exit saving changes and reboot

Login, then fetch and apply system updates. The `dist-upgrade` command goes
further than `upgrade` by resolving dependencies and removing stale packages. 
Since we're starting fresh, it makes more sense. 

```
pi@airmar200wx:~ $ sudo apt-get update
...
pi@airmar200wx:~ $ sudo apt-get dist-upgrade -y
...
```

Next fetch and apply firmware updates. The firmware is independent of the
system packages and must be updated seperately. Unfortunately, Jessie Lite
doesn't come with the updater package, `rpi-update`, so you must install it 
first.

```
pi@airmar200wx:~ $ sudo apt-get install rpi-update -y
...
pi@airmar200wx:~ $ sudo rpi-update
...
```

It should update without errors and advise you to reboot. Enter `sudo reboot`
to proceed.

#### *kplex* Setup

*kplex* is a NMEA multiplexing server; it's used to rebroadcast the Airmar
200WX data stream via TCP socket.

> If you have not yet disabled shell/kernel messages on the hardware serial
> port, use `raspi-config` to do so before continuing.

##### Create Account

Create a new system user for *kplex* to run under. We create a new group for
the user (instead of letting it get the default **nogroup** group), then add
it to the **dialout** group so it can access the hardware serial port.

```
pi@airmar200wx:~ $ sudo adduser --system --group kplex
Adding system user `kplex' (UID 109) ...
Adding new group `kplex' (GID 113) ...
Adding new user `kplex' (UID 109) with group `kplex' ...
Creating home directory `/home/kplex' ...
pi@airmar200wx~ $ sudo usermod -a -G dialout kplex
```

##### Clone and Build

Clone the source code repository into the new home directory and pretend to
be the *kplex* user so it receives file ownership. 

```
pi@airmar200wx:~ $ sudo -u kplex git clone https://github.com/stripydog/kplex /home/kplex
Cloning into `/home/kplex`...
remote: Counting objects: 812, done.
Receiving objects: 100% (812/812), 272.18 KiB | 258.00 KiB/s, done.
remote: Total 812 (delta 0), reused 0 (delta 0), pack-reused 812
Resolving deltas: 100% (595/595), done.
Checking connectivity... done.
```

Next switch to source code directory and build the program, while continuing
to masquerade as the new 'kplex' user.

```
pi@airmar200wx:~ $ cd /home/kplex
pi@airmar200wx:/home/kplex $ sudo -u kplex make
cc -g -Wall   -c -o kplex.o kplex.c
cc -g -Wall   -c -o fileio.o fileio.c
cc -g -Wall   -c -o serial.o serial.c
cc -g -Wall   -c -o bcast.o bcast.c
cc -g -Wall   -c -o tcp.o tcp.c
cc -g -Wall   -c -o options.o options.c
cc -g -Wall   -c -o error.o error.c
cc -g -Wall   -c -o lookup.o lookup.c
cc -g -Wall   -c -o mcast.o mcast.c
cc -g -Wall   -c -o gofree.o gofree.c
cc -g -Wall   -c -o udp.o udp.c
cc -o kplex kplex.o fileio.o serial.o bcast.o tcp.o options.o error.o lookup.o mcast.o gofree.o udp.o -pthread -lutil
```

After a successful build, the program is installed (as *root*, not *kplex*). 
You can see the executable's location using `which`.

```
pi@airmar200wx:/home/kplex $ sudo make install
test -d "//usr/bin" || install -d -g root -o root -m 755 //usr/bin
Install -g root -o root -m 755 kplex //usr/bin/kplex
pi@airmar200wx:/home/kplex $ which kplex
/usr/bin/kplex
```

Now is a good time to switch back to our home directory (`cd ~`).

##### Configure 

Copy the example configuration file to the location expected by the service,
then uncomment and update the values as appropriate. The weather station is 
connected to the hardware serial port (`/dev/ttyAMA0`) and its baud rate is
4800 by default.

```
pi@airmar200wx:~ $ sudo cp /home/kplex/kplex.conf.ex /etc/kplex.conf
pi@airmar200wx:~ $ sudo nano /etc/kplex.conf
```
```
...
[serial]
filename=/dev/ttyAMA0
direction=both
baud=4800

[tcp]
mode=server
port=10110
direction=out
```

##### Install as Service

Create a `systemd`-compatible service file:

```
pi@airmar200wx:~ $ sudo nano /etc/systemd/system/kplex.service
```
```
[Unit]
Description=kplex (NMEA multiplexer)
After=syslog.target network.target

[Service]
Type=simple
User=kplex
Group=kplex
ExecStart=/usr/bin/kplex

[Install]
WantedBy=multi-user.target
```

Finally, enable the service to start at boot:

```
pi@airmar200wx:/home/kplex $ sudo systemctl enable kplex
Created symlink from /etc/systemd/system/multi-user.target.wants/kplex.service to /etc/systemd/system/kplex.service
pi@airmar200wx:/home/kplex $ sudo systemctl start kplex
```

Reboot, then run `systemctl` to verify *kplex* is running.

#### Log data to file

> The real meat-and-potatoes of this repository is found here.

If you haven't yet, clone this repository and step inside it.

> **FIXME** update the repository address below using final repo name!
> To shortcut the future change, we're specifying the destination folder.

```
$ git clone https://bitbucket.org/patricktokeeffe/rpi-airmar-200wx rpi-airmar200wx
Cloning into 'rpi-airmar200wx'...
Username for 'https://bitbucket.org': patricktokeeffe
Password for 'https://patricktokeeffe@bitbucket.org':
remote: Counting objects: 46, done.
remote: Compressing objects: 100% (41/41), done.
remote: Total 46 (delta 18), reused 0 (delta 0)
Unpacking objects: 100% (46/46), done.
Checking connectivity... done.
pi@airmar200wx:~ $
```

To "install" the logging scripts, copy them into the `/usr/sbin` directory
(per the [Filesystem Hierarchy Standard](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard))
with new names (sans file extension), then mark the copied scripts as
executable.

```
pi@airmar200wx:~/rpi-airmar200wx $ sudo cp scripts/nmea2file.py /usr/sbin/nmea2file
pi@airmar200wx:~/rpi-airmar200wx $ sudo cp scripts/weather-logger.py /usr/sbin/weather-logger
pi@airmar200wx:~/rpi-airmar200wx $ sudo chmod +x /usr/sbin/nmea2file.py
pi@airmar200wx:~/rpi-airmar200wx $ sudo chmod +x /usr/sbin/weather-logger.py
```

Next, create the output directories for the logging scripts (**FIXME**):

```
pi@airmar200wx:~ sudo mkdir -p /var/log/airmar200wx/nmea
pi@airmar200wx:~ sudo mkdir -p /var/log/airmar200wx/tsv
```

Finally, copy the provided service configuration files to `/etc/systemd/system`
and set them to start at boot with `systemctl enable`. 

```
pi@airmar200wx:~ sudo cp scripts
pi@airmar200wx:~ sudo systemctl enable nmea2file
Created symlink from /etc/systemd/system/multi-user.target.wants/nmea2file.service to /etc/systemd/system/nmea2file.service.
pi@airmar200wx:~ sudo systemctl enable weather-logger
Created symlink from /etc/systemd/system/multi-user.target.wants/weather-logger.service to /etc/systemd/system/weather-logger.service.
```

Reboot and check the services are running correctly with `systemctl`. If a
service fails to start, you can get more information by calling 
`sudo systemctl status X` where "`X`" is the service name (i.e. 'nmea2file').


#### Samba (SMB) Setup

1. Install samba for sharing data: `sudo apt-get install samba -y`
2. Update samba config: `sudo nano /etc/samba/smb.conf`
    * (optional) update workgroup under "[global]" section near top
    * comment out the default exports (home directories & printers)
    * add the text block below at the end-of-file
3. Restart samba (must use old-style init.d command):
   `sudo /etc/init.d/samba restart`

```
[data]
   browseable = yes
   comment = Data share (read-only)
   create mask = 0700
   directory mask = 0700
   only guest = yes
   path = /var/log/airmar200wx
   public = yes
   read only = yes
```

#### Update clock using GPS

Feed specific GPS sentences to the local NTP daemon so the clock
is updated without a network connection.

Start by adding a psuedo-terminal which only receives the Recommended
Minimum Coordinates sentence (GPRMC). 

```
$ sudo nano /etc/kplex.conf
```
```
...

[pty]
mode=master
filename=/////////////////
direction=out
ofilter=+GPRMC:-all

```

Now create a FIFO for kplex to connect to...

```
$ sudo mkfifo /dev/gps0
```

And tell NTP to use that FIFO as a GPS source...

```
$ sudo nano /etc/ntp.conf
```
```
...
server 127.127.20.0 mode 1 prefer
...
```

`mode 1` indicates to only process `$GPRMC` sentences, and to expect
the default baud rate of 4800 bps. The `prefer` directive gives some
extra weight to the local GPS.

scenario 1 (ntp 4.2.6p5)

- create FIFO, assign ownership to `kplex`
- kplex writes to file `/dev/gps0`
- NTP uses `server 127.127.20.0`

-> results after restarting NTP (systemctl status)

    ...
    peers refreshed
    Listening on routing socket on fd #23 for interface updates
    refclock_setup fd 5 tcgetattr: Inappropriate ioctl for device

Device not listed in output of `ntpq -p`

--> tried updating to v4.2.8p7... still no device listed by `ntpq -p`
    and the error changed from `fd 5 tcgetattr` to `fd 4 tcgetattr`


scenario 2 (ntp 4.2.6p5)

- kplex writes to pty `/home/kplex/gps0`
- symlinked `/home/kplex/gps0` -> `/dev/gps0`
- NTP uses `server 127.127.20.0`

-> results after restarting NTP:

    ...
    peers refreshed
    Listening on routing socket on fd #23 for interface updates
    refclock_setup fd 5 TIOCMGET: Invalid argument
    GPS_NMEA(0) serial /dev/gps0 open at 4800 bps

and from `ntpq -p`: 

    remote           refid    st t when poll reach  delay   offset  jitter
    GPS_NMEA(0)      .GPS.     0 l   33   64    0   0.000    0.000   0.000
    ...


--> tried updating to 4.2.8p7... mixed results: still have "TIOCMGET"
    error but with `fd 4` instead of `fd 5`, but DO now see entry in
    `ntpq -p` with non-zero offset/jitter values... BUT GPS was marked as
    false ticker (x)    ........... waiting, waiting, waiting..... OK,
    after a few minutes local GPS gets selected (*)!


#### Off button support

Install support for a physical off button from this repository:

> https://bitbucket.org/patricktokeeffe/raspbian-off-button

*Note: this repository address may change to `.../rpi-off-button`
in the near future.*


#### RPi-Monitor Setup

***TODO***

Edit `/etc/rpimonitor/data.conf` to include these templates:
    `services.conf`
    `dht11.conf`

In `services.conf`, copy existing sections to add support for monitoring:
    rpimonitor    8888
    kplex         10110


In `dht11.conf` adapt first dynamic block to read air temp from file:

```
dynamic.1.name=roof_temp
dynamic.1.source=/dev/airmar200wx/air_temp
dynamic.1.regexp=(\S+)
dynamic.1.postprocess=$1
dynamic.1.rrd=GAUGE
```

Update references to `data.air_temp`. Comment out humidity stuff.
Restart rpimonitor service.



### Reference

* [Airmar PB200 Weather Station User Manual][ref-pb200]

  [ref-pb200]: http://www.airmartechnology.com/uploads/installguide/PB200UserManual.pdf















