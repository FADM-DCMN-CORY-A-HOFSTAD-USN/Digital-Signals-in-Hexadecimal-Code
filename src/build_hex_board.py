from skidl import *

# 1. Define the components (Mapping to your hand-drawn schematic)
# We add generic footprints so KiCad knows what 3D shape to use
serial_converter = Part('74xx', '74HC595', footprint='Package_SO:SOIC-16_3.9x9.9mm_P1.27mm') # Simulating SY10E445
hex_decoder = Part('4xxx', '4514', footprint='Package_DIP:DIP-24_W15.24mm')                 # CD4514B
ldo_regulator = Part('Regulator_Linear', 'AP131-15', footprint='Package_TO_SOT_SMD:SOT-23-5') # Simulating XC6602

# High-quality ceramic decoupling capacitors (TUF-grade requirement)
c_dec_1 = Part('Device', 'C', value='100nF', footprint='Capacitor_SMD:C_0805_2012Metric')
c_dec_2 = Part('Device', 'C', value='100nF', footprint='Capacitor_SMD:C_0805_2012Metric')
c_dec_3 = Part('Device', 'C', value='10uF', footprint='Capacitor_SMD:C_1206_3216Metric') # Bulk storage for the LDO

# 2. Define the Power Nets
gnd = Net('GND')
v_in = Net('5V_IN')
v_hex_logic = Net('0.5V_LOGIC') # The ultra-clean output from the LDO

# 3. Connect the Power Supply (XC6602)
v_in += ldo_regulator['IN'], c_dec_3[1]
gnd += ldo_regulator['GND'], c_dec_3[2], c_dec_1[2], c_dec_2[2]
v_hex_logic += ldo_regulator['OUT']

# 4. Connect Power to the Logic Chips and tie decoupling caps to them
v_hex_logic += serial_converter['VCC'], hex_decoder['VDD'], c_dec_1[1], c_dec_2[1]
gnd += serial_converter['GND'], hex_decoder['VSS']

# 5. Wire the Serial to Parallel Data Lines (Q0-Q3 mapping to your drawing)
data_bit_0 = Net('HEX_BIT_0')
data_bit_1 = Net('HEX_BIT_1')
data_bit_2 = Net('HEX_BIT_2')
data_bit_3 = Net('HEX_BIT_3')

data_bit_0 += serial_converter['QA'], hex_decoder['A0']
data_bit_1 += serial_converter['QB'], hex_decoder['A1']
data_bit_2 += serial_converter['QC'], hex_decoder['A2']
data_bit_3 += serial_converter['QD'], hex_decoder['A3']

# 6. Expose the 16 Hexadecimal output lines (S0-S15)
for i in range(16):
    hex_out_net = Net(f'HEX_OUT_{hex(i).upper().replace("0X", "")}')
    hex_out_net += hex_decoder[f'S{i}']

# Generate the KiCad Netlist
generate_netlist(file_='../hardware/netlists/hex_motherboard_v1.net')
print("TUF-Grade KiCad Netlist successfully generated in hardware/netlists/")
