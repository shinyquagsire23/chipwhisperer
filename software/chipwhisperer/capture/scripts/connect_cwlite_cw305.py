from chipwhisperer.capture.targets.CW305 import CW305
import chipwhisperer as cw

bitstream_file = r"C:\chipwhisperer\hardware\victims\cw305_artixtarget\fpga\vivado_examples" \
        r"\aes128_verilog\aes128_verilog.runs\impl_35t\cw305_top.bit"

scope = cw.scope()
self.scope = scope

target = cw.target(scope, type=CW305, bsfile=bitstream_file, force=False)
self.target = target