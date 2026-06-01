---
id: sitl-simulation
title: "SITL simulation"
version: 1.0.0
date: 2026-04-15
author: jsa
status: released
scope: generic
topic:
  - software-stack
personas:
  - 1.builder
  - 2.operator
  - 8.architect
platform:
  - bandit
  - ghost
  - wing
lang: en
licence: CC BY-SA 4.0
---

## Summary

Software In The Loop (SITL) simulation runs ArduPilot firmware on a desktop
computer rather than on flight controller hardware, connected to a physics
simulator that models the aircraft's dynamics. The flight controller behaves
identically to a real build — it runs the same PID loop, EKF, and failsafe
logic, responds to the same QGroundControl ground station, and executes the
same `.plan` mission files — but the aircraft exists only in software. For
libdrone ArduPilot platforms (Bandit, Ghost, Wing), SITL is the mandatory
validation step between writing a mission and flying it on hardware. A mission
that fails in SITL will fail on the aircraft. A mission that passes SITL
has eliminated the largest class of preventable first-flight failures.

---

## Concept

### What SITL actually simulates

ArduPilot SITL consists of two components running concurrently: the ArduPilot
firmware binary compiled for the host machine (not for the STM32), and a
physics simulator (typically ArduPilot's built-in SITL simulator, or
Gazebo/RealFlight for higher fidelity) that models aerodynamics, gravity,
GPS signal, and sensor noise.

The firmware binary receives simulated sensor data — accelerometer, gyroscope,
GPS position, barometer altitude — and outputs simulated motor commands. The
physics simulator advances the aircraft's virtual position and attitude based
on those motor commands and feeds the result back as the next sensor reading.
This loop runs faster than real time on modern hardware, making a 10-minute
survey mission testable in 2–3 minutes.

From QGroundControl's perspective, a SITL session is indistinguishable from
a real flight: it connects via UDP MAVLink, shows the same HUD, receives
the same telemetry stream, and accepts the same mission upload commands.
This is the primary value: the entire operator workflow — mission planning,
upload, mode switching, monitoring, failsafe verification — is exercised before
the first hardware flight.

### What SITL does not simulate

SITL is a control system and mission logic validator, not a hardware validator.
It cannot detect:
- Incorrect ELRS MAVLink configuration (SERIAL2_PROTOCOL error)
- Compass interference from motors at the actual PCB layout
- Mechanical resonance at the specific build's natural frequencies
- Battery voltage sag under real load
- GPS multipath at the deployment site

These require a real build and bench/hover testing. SITL and hardware testing
are complementary, not alternative.

### The ArduPilot SITL test workflow for Bandit

The standard pre-deployment SITL sequence validates three things in order:

1. **Mission logic**: does the `.plan` file execute correctly? Do all
   waypoints load, does the altitude profile make sense, does the mission
   end with RTL or Land?
2. **Failsafe behaviour**: what does the aircraft do when RC signal is
   removed mid-mission? When a simulated battery critical event fires?
3. **Mode transitions**: can the operator switch from Auto to Loiter and
   back without losing the mission state?

---

## Reference

### SITL setup for ArduPilot Copter (Bandit/Ghost)

**Prerequisites:** Ubuntu 20.04 or 22.04, Python 3.8+, git.

# Clone ArduPilot and install dependencies
      git clone https://github.com/ArduPilot/ardupilot.git
      cd ardupilot
      git submodule update --init --recursive
      Tools/environment_install/install-prereqs-ubuntu.sh -y
      . ~/.profile

# Build SITL for Copter
      ./waf configure --board sitl
      ./waf copter

# Launch SITL with Copter (replaces real MatekH7A3 FC)
      sim_vehicle.py -v ArduCopter --console --map

QGroundControl detects the SITL instance via UDP on port 14550 automatically.

**For ArduPlane (Wing):**
      sim_vehicle.py -v ArduPlane --console --map

### Standard SITL mission test sequence

1. Launch SITL → connect QGroundControl
2. Upload survey `.plan` from libdrone missions directory
3. In QGC: verify mission renders correctly on map, RTL altitude set
4. Arm (SITL accepts arm with no pre-arm checks by default)
5. Switch to AUTO → observe aircraft execute mission in QGC map view
6. Mid-mission: disconnect QGC UDP connection → verify RC failsafe triggers
   RTL (SITL simulates signal loss when GCS disconnects)
7. Reconnect → verify aircraft continues to mission if GCS link restored
8. Allow mission to complete → verify RTL and land

**Pass criteria:** mission executes without deviation; failsafe RTL triggers
within 2 seconds of signal loss; aircraft returns to within 5m of home.

---

## Procedure

### Test a new survey mission before first hardware flight

1. Export `.plan` file from QGroundControl after planning
2. Launch SITL: `sim_vehicle.py -v ArduCopter --console --map`
3. Connect QGC → upload `.plan` → verify in Plan view
4. Set simulated wind: `param set SIM_WIND_SPD 5` (test at expected
   field conditions)
5. Execute mission in AUTO mode — watch full flight in QGC map
6. Confirm all waypoints reached, final RTL completes, DISARM on landing
7. If any anomaly — altitude deviation >10m, mission abort, unexpected
   mode change — fix the `.plan` before flying hardware

---

## Rationale

SITL was identified as a required pre-flight step for all libdrone ArduPilot
missions in the Bandit specification (§15) specifically because mission logic
errors are silent until the aircraft is airborne. A survey grid that was
planned at 50m AGL but accidentally set to 50m AMSL will fly at the wrong
altitude relative to terrain — impossible to detect by inspecting the `.plan`
file in a text editor, trivially visible in a SITL run where the QGC altitude
indicator shows an unexpected value. The 15-minute SITL validation step
eliminates this class of error entirely.

---

## Connections

requires:
  - [[ardupilot-copter]]
  - [[qgroundcontrol]]
related:
  - [[ardupilot-commissioning]]
  - [[ardupilot-flight-modes]]
  - [[ardupilot-failsafe]]
  - [[bandit-variant]]
  - [[wing-variant]]
leads_to:
  - [[maiden-flight]]
  - [[ardupilot-autotune]]


[ardupilot-copter]: ardupilot-copter.md "ArduPilot Copter"
[qgroundcontrol]: qgroundcontrol.md "QGroundControl"
[ardupilot-commissioning]: ardupilot-commissioning.md "ArduPilot commissioning"
[ardupilot-flight-modes]: ardupilot-flight-modes.md "ArduPilot flight modes"
[ardupilot-failsafe]: ardupilot-failsafe.md "ArduPilot failsafe"
[bandit-variant]: bandit-variant.md "Bandit variant"
[wing-variant]: wing-variant.md "Wing variant"
[maiden-flight]: maiden-flight.md "Maiden flight"
[ardupilot-autotune]: ardupilot-autotune.md "ArduPilot Autotune"
