from math import e
import numpy as np

def HP_Power(T_ret, m_dot, c_f,T_sup, HE_eff=0.8):
    
    Qdot_HP = (HE_eff*(T_sup - T_ret)*m_dot*c_f)
        
    return Qdot_HP
    
    
def HP_COP(Tret, Thp_in):

    COP = 7.90471*e**(-0.024*(Tret - Thp_in))
    # if COP > 3.6:
    #     COP = 3.6

    return COP

def HP_COP_PWL(deltaT):

    return 7.90471 * np.exp(-0.024 * deltaT)

def HP_extra(T_amb, T_HPin, Power):
    
    COP = 7.90471*e**(-0.024*(T_HPin - T_amb))
    if COP > 3.6:
        COP = 3.6
    Q_dot = Power*COP

    # COP_air_registry.append(COP)
    return [Q_dot, COP]