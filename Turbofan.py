import numpy as np
import Constants
import adafruit_mcp3xxx.mcp3008 as MCP

MCP_PIN_IN = MCP.P0
channel = None


class TurboFan:

    def __init__(self, flight_level, fuel):
        self.Height = Constants.HEIGHT
        self.Temp = Constants.TEMP
        self.Speed = Constants.SPEED
        self.Pressure = Constants.PRESSURE
        self.conditions = {"temperature": self.Temp[flight_level],
                           "speed": self.Speed[flight_level],
                           "pressure": self.Pressure[flight_level]}
        self.fuel = fuel

    # Turbofan
    def engine_turbofan(self, output):
        # Output String
        out = ""
        # Initial Conditions
        m_f = self.fuel
        T_a = self.conditions['temperature']
        C_a = self.conditions['speed']
        P_a = self.conditions['pressure']
        # Variables/Constants
        Cp_a = 1.005  # kJ/kg
        g_a = 1.4
        B = 7.6  # Bypass
        n_inlet = 0.9
        PR_f = 1.75  # Fan
        n_fan = 0.8
        PR_1 = 1.2  # Axial
        n_axial = 0.8
        PR_2 = 2.5  # Centrifugal
        n_centri = 0.8
        P_loss = 0.05
        Cp_g = 1.148  # kJ/kg
        g_g = 1.333
        n_mech = 0.97
        n_LPT = 0.8
        n_HPT = 0.8
        n_nozzle = 0.95  # Cold and Hot Nozzle have same efficency

        # Inlet
        m_a = 5  # kg/s
        T_01 = T_a + (C_a) ** 2 / (2 * Cp_a * 1000)
        P_01 = P_a * (1 + n_inlet * (C_a ** 2) /
                      (2 * 1000 * Cp_a * T_a)) ** (g_a / (g_a - 1))

        # Fan
        P_02 = PR_f * P_01
        dt_1 = (T_01 / n_fan) * ((PR_1) ** ((g_a - 1) / g_a) - 1)
        T_02 = T_01 + dt_1
        m_c = (m_a * B) / (B + 1)
        m_h = (m_a) / (B + 1)

        W_fan = Cp_a * (dt_1)
        W_fan_dot = m_a * W_fan

        # Axial Compressor
        P_03 = PR_1 * P_02
        dt_2 = (T_02 / n_axial) * ((PR_1) ** ((g_a - 1) / g_a) - 1)
        T_03 = T_02 + dt_2

        W_axial = Cp_a * (dt_2)
        W_axial_dot = m_h * W_axial

        # Centrifugal Compressor
        P_04 = PR_2 * P_03
        dt_3 = (T_03 / n_centri) * ((PR_2) ** ((g_a - 1) / g_a) - 1)
        T_04 = T_03 + dt_3

        W_centri = Cp_a * (dt_3)
        W_centri_dot = m_h * W_centri

        # Combustion
        P_05 = P_04 * (1 - P_loss)
        LHV = 43100  # kJ/kg*K
        f = m_f / m_a
        m_hg = m_h + m_f
        T_05 = (f * LHV + Cp_a * T_04) / (Cp_g * (1 + f))

        # High Pressure Turbine (STOPPED HERE)
        W_HPT_dot = W_centri_dot / n_mech
        W_HPT = W_HPT_dot / m_hg

        dt_4 = W_HPT / Cp_g
        T_06 = T_05 - dt_4
        P_06 = P_05 * (1 - (1 / n_HPT) * (1 - (T_06 / T_05))) ** (g_g / (g_g - 1))

        # Low Pressure Turbine
        W_total_dot = W_axial_dot + W_fan_dot
        W_LPT_dot = W_total_dot / n_mech
        W_LPT = W_LPT_dot / m_hg

        dt_5 = W_LPT / Cp_g
        T_07 = T_06 - dt_5
        P_07 = P_06 * (1 - (1 / n_LPT) * (1 - (T_07 / T_06))) ** (g_g / (g_g - 1))

        # Cold Nozzle
        P_a_ratio = P_02 / P_a
        P_c_ratio = 1 / \
                    ((1 - (1 / n_nozzle) * (g_g - 1 / (g_g + 1))) ** (g_g / (g_g - 1)))
        if (P_a_ratio > P_c_ratio):  # Nozzle Choked
            Ma = 1
            P_9 = P_02 / P_c_ratio
            T_09 = T_02
            T_9 = T_09 / (1 + (g_g - 1) / 2)
            C_9 = 1 * np.sqrt(g_a * 287 * T_9)
            Nozzle_cold = 1
            # print('The Cold Nozzle is choked')
            # print(' ')
            out += 'The Cold Nozzle is choked\n'

        else:  # Nozzle Not Choked
            P_9 = P_a
            T_09 = T_02
            dt_9 = n_nozzle * T_09 * (1 - (P_9 / P_02)) ** ((g_g - 1) / g_g)
            T_9 = T_09 - dt_9
            C_9 = np.sqrt(2 * Cp_g * 1000 * dt_9)
            Nozzle_cold = 0
            # print('The Cold Nozzle is not choked')
            # print(' ')
            out += 'The Cold Nozzle is not choked\n'

        # Hot Nozzle
        P_a_ratio = P_07 / P_a
        P_c_ratio = 1 / \
                    ((1 - (1 / n_nozzle) * (g_g - 1 / (g_g + 1))) ** (g_g / (g_g - 1)))
        if (P_a_ratio > P_c_ratio):  # Nozzle Choked
            Ma = 1
            P_8 = P_07 / P_c_ratio
            T_08 = T_07
            T_8 = T_08 / (1 + (g_g - 1) / 2)
            C_8 = 1 * np.sqrt(g_a * 287 * T_8)
            Nozzle_hot = 1
            # print('The Hot Nozzle is choked')
            # print(' ')
            out += 'The Hot Nozzle is choked\n'

        else:  # Nozzle Not Choked
            P_8 = P_a
            T_08 = T_07
            dt_8 = n_nozzle * T_08 * (1 - (P_8 / P_07)) ** ((g_g - 1) / g_g)
            T_8 = T_08 - dt_8
            C_8 = np.sqrt(2 * Cp_g * 1000 * dt_8)
            Nozzle_hot = 0
            # print('The Hot Nozzle is not choked')
            # print(' ')
            out += 'The Hot Nozzle is not choked\n'

        # Thrust Hot Nozzle
        if (Nozzle_hot == 1):
            rho = P_8 / (287 * T_8)
            A = m_hg / (rho * C_8)
            F_hot = m_hg * C_8 - m_a * C_a + (P_8 - P_a) * A

        else:
            F_hot = m_hg * C_8 - m_a * C_a

        # Thrust Cold Nozzle
        if (Nozzle_cold == 1):  # Nozzle Choked
            rho = P_9 / (287 * T_9)
            A = m_c / (rho * C_9)
            F_cold = m_c * C_9 - m_a * C_a + (P_9 - P_a) * A

        else:  # Nozzle Not Choked
            F_cold = m_c * C_9

        # SFC
        F_total = F_hot + F_cold
        SFC = m_f / F_total
        # print('The total thrust is ' + str(F_total))
        # print(' ')
        out += f'The total thrust is {F_total}\n'

        # print('The SFC is ' + str(SFC))
        # print(' ')
        out += f'The SFC is {SFC}\n'

        # Propulsive Efficiency
        n_p = (F_total * C_a) / \
              (0.5 * ((m_c * C_9 ** 2 + m_hg * C_8 ** 2) - (m_a * C_a ** 2)))
        # print('The Propulsive Efficiency is ' + str(n_p))
        # print(' ')
        out += f'The Propulsive Efficiency is {n_p}\n'

        # Efficieny of the Cycle
        n_e = (0.5 * (m_c * C_9 ** 2 + m_hg * C_8 ** 2) - (m_a * C_a ** 2)) / (m_f * LHV)
        # print('The Efficieny of the Cycle is ' + str(n_e))
        # print(' ')
        out += f'The Efficiency of the Cycle is {n_e}\n'

        # Overall Efficiency
        n_0 = (F_total * C_a) / (m_f * LHV)
        # print('The Overall Efficiency ' + str(n_0))
        # print(' ')
        out += f'The Overall Efficiency {n_0}\n'
        #         print(f"FAN: {out}")

        output.update({'out': out})

    def get_conditions(self):
        return self.conditions['pressure'], self.conditions['speed'], self.conditions['temperature']
