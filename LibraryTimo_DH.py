from scipy.constants import sigma, pi
from math import exp, log

def surfaceTemperature_C(T_amb, G, v, Ts):
    

    # Radiative heat transfer coefficient
    RH = 70
    Tsky = ((0.62+0.056*(6.11*(RH/100)*exp(17.63*T_amb/(T_amb+243)))**0.5)**0.25)*T_amb
    epsilon = 0.25
    alpha_0 = 0.25

    # Wind forced convection
    if v < 5:
        h_conv = 5.7 + 3.8*v
    else:   # 5 <= v < 10
        h_conv = 6.47 + v**0.78

    h_r = epsilon*sigma*((Ts + 273.15)**2 + (Tsky + 273.15)**2)*((Ts + 273.15) + (Tsky + 273.15))
    h = h_conv + h_r
    
    delta_R = sigma*((Ts + 273.15)**4 - (Tsky + 273.15)**4)
    
    T_e = T_amb + alpha_0*G/h - epsilon*delta_R/h
    
    depth2boundary = 6
    k_soil = 1.19
    Ts_d = (0.0318*depth2boundary + 8.01768)
    Ts_new = (k_soil*Ts_d + depth2boundary*h*T_e)/(depth2boundary*h+k_soil)
    return Ts_new

def pipe_losses_C(T_pipe_in, L, T_amb, G, v, Ts):
    
    # Pipe parameters
    m_dot_pipe = 50
    epsilon = 0.25
    alpha_0 = 0.25
    k_soil = 1.19
    depth2boundary = 6
    c_f = 4200
    diameters = [0.13, 0.15, 0.40]        # [inner, outer, insulation]  

    k_f=0.6071
    k_tubes=[398, 0.038]
    H = 1

    density = 1000
    viscR =1.562e-5
    viscP = 0.8927e-6


    # Wind forced convection
    if v < 5:
        h_conv = 5.7 + 3.8*v
    else:   # 5 <= v < 10
        h_conv = 6.47 + v**0.78
    
    # Radiative heat transfer coefficient
    RH = 70
    Tsky = ((0.62+0.056*(6.11*(RH/100)*exp(17.63*T_amb/(T_amb+243)))**0.5)**0.25)*T_amb

    h_r = epsilon*sigma*((Ts + 273.15)**2 + (Tsky + 273.15)**2)*((Ts + 273.15) + (Tsky + 273.15))
    
    # Total heat transfer coefficient
    h = h_conv + h_r
    
    delta_R = sigma*((Ts + 273.15)**4 - (Tsky + 273.15)**4)

    T_e = T_amb + alpha_0*G/h - epsilon*delta_R/h
    
    Ts_d = (0.0318*depth2boundary + 8.01768)

    Ts_new = (k_soil*Ts_d + depth2boundary*h*T_e)/(depth2boundary*h+k_soil)



    # Pipe resistance

    

    Reynolds =  4*m_dot_pipe/(density*pi*diameters[0]*viscR)

    Prantl =  viscP/(k_f/(density*c_f))

    # Fluid conductivee heat transfer
    if Reynolds == 0:
        fcht =  2*k_f/diameters[0]
    elif Reynolds < 2300:
        fcht = 4.36*k_f/diameters[0]
    else:
        fcht = 0.023*k_f*(Reynolds**0.8)*(Prantl**0.4)/diameters[0]

    R_convective = 1/(pi*diameters[0]*fcht)

    R_conductive1 = log(diameters[1]/diameters[0])/(2*pi*k_tubes[0])
    R_conductive2 = log(diameters[2]/diameters[1])/(2*pi*k_tubes[1])
    R_conductive3 = log(2*H/diameters[2])/(2*pi*k_soil)
    

    R_total = R_convective + R_conductive1 + R_conductive2 + R_conductive3 

    T_out = Ts_new - (Ts_new - T_pipe_in)*exp(-L/(m_dot_pipe*c_f*R_total))
    
    Qdot_pipe = m_dot_pipe*c_f*(T_out - T_pipe_in)
    

                                                                                                                                           
    return [Qdot_pipe, T_out, Ts_new]