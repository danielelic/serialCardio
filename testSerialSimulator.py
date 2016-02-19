# -*- coding: utf-8 -*-
from datetime import datetime
import time
import re
import fakeSerial as serial


class CRC8:
    def __init__(self):
        self.crcTable = (
            0x000, 0x091, 0x061, 0x0f0, 0x0c2, 0x053, 0x0a3, 0x032,
            0x0c7, 0x056, 0x0a6, 0x037, 0x005, 0x094, 0x064, 0x0f5,
            0x0cd, 0x05c, 0x0ac, 0x03d, 0x00f, 0x09e, 0x06e, 0x0ff,
            0x00a, 0x09b, 0x06b, 0x0fa, 0x0c8, 0x059, 0x0a9, 0x038,
            0x0d9, 0x048, 0x0b8, 0x029, 0x01b, 0x08a, 0x07a, 0x0eb,
            0x01e, 0x08f, 0x07f, 0x0ee, 0x0dc, 0x04d, 0x0bd, 0x02c,
            0x014, 0x085, 0x075, 0x0e4, 0x0d6, 0x047, 0x0b7, 0x026,
            0x0d3, 0x042, 0x0b2, 0x023, 0x011, 0x080, 0x070, 0x0e1,
            0x0f1, 0x060, 0x090, 0x001, 0x033, 0x0a2, 0x052, 0x0c3,
            0x036, 0x0a7, 0x057, 0x0c6, 0x0f4, 0x065, 0x095, 0x004,
            0x03c, 0x0ad, 0x05d, 0x0cc, 0x0fe, 0x06f, 0x09f, 0x00e,
            0x0fb, 0x06a, 0x09a, 0x00b, 0x039, 0x0a8, 0x058, 0x0c9,
            0x028, 0x0b9, 0x049, 0x0d8, 0x0ea, 0x07b, 0x08b, 0x01a,
            0x0ef, 0x07e, 0x08e, 0x01f, 0x02d, 0x0bc, 0x04c, 0x0dd,
            0x0e5, 0x074, 0x084, 0x015, 0x027, 0x0b6, 0x046, 0x0d7,
            0x022, 0x0b3, 0x043, 0x0d2, 0x0e0, 0x071, 0x081, 0x010,
            0x0a1, 0x030, 0x0c0, 0x051, 0x063, 0x0f2, 0x002, 0x093,
            0x066, 0x0f7, 0x007, 0x096, 0x0a4, 0x035, 0x0c5, 0x054,
            0x06c, 0x0fd, 0x00d, 0x09c, 0x0ae, 0x03f, 0x0cf, 0x05e,
            0x0ab, 0x03a, 0x0ca, 0x05b, 0x069, 0x0f8, 0x008, 0x099,
            0x078, 0x0e9, 0x019, 0x088, 0x0ba, 0x02b, 0x0db, 0x04a,
            0x0bf, 0x02e, 0x0de, 0x04f, 0x07d, 0x0ec, 0x01c, 0x08d,
            0x0b5, 0x024, 0x0d4, 0x045, 0x077, 0x0e6, 0x016, 0x087,
            0x072, 0x0e3, 0x013, 0x082, 0x0b0, 0x021, 0x0d1, 0x040,
            0x050, 0x0c1, 0x031, 0x0a0, 0x092, 0x003, 0x0f3, 0x062,
            0x097, 0x006, 0x0f6, 0x067, 0x055, 0x0c4, 0x034, 0x0a5,
            0x09d, 0x00c, 0x0fc, 0x06d, 0x05f, 0x0ce, 0x03e, 0x0af,
            0x05a, 0x0cb, 0x03b, 0x0aa, 0x098, 0x009, 0x0f9, 0x068,
            0x089, 0x018, 0x0e8, 0x079, 0x04b, 0x0da, 0x02a, 0x0bb,
            0x04e, 0x0df, 0x02f, 0x0be, 0x08c, 0x01d, 0x0ed, 0x07c,
            0x044, 0x0d5, 0x025, 0x0b4, 0x086, 0x017, 0x0e7, 0x076,
            0x083, 0x012, 0x0e2, 0x073, 0x041, 0x0d0, 0x020, 0x0b1)

    # def crc(self, msg):
    #     runningCRC = 0
    #     for c in msg:
    #         runningCRC = self.crcByte(runningCRC, int(c.encode('hex'), 16))
    #     return runningCRC


    def crc(self, msg):
        runningCRC = 0x00
        i = 0
        msg1 = ['09', '05', 'fd', 'fd', 'a5', '0a', '0f', '0d', '51', '4f', '6d', '68', 'aa', '50', '3a', '30', '39', 'd9']
        print msg1
        print('step', 'phase', 'runningCRC')
        for c in msg1:
            i += 1
            print(i, 'A', runningCRC)
            runningCRC = self.crcTable[runningCRC ^ int(c, 16)]
            print(i, 'B', runningCRC)
            runningCRC = runningCRC & 0xFF
            print(i, 'C', runningCRC)
        import sys
        sys.exit()
        return runningCRC


    def crcByte(self, oldCrc, byte):
        res = self.crcTable[oldCrc & 0xFF ^ byte & 0xFF]
        return res


class passport:
    def __init__(self, data):
        self.data = data
        self.ecghigh_0 = re.findall(r'.{1,2}', (bin(int(data[7 - 1], 16))[2:]).zfill(len(data[7 - 1]) * 4),
                                    re.DOTALL)  # aabbccdd
        self.ecghigh_1 = re.findall(r'.{1,2}', (bin(int(data[25 - 1], 16))[2:]).zfill(len(data[25 - 1]) * 4),
                                    re.DOTALL)  # aabbccdd
        self.ecghigh_2 = re.findall(r'.{1,2}', (bin(int(data[43 - 1], 16))[2:]).zfill(len(data[43 - 1]) * 4),
                                    re.DOTALL)  # aabbccdd
        self.ecghigh_3 = re.findall(r'.{1,2}', (bin(int(data[61 - 1], 16))[2:]).zfill(len(data[61 - 1]) * 4),
                                    re.DOTALL)  # aabbccdd

        self.ecg_00 = "{0}{1}".format(str(self.ecghigh_0[0]),
                                      (str(bin(int(data[3 - 1], 16))[2:]).zfill(len(data[3 - 1]) * 4)))  # aaaaaaaa
        self.ecg_01 = "{0}{1}".format(str(self.ecghigh_1[0]),
                                      (str(bin(int(data[21 - 1], 16))[2:]).zfill(len(data[21 - 1]) * 4)))  # aaaaaaaa
        self.ecg_02 = "{0}{1}".format(str(self.ecghigh_2[0]),
                                      (str(bin(int(data[39 - 1], 16))[2:]).zfill(len(data[39 - 1]) * 4)))  # aaaaaaaa
        self.ecg_03 = "{0}{1}".format(str(self.ecghigh_3[0]),
                                      (str(bin(int(data[57 - 1], 16))[2:]).zfill(len(data[57 - 1]) * 4)))  # aaaaaaaa
        self.ecg_04 = "{0}{1}".format(str(self.ecghigh_0[1]),
                                      (str(bin(int(data[4 - 1], 16))[2:]).zfill(len(data[4 - 1]) * 4)))  # bbbbbbbb
        self.ecg_05 = "{0}{1}".format(str(self.ecghigh_1[1]),
                                      (str(bin(int(data[22 - 1], 16))[2:]).zfill(len(data[22 - 1]) * 4)))  # bbbbbbbb
        self.ecg_06 = "{0}{1}".format(str(self.ecghigh_2[1]),
                                      (str(bin(int(data[40 - 1], 16))[2:]).zfill(len(data[40 - 1]) * 4)))  # bbbbbbbb
        self.ecg_07 = "{0}{1}".format(str(self.ecghigh_3[1]),
                                      (str(bin(int(data[58 - 1], 16))[2:]).zfill(len(data[58 - 1]) * 4)))  # bbbbbbbb
        self.ecg_08 = "{0}{1}".format(str(self.ecghigh_0[2]),
                                      (str(bin(int(data[5 - 1], 16))[2:]).zfill(len(data[5 - 1]) * 4)))  # cccccccc
        self.ecg_09 = "{0}{1}".format(str(self.ecghigh_1[2]),
                                      (str(bin(int(data[23 - 1], 16))[2:]).zfill(len(data[23 - 1]) * 4)))  # cccccccc
        self.ecg_10 = "{0}{1}".format(str(self.ecghigh_2[2]),
                                      (str(bin(int(data[41 - 1], 16))[2:]).zfill(len(data[41 - 1]) * 4)))  # cccccccc
        self.ecg_11 = "{0}{1}".format(str(self.ecghigh_3[2]),
                                      (str(bin(int(data[59 - 1], 16))[2:]).zfill(len(data[59 - 1]) * 4)))  # cccccccc
        self.ecg_12 = "{0}{1}".format(str(self.ecghigh_0[3]),
                                      (str(bin(int(data[6 - 1], 16))[2:]).zfill(len(data[6 - 1]) * 4)))  # dddddddd
        self.ecg_13 = "{0}{1}".format(str(self.ecghigh_1[3]),
                                      (str(bin(int(data[24 - 1], 16))[2:]).zfill(len(data[24 - 1]) * 4)))  # dddddddd
        self.ecg_14 = "{0}{1}".format(str(self.ecghigh_2[3]),
                                      (str(bin(int(data[42 - 1], 16))[2:]).zfill(len(data[42 - 1]) * 4)))  # dddddddd
        self.ecg_15 = "{0}{1}".format(str(self.ecghigh_3[3]),
                                      (str(bin(int(data[60 - 1], 16))[2:]).zfill(len(data[60 - 1]) * 4)))  # dddddddd

        self.pacerbits_0 = re.findall(r'.{1}', (bin(int(data[8 - 1], 16))[2:]).zfill(len(data[8 - 1]) * 4), re.DOTALL)[
                           0:4]  # abcdeeff
        self.pacerbits_1 = re.findall(r'.{1}', (bin(int(data[26 - 1], 16))[2:]).zfill(len(data[26 - 1]) * 4),
                                      re.DOTALL)[0:4]  # abcdeeff
        self.pacerbits_2 = re.findall(r'.{1}', (bin(int(data[44 - 1], 16))[2:]).zfill(len(data[44 - 1]) * 4),
                                      re.DOTALL)[0:4]  # abcdeeff
        self.pacerbits_3 = re.findall(r'.{1}', (bin(int(data[62 - 1], 16))[2:]).zfill(len(data[62 - 1]) * 4),
                                      re.DOTALL)[0:4]  # abcdeeff

        self.wawehigh_0 = re.findall(r'.{1,2}', (bin(int(data[8 - 1], 16))[2:]).zfill(len(data[8 - 1]) * 4),
                                     re.DOTALL)  # abcdeeff
        self.wawehigh_1 = re.findall(r'.{1,2}', (bin(int(data[26 - 1], 16))[2:]).zfill(len(data[26 - 1]) * 4),
                                     re.DOTALL)  # abcdeeff
        self.wawehigh_2 = re.findall(r'.{1,2}', (bin(int(data[44 - 1], 16))[2:]).zfill(len(data[44 - 1]) * 4),
                                     re.DOTALL)  # abcdeeff
        self.wawehigh_3 = re.findall(r'.{1,2}', (bin(int(data[62 - 1], 16))[2:]).zfill(len(data[62 - 1]) * 4),
                                     re.DOTALL)  # abcdeeff

        self.wawe_1_00 = "{0}{1}".format(str(self.wawehigh_0[2]),
                                         (str(bin(int(data[9 - 1], 16))[2:]).zfill(len(data[9 - 1]) * 4)))  # eeeeeeee
        self.wawe_1_02 = "{0}{1}".format(str(self.wawehigh_1[2]),
                                         (str(bin(int(data[27 - 1], 16))[2:]).zfill(len(data[27 - 1]) * 4)))  # eeeeeeee
        self.wawe_1_04 = "{0}{1}".format(str(self.wawehigh_2[2]),
                                         (str(bin(int(data[45 - 1], 16))[2:]).zfill(len(data[45 - 1]) * 4)))  # eeeeeeee
        self.wawe_1_06 = "{0}{1}".format(str(self.wawehigh_3[2]),
                                         (str(bin(int(data[63 - 1], 16))[2:]).zfill(len(data[63 - 1]) * 4)))  # eeeeeeee
        self.wawe_1_08 = "{0}{1}".format(str(self.wawehigh_0[3]),
                                         (str(bin(int(data[10 - 1], 16))[2:]).zfill(len(data[10 - 1]) * 4)))  # ffffffff
        self.wawe_1_10 = "{0}{1}".format(str(self.wawehigh_1[3]),
                                         (str(bin(int(data[28 - 1], 16))[2:]).zfill(len(data[28 - 1]) * 4)))  # ffffffff
        self.wawe_1_12 = "{0}{1}".format(str(self.wawehigh_2[3]),
                                         (str(bin(int(data[46 - 1], 16))[2:]).zfill(len(data[46 - 1]) * 4)))  # ffffffff
        self.wawe_1_14 = "{0}{1}".format(str(self.wawehigh_3[3]),
                                         (str(bin(int(data[64 - 1], 16))[2:]).zfill(len(data[64 - 1]) * 4)))  # ffffffff

        self.wawehigh_0 = re.findall(r'.{1,2}', (bin(int(data[15 - 1], 16))[2:]).zfill(len(data[15 - 1]) * 4),
                                     re.DOTALL)  # gghhiijj
        self.wawehigh_1 = re.findall(r'.{1,2}', (bin(int(data[33 - 1], 16))[2:]).zfill(len(data[33 - 1]) * 4),
                                     re.DOTALL)  # gghhiijj
        self.wawehigh_2 = re.findall(r'.{1,2}', (bin(int(data[51 - 1], 16))[2:]).zfill(len(data[51 - 1]) * 4),
                                     re.DOTALL)  # gghhiijj
        self.wawehigh_3 = re.findall(r'.{1,2}', (bin(int(data[69 - 1], 16))[2:]).zfill(len(data[69 - 1]) * 4),
                                     re.DOTALL)  # gghhiijj

        self.wawe_2_00 = "{0}{1}".format(str(self.wawehigh_0[0]),
                                         (str(bin(int(data[11 - 1], 16))[2:]).zfill(len(data[11 - 1]) * 4)))  # gggggggg
        self.wawe_2_02 = "{0}{1}".format(str(self.wawehigh_1[0]),
                                         (str(bin(int(data[29 - 1], 16))[2:]).zfill(len(data[29 - 1]) * 4)))  # gggggggg
        self.wawe_2_04 = "{0}{1}".format(str(self.wawehigh_2[0]),
                                         (str(bin(int(data[47 - 1], 16))[2:]).zfill(len(data[47 - 1]) * 4)))  # gggggggg
        self.wawe_2_06 = "{0}{1}".format(str(self.wawehigh_3[0]),
                                         (str(bin(int(data[65 - 1], 16))[2:]).zfill(len(data[65 - 1]) * 4)))  # gggggggg
        self.wawe_2_08 = "{0}{1}".format(str(self.wawehigh_0[1]),
                                         (str(bin(int(data[12 - 1], 16))[2:]).zfill(len(data[12 - 1]) * 4)))  # hhhhhhhh
        self.wawe_2_10 = "{0}{1}".format(str(self.wawehigh_1[1]),
                                         (str(bin(int(data[30 - 1], 16))[2:]).zfill(len(data[30 - 1]) * 4)))  # hhhhhhhh
        self.wawe_2_12 = "{0}{1}".format(str(self.wawehigh_2[1]),
                                         (str(bin(int(data[48 - 1], 16))[2:]).zfill(len(data[48 - 1]) * 4)))  # hhhhhhhh
        self.wawe_2_14 = "{0}{1}".format(str(self.wawehigh_3[1]),
                                         (str(bin(int(data[66 - 1], 16))[2:]).zfill(len(data[66 - 1]) * 4)))  # hhhhhhhh

        self.wawe_3_00 = "{0}{1}".format(str(self.wawehigh_0[2]),
                                         (str(bin(int(data[13 - 1], 16))[2:]).zfill(len(data[13 - 1]) * 4)))  # iiiiiiii
        self.wawe_3_02 = "{0}{1}".format(str(self.wawehigh_1[2]),
                                         (str(bin(int(data[31 - 1], 16))[2:]).zfill(len(data[31 - 1]) * 4)))  # iiiiiiii
        self.wawe_3_04 = "{0}{1}".format(str(self.wawehigh_2[2]),
                                         (str(bin(int(data[49 - 1], 16))[2:]).zfill(len(data[49 - 1]) * 4)))  # iiiiiiii
        self.wawe_3_06 = "{0}{1}".format(str(self.wawehigh_3[2]),
                                         (str(bin(int(data[67 - 1], 16))[2:]).zfill(len(data[67 - 1]) * 4)))  # iiiiiiii
        self.wawe_3_08 = "{0}{1}".format(str(self.wawehigh_0[3]),
                                         (str(bin(int(data[14 - 1], 16))[2:]).zfill(len(data[14 - 1]) * 4)))  # jjjjjjjj
        self.wawe_3_10 = "{0}{1}".format(str(self.wawehigh_1[3]),
                                         (str(bin(int(data[32 - 1], 16))[2:]).zfill(len(data[32 - 1]) * 4)))  # jjjjjjjj
        self.wawe_3_12 = "{0}{1}".format(str(self.wawehigh_2[3]),
                                         (str(bin(int(data[50 - 1], 16))[2:]).zfill(len(data[50 - 1]) * 4)))  # jjjjjjjj
        self.wawe_3_14 = "{0}{1}".format(str(self.wawehigh_3[3]),
                                         (str(bin(int(data[68 - 1], 16))[2:]).zfill(len(data[68 - 1]) * 4)))  # jjjjjjjj

        self.crc_0 = (bin(int(data[20 - 1], 16))[2:]).zfill(len(data[20 - 1]) * 4)  # xxxxxxxx
        self.crc_1 = (bin(int(data[38 - 1], 16))[2:]).zfill(len(data[38 - 1]) * 4)  # xxxxxxxx
        self.crc_2 = (bin(int(data[56 - 1], 16))[2:]).zfill(len(data[56 - 1]) * 4)  # xxxxxxxx
        self.crc_3 = (bin(int(data[74 - 1], 16))[2:]).zfill(len(data[74 - 1]) * 4)  # xxxxxxxx

    def printData(self):
        crcTest = CRC8().crc(self.data[3 - 1:21 - 1])
        if (crcTest == 0):
            currenttime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
            print(int(self.ecg_00, 2), currenttime)
            print(int(self.ecg_01, 2), currenttime)
            print(int(self.ecg_02, 2), currenttime)
            print(int(self.ecg_03, 2), currenttime)
            print(int(self.ecg_04, 2), currenttime)
            print(int(self.ecg_05, 2), currenttime)
            print(int(self.ecg_06, 2), currenttime)
            print(int(self.ecg_07, 2), currenttime)
            print(int(self.ecg_08, 2), currenttime)
            print(int(self.ecg_09, 2), currenttime)
            print(int(self.ecg_10, 2), currenttime)
            print(int(self.ecg_11, 2), currenttime)
            print(int(self.ecg_12, 2), currenttime)
            print(int(self.ecg_13, 2), currenttime)
            print(int(self.ecg_14, 2), currenttime)
            print(int(self.ecg_15, 2), currenttime)


def run():
    strPort = '/dev/ttyUSB0'
    ser = serial.Serial(strPort, 9600, timeout=1)
    x_aa = ser.read()  # read one byte
    while x_aa != "":
        x_aa = ser.read()  # read one byte
        if (x_aa.encode("hex") == 'aa'):
            x_55 = ser.read()
            if (x_55.encode("hex") == '55'):
                x = x_aa + x_55 + ser.read(72)
                data = re.findall(r'.{1,2}', x.encode('hex'), re.DOTALL)
                dataPass = passport(data)
                dataPass.printData()
                time.sleep(.008)  # fix when serial is real connect to passport
    ser.close()


run()
