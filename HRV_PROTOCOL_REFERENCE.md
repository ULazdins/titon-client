# Titon Aura-t WiFi HRV Control Protocol Reference

Based on decompiled Android application analysis. All messages are wrapped with `<stx>` and `<etx>` markers.

## Message Format

- **Command Structure**: `<stx>COMMAND[PARAMETERS]<etx>`
- **Response**: Messages are prefixed with device MAC addresses
- **Encoding**: Most parameters are 3-digit format (%03d) unless otherwise noted

---

## 1. FAN SPEED CONTROL (PWM Setting)

### Fan Speed Read Commands

- **C010** - Read Fan 1 Intake Speed (0-100%)
- **C110** - Read Fan 1 Exhaust Speed (0-100%)
- **C210** - Read Fan 2 Intake Speed (0-100%)
- **C310** - Read Fan 2 Exhaust Speed (0-100%)
- **C410** - Read Fan 3 Intake Speed (0-100%)
- **C510** - Read Fan 3 Exhaust Speed (0-100%)
- **C610** - Read Fan 4 Intake Speed (0-100%)
- **C710** - Read Fan 4 Exhaust Speed (0-100%)

### Fan Speed Set Commands

- **C0[0000nnnn]** - Set Fan 1 Intake to value nnnn (0-100%)
- **C1[0000nnnn]** - Set Fan 2 Intake to value nnnn (0-100%)
- **C2[0000nnnn]** - Set Fan 3 Intake to value nnnn (0-100%)
- **C3[0000nnnn]** - Set Fan 4 Intake to value nnnn (0-100%)
- **C4[0000nnnn]** - Set Fan 1 Exhaust to value nnnn (0-100%)
- **C5[0000nnnn]** - Set Fan 2 Exhaust to value nnnn (0-100%)
- **C6[0000nnnn]** - Set Fan 3 Exhaust to value nnnn (0-100%)
- **C7[0000nnnn]** - Set Fan 4 Exhaust to value nnnn (0-100%)

### Transaction Control

- **CS[nnn]** - Begin PWM transaction/edit mode (nnn = checksum)
- **CE[nnn]** - End PWM transaction/commit changes (nnn = checksum)

---

## 2. FAN SPEED PRESETS (Quick Select)

- **L[nnn]** - Get current fan speed preset (returns PS acknowledgment with current speed)
- **F1[nnn]** - Set Fan to Speed 1
- **F2[nnn]** - Set Fan to Speed 2
- **F3[nnn]** - Set Fan to Speed 3
- **F4[nnn]** - Set Fan to Speed 4

---

## 3. TIMER MANAGEMENT

### Timer Status

- **TM1** - Get timer status (returns TM1 with mode 0=off, 2=on)
- **TM0x** - Set timer to x (where x is the timer preset number)

---

## 4. FILTER CHANGE ACTIVITY

- **SF1[nnn]** - Filter 1 status/change (parameters unclear)
- **SF01[ddd]** - Set Filter 1, 3-digit parameter

---

## 5. HUMIDITY (PH) CONTROL

### Humidity Settings

- **SH1000** - Read humidity level (returns SH with value in format SH0nnnnn)
  - Response example: `SH065040` = 65% humidity
- **SH0[nnnn]** - Set humidity level to nn% (0-100%)
  - Value format: `SH0` + 3-digit percentage

---

## 6. SUMMER SETTINGS

### Summer Status

- **SS1000** - Get Summer Supply temperature (returns SS with value)
  - Response format: `SS nnn mmm` where nnn = temperature × 10, mmm = status
- **SE1000** - Get Summer Extract temperature threshold
  - Response format: `SE nnn mmm` where nnn = temperature × 10
- **SB10** - Get Summer Boost status (returns SB with disable/enable state)
  - Response example: `SB 0 033` = boost disabled

### Summer Configuration

- **SS0[nnn][mmm]** - Set Summer Supply temperature (nnn = temp×10, mmm = status)
- **SE0[nnn][mmm]** - Set Summer Extract temperature (nnn = temp×10, mmm = status)
- **SB[x][nnn]** - Set Summer Boost control (x = 0=disable/1=enable, nnn = checksum)

---

## 7. OTHER SETTINGS (Kitchen/Bathroom Timers)

### Kitchen Timer

- **SK10** - Read kitchen timer duration
- **SK0[xxx]** - Set kitchen timer to xxx minutes (0-100)

### Bathroom Timer

- **SW10** - Read bathroom timer duration
- **SW0[xxx]** - Set bathroom timer to xxx minutes (0-100)

---

## 8. SWITCH SELECTION (SwitchSelectActivity)

- **X010 to X410** - Query switch settings (4 switches available)
  - Response format: `X nnn mmm`where nnn = switch type code, mmm = room code

### Switch Type Codes

- **1** - Wet Room Boost
- **2** - Kitchen Boost
- **3** - Set Back
- **4** - Summer Boost Disable
- **5** - Fan Speed 4
- **6** - Fans Off (N/O - Normally Open)
- **7** - Fans Off (N/C - Normally Closed)
- **8** - Manual Summer Bypass

### Switch Configuration

- **X00[xx]** - Save switch settings for room xx (2-digit room code)

---

## 9. DATE/TIME SETTINGS

- **ST0[tttt]** - Set device time/date (format unclear, 4-digit parameter)
  - Device prompts: "Please confirm that you want to update the aura-t display time and day?"

---

## 10. SYSTEM CONTROL

- **Z[nnn]** - Acknowledge receipt/checksum validation (nnn = checksum)
- **L** - General status query (gets acknowledgment with <zck> marker for checksum)

---

## Message Wrapper Protocol

All commands follow this pattern:

```
<stx>COMMAND<etx>
```

Responses include:

```
:DAT|SOURCE_MAC|DEST_MAC|COMMAND_RESPONSE
```

Special markers:

- `<zck>` - Checksum marker (appears in responses requiring acknowledgment)
- `PS` - Positive/acknowledgment marker
- `<ack>` - Acknowledgment suffix in responses

---

## Checksum Calculation

The protocol uses XOR-based checksums:

- Most checksums are calculated as: `(byte1 ^ byte2 ^ byte3) ^ byte4`
- Bytes are typically the ASCII values of command characters
- Example for "CS": `C ^ S ^ checksum_byte = result`

---

## Notes

1. **Value Ranges**: Most percentage values (fan speeds, humidity) are 0-100
2. **Temperature Format**: Summer settings use temperature × 10 (e.g., 25.0°C = 250)
3. **XOR Protection**: Commands with parameters often XOR the value with checksum bytes for simple verification
4. **Room Codes**: 2-digit codes appear to identify different zones/rooms
5. **Status Polling**: The "L" command and timer queries use the <zck> marker for handshaking

---

## Implementation Notes for Home Assistant

Based on this protocol, the following entities can be exposed:

- **Select**: Fan speed preset (F1-F4)
- **Number**: Individual fan speeds (C0-C7), humidity, temperature setpoints
- **Switch**: Manual controls, summer boost
- **Sensor**: Current humidity %, fan speeds, timer status
- **Climate**: Summer mode with temperature control
