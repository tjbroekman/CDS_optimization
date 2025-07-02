from scipy.constants import Stefan_Boltzmann as sigma
from math import sin, cos, radians, exp, pi

def PVT_model(T_amb, G, v, T_f_in, T_glass_0, T_PV_0, T_a_0, T_f_0, dt, PVT_active):

    
    A_collector = 1.77

    A_glass = A_collector
    A_PV = A_collector
    A_a = A_collector
    A_t = 1.48

    D_tube = 0.009

    tilt = 0

    rho_glass = 2200
    rho_PV = 2330
    rho_a = 2699
    rho_f = 1050

    L_glass = 0.0032
    L_gap = 0.02
    L_PV_glass = 0.003
    L_PV_EVA = 0.0005
    L_PV_tedlar = 0.0001
    L_PV = L_PV_glass + L_PV_EVA + L_PV_tedlar

    L_a = 0.005
    L_ins = 0.04

    if PVT_active:
        m_f_dot_PVT=0.029085
    else:
        m_f_dot_PVT = 0

    
        
    k_glass = 1.8
    k_air = 0.024
    k_PV_glass = 1.8
    k_PV_EVA = 0.35
    k_PV_tedlar = 0.2
    
    k_f = 0.6071
    k_ins = 0.035

    c_glass = 670
    c_pv = 900
    c_a = 800
    c_f = 3800

    alpha_glass = 0.9
    alpha_PV = 0.9
    
    epsilon_glass = 0.9
    epsilon_PV = 0.96
    tau_glass = 0.1

    eff_HE = 0.8
    eff_STC = 0.184

    m_glass = rho_glass*A_glass*L_glass
    m_PV = rho_PV*A_PV*L_PV
    m_a = rho_a*A_a*L_a
    m_f = 0.65*rho_f/1000  # N_tubes*rho_f*(0.125*pi*D_tube**2)*Len_collector

    # Wind forced convection (checked and correct)
    if v < 5:
        h_glass_conv = 5.7 + 3.8*v
    else:   # 5 <= v < 10
        h_glass_conv = 6.47 + v**0.78

    


    # Sky temperature  (checked and correct, values make sense)
    RH = 70
    Tsky = ((0.62+0.056*(6.11*(RH/100)*exp(17.63*T_amb/(T_amb+243)))**0.5)**0.25)*T_amb
    

    # radiant heat transfer coefficient glass (checked and correct, values make sense)
    h_glass_r = epsilon_glass*sigma*((T_glass_0 + 273.15)**2 + (Tsky + 273.15)**2)*((T_glass_0 + 273.15) + (Tsky) + 273.15)
    

    # Conductive heat transfer coefficient (checked and constant)
    L = [L_PV_glass, L_PV_EVA]
    k = [k_PV_glass, k_PV_EVA]
    CHTC = sum([L[i]/k[i] for i in range(len(k))])**-1
    

    # Air gap convection
    beta=3.4e-3
    visc=1.562e-5
    k=0.024
    density=1.184
    c=1005
    g=9.8


    Rayleigh = (g*beta*(abs(T_glass_0 - T_PV_0))*L_gap**3)/(visc*(k/(density*c)))
    
    Nusselt = 1 + 1.44*(1 - 1708/(Rayleigh*cos(radians(tilt))))*(1 - 1708*(sin(radians(1.6*tilt))**1.6)/(Rayleigh*cos(radians(tilt))))*((Rayleigh*cos(radians(tilt))/5830)**(1/3)-1)
    
    AGC = Nusselt*k_air/L_gap


    h_gap = (CHTC**-1 + AGC**-1)**-1
   

    # Radiative heat transfer coefficient two plates
    h_glassPV_r = sigma*((T_glass_0 + 273.15)**2 + (T_PV_0 + 273.15)**2)*((T_glass_0 + 273.15) + (T_PV_0 + 273.15))*(epsilon_glass**-1 + epsilon_PV**-1 - 1)**-1
   


    # Conductive heat transfer coefficient
    L = [L_PV_EVA, L_PV_tedlar]
    k = [k_PV_EVA, k_PV_tedlar]

    h_PVa_cond = sum([L[i]/k[i] for i in range(len(k))])**-1
   

    density=1000
    visc=1.562e-5

    Reynolds = 4*m_f_dot_PVT/(density*pi*D_tube*visc)



    visc=0.8927e-6
    k=0.6071
    c=4200
    Prandlt = visc/(k/(density*c))

    if Reynolds == 0:
        h_af = 2*k_f/D_tube
    elif Reynolds < 2300:
        h_af = 4.36*k_f/D_tube
    else:
        h_af = 0.023*k_f*(Reynolds**0.8)*(Prandlt**0.4)/D_tube

    

    

    # Conductive heat transfer coefficient
    L = [L_ins]
    k = [k_ins]

    h_a_cond = sum([L[i]/k[i] for i in range(len(k))])**-1
   

    T_ref = 25
    beta_PV = -0.00365
    PV_efficiency = eff_STC*(1 - beta_PV*(T_PV_0 - T_ref))
    

    T_glass = T_glass_0 + dt*A_glass/(m_glass*c_glass)*(h_glass_conv*(T_amb - T_glass_0) + h_glass_r*(Tsky - T_glass_0) + h_gap*(T_PV_0 - T_glass_0) + h_glassPV_r*(T_PV_0 - T_glass_0) + alpha_glass*G)
    
    T_PV = T_PV_0 + (A_PV*dt/(m_PV*c_pv))*(h_gap*(T_glass_0 - T_PV_0) + h_glassPV_r*(T_glass_0 - T_PV_0) + h_PVa_cond*(T_a_0 - T_PV_0) + alpha_PV*tau_glass*G*(1 - PV_efficiency))
    
    T_a = T_a_0 + (dt/(m_a*c_a))*(A_a*h_PVa_cond*(T_PV_0 - T_a_0) + h_af*A_t*(T_f_0 - T_a_0) + h_a_cond*A_a*(T_amb - T_a_0))
    
    T_f = T_f_0 + (dt/(m_f*c_f))*(h_af*A_t*(T_a_0 - T_f_0) + 2*m_f_dot_PVT*c_f*(T_f_in - T_f_0))
   

    return [T_glass, T_PV, T_a, T_f, m_f_dot_PVT]


    
def PV_efficiency(T_PV, n_STC, beta_PV=-0.00365, T_ref=25):
    return n_STC*(1 - beta_PV*(T_PV - T_ref))

def PV_out(T_PV, G, A_PV=1.77, n_STC=0.2031):
   return PV_efficiency(T_PV, n_STC)*G*A_PV