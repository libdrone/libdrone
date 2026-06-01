---
id: payload-software-protocol
title: "Payload software protocol"
version: 1.0.0
date: 2026-04-12
author: jsa
status: released
scope: libdrone
topic:
  - payload-architecture
personas:
  - 3.payload-dev
  - 5.student
  - 8.architect
platform:
  - all
lang: en
licence: CC BY-SA 4.0
---

## Summary

The libdrone payload software interface defines three buses: a realtime bus
(MSP on UART4 RX, payload to FC, for OSD display in the pilot's goggles), a
control bus (plain text on UART4 TX, FC to payload, for pilot commands), and
a GPS bus (NMEA on Connector B PIN 2, read-only, for position tagging).
Every compliant payload must implement all three. A payload that only logs
to SD card without sending OSD data, or that ignores pilot commands, is
non-compliant. The I2C bus and GPIO lines complete the interface for sensors
and radio-controlled switching.

---

## Concept

### Why three buses are required

A logging-only payload is invisible to the pilot in flight. The pilot cannot
confirm the sensor is running, cannot see readings in the goggles, and cannot
stop logging if something goes wrong. A payload that streams OSD but cannot
be commanded is outside pilot control during the flight. Three-bus compliance
ensures the pilot has visibility (OSD), authority (commands), and the payload
has context (GPS position for data tagging). All three together make the
system safe and scientifically useful.

### MSP OSD protocol (UART4 RX)

The FC's OSD system uses MSP DisplayPort to receive character data from the
payload and overlay it on the HDZero video frame. The payload sends MSP frames
on UART4 RX at 2–10 Hz. The FC relays them to the VTX, which renders them in
the goggles.

MSP frame format for OSD write:

    $M< [byte_count] [182] [row] [col] [0x00] [char0...charN] [0x00] [CRC]
    $M< [1]          [182] [4]   [CRC_of_above]   (draw screen command)

The CRC is the XOR of all bytes from `byte_count` onward.

Update rate: 2 Hz minimum for visibility, 10 Hz maximum for bandwidth
efficiency. The OSD renders at video frame rate (60 Hz) regardless — sending
faster than 10 Hz adds no visual benefit and wastes UART bandwidth.

### Command bus (UART4 TX)

The FC sends plain-text newline-terminated commands to the payload at
115,200 baud. Commands are triggered by pilot radio switch actions. Every
compliant payload must respond to at minimum `ENABLE` and `DISABLE`.

Standard command vocabulary:

| Command | Meaning | Required response |
|---|---|---|
| `ENABLE\n` | Begin operation | `OK\n` |
| `DISABLE\n` | Suspend operation | `OK\n` |
| `LOG_START\n` | Begin SD logging | `LOG_OK\n` or `LOG_ERR\n` |
| `LOG_STOP\n` | Stop SD logging | `OK\n` |
| `STATUS\n` | Report state | `STATUS:state,detail\n` |

Custom commands may be added using the same format, provided they do not
conflict with the standard vocabulary.

### GPS bus (Connector B PIN 2)

NMEA sentences at 57,600 baud, 10 Hz update rate. The payload parses GGA
sentences for latitude, longitude, altitude, and satellite count. Every
logged data record should be tagged with the GPS timestamp and position
at the time of measurement.

The 1 MΩ series resistor on the drone side limits the GPS tap to read-only.
Never attempt to write to this pin.

### I2C sensor bus (Connector A PIN 5/6)

FC is I2C master. Payload sensors are slaves. The payload does not initiate
I2C transactions — it responds to FC-initiated reads. For the Sensirion SEN66
at address 0x6B: the FC reads measurement frames at 1 Hz and forwards the
data to the OSD. The payload MCU may also read the sensor independently if it
needs the data for logging — I2C allows multiple masters with proper
arbitration, but the simpler approach is to have the payload MCU read the
sensor and send the data to the FC via MSP.

### GPIO control (Connector B PIN 5/6)

Radio switches on the TX16S map to AUX channels in Betaflight. Betaflight
drives the corresponding GPIO pins high/low. The payload reads these as
digital inputs and responds: GPIO1 high = master enable, GPIO1 low = master
disable. This is the hardware backup to the UART command bus — if UART
communication fails, GPIO still provides enable/disable authority.

---

## Reference

### Minimum viable OSD implementation (MicroPython)

    def msp_write_osd(uart, row, col, text):
        data = bytes([row, col, 0x00]) + text.encode() + b'\x00'
        n = len(data)
        cmd = 182  # MSP_DISPLAYPORT
        crc = n ^ cmd
        for b in data:
            crc ^= b
        frame = b'$M<' + bytes([n, cmd]) + data + bytes([crc])
        uart.write(frame)
        # Draw screen command
        draw_data = bytes([4])
        n2 = 1
        crc2 = n2 ^ cmd ^ 4
        uart.write(b'$M<' + bytes([n2, cmd]) + draw_data + bytes([crc2]))

### Minimum viable GPS parser (MicroPython)

    def parse_gga(sentence):
        parts = sentence.split(',')
        if len(parts) < 10 or parts[6] == '0':
            return None
        lat_raw = float(parts[2])
        lat = int(lat_raw / 100) + (lat_raw % 100) / 60
        if parts[3] == 'S': lat = -lat
        lon_raw = float(parts[4])
        lon = int(lon_raw / 100) + (lon_raw % 100) / 60
        if parts[5] == 'W': lon = -lon
        return lat, lon, float(parts[9]), int(parts[7])


### Recommended OSD field layout

| Row | Col | Content |
|---|---|---|
| 1 | 1 | Primary sensor reading (e.g. `PM2.5: 34 ug/m3`) |
| 2 | 1 | Secondary reading (e.g. `CO2: 412 ppm`) |
| 3 | 1 | Log status (e.g. `LOG: REC 00:04:32`) |
| 4 | 1 | GPS lock indicator |

### Three-bus compliance requirement

| Bus | Signal path | Minimum implementation |
|---|---|---|
| Realtime (OSD) | UART4 RX → FC → VTX → goggles | MSP OSD frames at ≥2 Hz |
| Control | UART4 TX → payload MCU | Respond to ENABLE and DISABLE |
| Storage | SD card or equivalent | GPS-tagged records at ≥1 Hz |
| GPS | Connector B PIN 2 → payload MCU | Parse GGA, tag all logged records |

---

## Procedure

### Testing the software interface on the bench

1. Connect a USB-serial adapter to UART4 RX (Connector A PIN 4). Open a
   terminal at 115,200 baud. Confirm MSP frames are arriving when the ESP32
   sends them. Decode manually: first three bytes should be `24 4D 3C` ($M<).
2. Connect a USB-serial adapter to UART4 TX (Connector A PIN 3). Send `ENABLE\n`
   and verify the payload responds `OK\n` on a second serial monitor.
3. Connect a USB-serial adapter to Connector B PIN 2. Set baud to 57,600.
   Confirm NMEA sentences arrive at 10 Hz when connected to a powered drone
   outdoors.
4. In Betaflight Configurator → OSD tab: verify the payload OSD fields appear
   in the layout. If not, check MSP DisplayPort is assigned to UART1 (VTX).

---

## Rationale

### Why plain text for the command bus instead of MSP

MSP binary framing on the command bus would allow structured bidirectional
communication but requires careful framing implementation on both FC and
payload sides. The current command vocabulary is small and low-frequency —
one command per switch throw, not a continuous data stream. Plain text with
newline termination is easier to implement in MicroPython, easier to debug
on the bench with a serial terminal, and adequate for the command rates
involved. If the command vocabulary grows to require structured data or
higher bandwidth, MSP on UART4 TX is the natural upgrade path.

---

## Connections

requires:
  - [[payload-electrical-interface]]
  - [[gx12-connector-standard]]
related:
  - [[flight-controller-hardware]]
  - [[imu-gyroscope]]
  - [[gnss-gps]]
leads_to:
  - [[psb1-shield-board]]


[payload-electrical-interface]: payload-electrical-interface.md "Payload electrical interface"
[gx12-connector-standard]: gx12-connector-standard.md "GX12 connector standard"
[flight-controller-hardware]: flight-controller-hardware.md "Flight controller hardware"
[imu-gyroscope]: imu-gyroscope.md "IMU and gyroscope"
[gnss-gps]: gnss-gps.md "GNSS and GPS"
[psb1-shield-board]: psb1-shield-board.md "PSB-1 payload shield board"
