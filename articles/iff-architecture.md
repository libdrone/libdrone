---
id: iff-architecture
title: "IFF architecture"
version: 1.0.0
date: 2026-04-13
author: jsa
status: released
scope: libdrone
topic:
  - iff-deconfliction
personas:
  - 9.defense
  - 8.architect
  - 3.payload-dev
platform:
  - pro
  - bandit
  - ghost
lang: en
licence: CC BY-SA 4.0
---

## Summary

libdrone's IFF architecture is a layered system of five implementation levels,
each addressing different operational scenarios and observer capabilities.
The IR strobe (L1) is the most resilient — it works when everything else fails
and requires no infrastructure. Remote ID (L2) satisfies regulatory compliance
and civilian airspace management. ATAK/CoT integration (L3/L4) provides
tactical network presence visible to allied forces. A reserved hardware
interface (L6) positions libdrone for future allied IFF standards. The
ESP32-S3 companion board is the IFF intelligence layer: it bridges the
flight controller's internal protocol to the external tactical network,
making IFF capability a firmware function rather than a hardware redesign.

---

## Concept

### Why layers and not a single system

No single IFF technology covers all operational scenarios. IR strobe works
in daylight and darkness for NVG-equipped observers but produces no
machine-readable identification. Remote ID is machine-readable but limited
in range and broadcasts to anyone in range, including adversaries. CoT
provides precision tactical network integration but requires IP connectivity.
Classified military IFF provides the strongest identification but is
inaccessible to civilian operators.

Each layer adds coverage in the scenario where the layers above it fail. The
correct deployment is the maximum applicable layers for the operational context,
not a single chosen solution.

### The ESP32-S3 as the IFF intelligence layer

The flight controller (Matek H7A3-SLIM) generates all the data needed for IFF:
GPS position, attitude, battery state, flight mode, armed status. But it has
no WiFi, no TCP/IP stack, and no CPU headroom for application-layer protocol
translation. The ELRS radio link is a control channel, not a data network.

Only the ESP32-S3 sits at the intersection of the FC data bus and the IP
world. It receives MSP (Betaflight) or MAVLink (ArduPilot) from the FC via
companion UART, translates it to CoT XML, and multicasts via WiFi to the
tactical network. It simultaneously manages Remote ID broadcast and sensor
payload data upload. This is why ESP32-S3 is mandatory on Pro, Bandit, Ghost,
and Wing — without it, IFF capability above L2 does not exist.

### ArduPilot vs Betaflight IFF capability

**ArduPilot (Bandit, Ghost)**: natural ATAK advantage. MAVLink is a full
telemetry standard. ArduPilot streams HEARTBEAT, GLOBAL_POSITION_INT, and
ATTITUDE messages continuously. Any TAK server with a MAVLink plugin, or
an ESP32-S3 MAVLink → CoT bridge, consumes this directly. Mission state
(waypoints, auto modes) is visible to the GCS. Position quality is high
(EKF-fused GPS).

**Betaflight (Pro, Core)**: architecturally constrained. MSP is a
Betaflight-specific binary protocol with no GCS standard. An ESP32-S3
MSP → CoT bridge polls `MSP_RAW_GPS`, `MSP_ATTITUDE`, `MSP_ANALOG`, and
`MSP_STATUS_EX` to construct CoT events. Position fidelity is lower than
ArduPilot (no EKF). Mission state is not available. The gap is real but
closeable for situational awareness use cases: position and status arrive
in ATAK as a blue rotary-wing track.

---

## Reference

### IFF layer implementation status

| Layer | Technology | Platform support | Implementation status |
|---|---|---|---|
| L1 | IR strobe (850/940nm) | All | Available now — bolt-on |
| L2 | EU Remote ID | Pro, Bandit, Ghost | Module required (Dronetag Mini or equivalent) |
| L3 | ATAK / CoT (ArduPilot) | Bandit, Ghost | ESP32-S3 MAVLink→CoT bridge — firmware work required |
| L4 | ATAK / CoT (Betaflight) | Pro | ESP32-S3 MSP→CoT bridge — firmware work required |
| L5 | Classified mil IFF (Mode 4/5) | N/A | Not accessible to civilian operators |
| L6 | Future allied civilian IFF | All | GX12-7 Connector B GPIO pins reserved as IFF module interface |

### CoT event format (ESP32-S3 output)

    <event version="2.0" uid="LIBDRONE-PRO-001" type="a-f-A-M-F-Q"
          time="2026-04-13T10:00:00Z" start="..." stale="...">
      <point lat="50.0755" lon="14.4378" hae="350.0" ce="10" le="15"/>
      <detail>
        <contact callsign="LIBDRONE-PRO-001"/>
        <track speed="8.2" course="270"/>
        <remarks>BAT: 22.1V / 840mAh / Mode: ANGLE</remarks>
      </detail>
    </event>

CoT type `a-f-A-M-F-Q`: Atom / Friendly / Air / Military / Fixed-Wing / Quadrotor.
Appears in ATAK as a blue rotary-wing icon. Multicast address: 239.2.3.1:6969, UDP.

### Reserved IFF module interface (L6)

GX12-7 Connector B GPIO pins 3 and 4 are reserved for future IFF module:
- Physical: standard payload mast mount, ≤ 50 g
- Electrical: Connector B GPIO pins 3/4 for digital challenge/response
- Power: 3.3V or 5V from Connector B

When an allied civilian IFF standard emerges, the libdrone response is an
ESP32-S3 firmware update plus a new GX12 payload module — not a platform
redesign.

---

## Procedure

### Enabling ATAK CoT on Pro (Betaflight)

1. Ensure ESP32-S3 companion board is fitted and functional (OSD working).
2. Flash updated ESP32-S3 firmware with MSP → CoT bridge function enabled.
3. Configure in `lcm1_config.json`:
   - `callsign`: unique identifier for this drone
   - `tak_server_ip`: TAK server address or multicast (239.2.3.1)
   - `tak_server_port`: 6969 (multicast) or assigned port
   - `cot_update_rate_hz`: 1–2 (adequate for blue force tracking)
4. Power on drone outdoors. Verify GPS fix.
5. On ATAK tablet: confirm blue rotary-wing icon appears with drone's callsign.
6. Verify position tracks correctly as drone moves.
7. Confirm stale timeout: icon should disappear within 60 seconds if drone powers off.

### Enabling ATAK CoT on Bandit (ArduPilot)

1. Configure ArduPilot to stream MAVLink on UART6 at 57,600 baud.
2. Flash ESP32-S3 with MAVLink → CoT bridge firmware.
3. Configure callsign and TAK server as above.
4. Verify in ATAK — same procedure as Pro.

---

## Rationale

### Why the CoT bridge is firmware and not a separate hardware device

A separate hardware device adds mass, cost, connector complexity, and a
failure mode. The ESP32-S3 is already present on the platform, already
connected to the FC via companion UART, already managing WiFi. Adding CoT
output is a software function on existing hardware — the architecture that
exists already is the correct architecture for IFF integration. This is the
benefit of making ESP32-S3 mandatory across the platform family.

### Why the Core is excluded from the ESP32-S3 mandate

Core is a training platform. Adding IFF complexity to the education pathway
increases the configuration surface area without improving the training
outcome. The IFF mandate applies to operational platforms (Pro, Bandit, Ghost,
Wing) where deployment in security-sensitive environments is a use case. The
Core's use case is pilot and builder training — this is not compromised by
omitting IFF capability.

---

## Connections

requires:
  - [[threat-assessment]]
  - [[iff-layers]]
  - [[emissions-control]]
related:
  - [[remote-id-compliance]]
  - [[lcm1-spec]]
  - [[payload-software-protocol]]
  - [[flight-controller-hardware]]
  - [[esp32-s3-companion]]
leads_to:
  - [[operational-security]]
  - [[platform-selection]]
  - [[esp32-s3-companion]]


[threat-assessment]: threat-assessment.md "Threat assessment"
[iff-layers]: iff-layers.md "IFF layers"
[emissions-control]: emissions-control.md "Emissions control"
[remote-id-compliance]: remote-id-compliance.md "Remote ID compliance"
[lcm1-spec]: lcm1-spec.md "LCM-1 compute module"
[payload-software-protocol]: payload-software-protocol.md "Payload software protocol"
[flight-controller-hardware]: flight-controller-hardware.md "Flight controller hardware"
[esp32-s3-companion]: esp32-s3-companion.md "ESP32-S3 companion board"
[operational-security]: operational-security.md "Operational security"
[platform-selection]: platform-selection.md "Platform selection"
