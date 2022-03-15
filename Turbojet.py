import numpy as np
import Constants


class Turbojet:
    def __init__(self, flight_level, fuel):
        self.Temp = Constants.TEMP
        self.Speed = Constants.SPEED
        self.Pressure = Constants.PRESSURE
        self.conditions = {"temperature": self.Temp[flight_level],
                           "speed": self.Speed[flight_level],
                           "pressure": self.Pressure[flight_level]}
        self.fuel = fuel

    # Going throughout the engine
    def engine_turbojet(self, output):
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
        n_inlet = 0.9
        pr_1 = 1.2  # Axial
        n_axial = 0.8
        pr_2 = 2.5  # Centrifugal
        n_centri = 0.8
        P_loss = 0.05
        Cp_g = 1.148  # kJ/kg
        g_g = 1.333
        n_mech = 0.97
        n_turbine = 0.8
        n_nozzle = 0.95
        # Inlet
        m_a = 5
        T_01 = T_a + (C_a) ** 2 / (2 * Cp_a * 1000)
        P_01 = P_a * (1 + n_inlet * (C_a ** 2) /
                      (2 * 1000 * Cp_a * T_a)) ** (g_a / (g_a - 1))

        # Axial Compressor
        P_02 = pr_1 * P_01
        dt_1 = (T_01 / n_axial) * ((pr_1) ** ((g_a - 1) / g_a) - 1)
        T_02 = T_01 + dt_1

        W_axial = Cp_a * (dt_1)
        W_axial_dot = m_a * W_axial

        # Centrifugal Compressor
        P_03 = pr_2 * P_02
        dt_2 = (T_02 / n_centri) * ((pr_2) ** ((g_a - 1) / g_a) - 1)
        T_03 = T_02 + dt_2

        W_centri = Cp_a * (dt_2)
        W_centri_dot = m_a * W_centri

        # Combustion
        P_04 = P_03 * (1 - P_loss)
        lhv = 43100  # kJ/kg*K
        f = m_f / m_a
        m_g = m_a + m_f
        T_04 = (f * lhv + Cp_a * T_03) / (Cp_g * (1 + f))

        # Axial Turbine
        W_total_dot = W_axial_dot + W_centri_dot
        W_turbine_dot = W_total_dot / n_mech
        W_turbine = W_turbine_dot / m_g

        dt_3 = W_turbine / Cp_g
        T_05 = T_04 - dt_3
        P_05 = P_04 * (1 - (1 / n_turbine) *
                       (1 - (T_05 / T_04))) ** (g_g / (g_g - 1))

        # Nozzle
        P_a_ratio = P_05 / P_a
        P_c_ratio = 1 / \
                    ((1 - (1 / n_nozzle) * (g_g - 1 / (g_g + 1))) ** (g_g / (g_g - 1)))
        if (P_a_ratio > P_c_ratio):  # Nozzle Choked
            Ma = 1
            P_6 = P_05 / P_c_ratio
            T_06 = T_05
            T_6 = T_06 / (1 + (g_g - 1) / 2)
            C_6 = 1 * np.sqrt(g_a * 287 * T_6)
            Nozzle = 1
            #print('The Nozzle is choked')
            #print(' ')
            out += 'The Nozzle is choked\n'
        else:  # Nozzle Not Choked
            P_6 = P_a
            T_06 = T_05
            dt_4 = n_nozzle * T_05 * (1 - (P_6 / P_05)) ** ((g_g - 1) / g_g)
            T_6 = T_06 - dt_4
            C_6 = np.sqrt(2 * Cp_g * 1000 * dt_4)
            Nozzle = 0
            #print('The Nozzle is not choked')
            #print(' ')
            out += 'The Nozzle is not choked\n'

        # Propulsion
        if (Nozzle == 1):
            rho = P_6 / (287 * T_6)
            A = m_g / (rho * C_6)
            Thrust = m_g * C_6 - m_a * C_a + (P_6 - P_a) * A
            Thrust_specific = Thrust / m_a
        else:
            Thrust = m_g * C_6 - m_a * C_a
            Thrust_specific = Thrust / m_a

        #print('The total thrust is ' + str(Thrust))
        #print(' ')
        out += f'The total thrust is {Thrust}\n'
        # SFC
        SFC = m_f / Thrust
        #print('The SFC is ' + str(SFC))
        #print(' ')
        out += f'The SFC is {SFC}\n'
        # Propulsive Efficiency
        n_p = (Thrust * C_a) / (0.5 * ((m_g * C_6 ** 2) - (m_a * C_a ** 2)))
        #print('The Propulsive Efficiency is ' + str(n_p))
        #print(' ')
        out += f'The Propulsive Efficiency is {n_p}\n'
        # Efficieny of the Cycle
        n_e = (0.5 * ((m_g * C_6 ** 2) - (m_a * C_a ** 2))) / (m_f * lhv)
        #print('The Efficieny of the Cycle is ' + str(n_e))
        #print(' ')
        out += f'The Efficiency of the Cycle is {n_e}\n'
        # Overall Efficiency
        n_0 = (Thrust * C_a) / (m_f * lhv)
        #print('The Overall Efficiency ' + str(n_0))
        #print(' ')
        out += f'The Overall Efficiency {n_0}\n'
#         print(f"JET: {out}")
        output.update({'out':out})

    def get_conditions(self):
        return self.conditions['pressure'], self.conditions['speed'], self.conditions['temperature']
