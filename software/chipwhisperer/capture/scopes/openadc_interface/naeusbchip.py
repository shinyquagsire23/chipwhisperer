# Authors: Colin O'Flynn
#
# Find this and more at newae.com - this file is part of the chipwhisperer
# project, http://www.assembla.com/spaces/chipwhisperer
#
#    This file is part of chipwhisperer.
#
#    chipwhisperer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    chipwhisperer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with chipwhisperer.  If not, see <http://www.gnu.org/licenses/>.
#=================================================
import logging
import sys
import traceback
# import chipwhisperer.capture.scopes._qt as openadc_qt
from .. import _qt as openadc_qt
from chipwhisperer.capture.scopes.cwhardware.ChipWhispererFWLoader import CWLite_Loader, CW1200_Loader
from chipwhisperer.capture.scopes.cwhardware.ChipWhispererFWLoader import FWLoaderConfig
from chipwhisperer.common.utils.util import DictType, camel_case_deprecated

try:
    from chipwhisperer.capture.scopes.cwhardware import ChipWhispererLite as CWL
except ImportError:
    CWL = None
    logging.error("Could not import ChipWhispererLite\n" + traceback.format_exc())

try:
    import usb
except ImportError:
    usb = None
    logging.error("Could not import USB\n" + traceback.format_exc())


class OpenADCInterface_NAEUSBChip(object):
    _name = "NewAE USB (CWLite/CW1200)"

    def __init__(self, oadcInstance):
        self.ser = None
        self.dev = None
        self.scope = None
        self.last_id = None

        if (openadc_qt is None) or (usb is None):
            missingInfo = ""
            if openadc_qt is None:
                missingInfo += "openadc.qt "
            if usb is None:
                missingInfo += " usb"
            raise ImportError("Needed imports for ChipWhisperer missing: %s" % missingInfo)
        else:
            self.cwFirmwareConfig = {
                0xACE2:FWLoaderConfig(CWLite_Loader()),
                0xACE3:FWLoaderConfig(CW1200_Loader())
            }
            self.scope = oadcInstance

    def con(self, sn=None):
        if self.ser is None:
            self.dev = CWL.CWLiteUSB()

            nae_products = [0xACE2, 0xACE3]
            #possible_sn = self.dev.get_possible_devices(nae_products)
            #handle = self.dev.get_possible_devices(nae_products)
            self.dev.con(idProduct=nae_products, serial_number=sn)
            self.cwFirmwareConfig[0xACE2].setInterface(self.dev.fpga)
            try:
                self.cwFirmwareConfig[0xACE2].loadFPGA()
            except:
                self.dev.dis()
                self.dev.usbdev.close()
                raise
            self.ser = self.dev.usbdev()


    def dis(self):
        if self.ser is not None:
            self.getFWConfig().setInterface(None)
            self.scope.close()
            self.ser.close()
            self.ser = None
        if self.dev is not None:
            self.dev.dis()
            self.dev = None

    def __del__(self):
        if self.ser is not None:
            self.ser.close()

    def getFWConfig(self):
        try:
            return self.cwFirmwareConfig[self.last_id]
        except KeyError as e:
            return FWLoaderConfig(CWLite_Loader())

    def get_name(self):
        return self._name

    getName = camel_case_deprecated(get_name)
