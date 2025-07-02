import gurobipy as gp
import math

def massCapacity(houseType):

    # Air
    c_air = 1005.4               # Specific heat of air at 273 K [J/kgK]
    airDensity = 1.025           # Densiity of air at 293 K [kg/m^3]

    if houseType == 1:
        windows_area = 213
        lenHouse = 35             # House length [m]
        widHouse = 25             # House width [m]
        htHouse = 6               # House height [m]
        roof_Area = 874

    if houseType == 2:
        windows_area = 400
        lenHouse = 50             # House length [m]
        widHouse = 30             # House width [m]
        htHouse = 7               # House height [m]
        roof_Area = 1504

    if houseType == 3:
        windows_area = 647
        lenHouse = 70             # House length [m]
        widHouse = 40             # House width [m]
        htHouse = 8               # House height [m]
        roof_Area = 3130

    # Walls (concrete)
    LWall = 0.25           # Wall thickness [m]
    wallDensity = 2400           # Density [kg/m^3]
    c_wall = 750            # Specific heat [J/kgK]
    walls_area = 2*(lenHouse + widHouse) * htHouse - windows_area
    m_walls = wallDensity * walls_area * LWall

    LWindow = 0.004                 # Thickness of a single window pane [m]
    windowDensity = 2500            # Density of glass [kg/m^3]
    c_window = 840                  # Specific heat of glass [J/kgK]

    m_windows = windowDensity * windows_area * LWindow
    
    # Roof (glass fiber)
    LRoof = 0.2            # Roof thickness [m]
    roofDensity = 2440           # Density of glass fiber [kg/m^3]
    c_roof = 835            # Specific heat of glass fiber [J/kgK]
    m_roof = roofDensity * roof_Area * LRoof
    
    m_air = airDensity * lenHouse * widHouse * htHouse

    mc_T = m_air*c_air + m_roof*c_roof + m_windows*c_window + m_walls*c_wall

    return mc_T

def House_Thermal_losses(houseType, T_0_in, T_amb):

    #############################   Parameters ################################

    U = 1
    C_stack=0.015
    C_wind=0.0012
    N_bedrooms=1

    # Convective heat transfer coefficients [W/m^2K]
    h_air_wall = 0.9             # Indoor air -> walls, scaled to R-value of a C-label house
    h_wall_atm = 0.9             # Walls -> atmosphere, scaled to R-value of a C-label house
    h_air_window = 25            # Indoor air -> windows
    h_window_atm = 32            # Windows -> atmosphere
    h_air_roof = 12              # Indoor air -> roof
    h_roof_atm = 38              # Roof -> atmosphere

    # Air
    c_air = 1005.4               # Specific heat of air at 273 K [J/kgK]
    airDensity = 1.025           # Densiity of air at 293 K [kg/m^3]
    kAir = 0.0257                # Thermal conductivity of air at 293 K [W/mK]

    if houseType == 1:
        windows_area = 213
        lenHouse = 35             # House length [m]
        widHouse = 25             # House width [m]
        htHouse = 6               # House height [m]
        roof_Area = 874

    if houseType == 2:
        windows_area = 400
        lenHouse = 50             # House length [m]
        widHouse = 30             # House width [m]
        htHouse = 7               # House height [m]
        roof_Area = 1504

    if houseType == 3:
        windows_area = 647
        lenHouse = 70             # House length [m]
        widHouse = 40             # House width [m]
        htHouse = 8               # House height [m]
        roof_Area = 3130

    LWindow = 0.004                 # Thickness of a single window pane [m]
    LCavity = 0.014                 # Thickness of the cavity between the double glass window [m]
    kWindow = 0.8                   # Thermal conductivity of glass [W/mK]

    U_windows = ((1/h_air_window) + (LWindow/kWindow) +
                 (LCavity/kAir) + (LWindow/kWindow) + (1/h_window_atm))**-1

    # Walls (concrete)
    LWall = 0.25           # Wall thickness [m]
    kWall = 0.14           # Thermal conductivity [W/mK]
    walls_area = 2*(lenHouse + widHouse) * htHouse - windows_area
    U_wall = ((1/h_air_wall) + (LWall / kWall) + (1/h_wall_atm))**-1

    # Roof (glass fiber)
    LRoof = 0.2            # Roof thickness [m]
    kRoof = 0.04           # Thermal conductivity of glass fiber [W/mK]
    U_roof = ((1/h_air_roof) + (LRoof/kRoof) + (1/h_roof_atm))**-1

    A_exposed = walls_area + windows_area



    ############################   Calculations ###############################
    ################### Thermal carrier ######################

    ## Thermal losses
    # Roof
    Qdot_roof = U_roof * roof_Area * (T_amb - T_0_in)

    # Windows
    Qdot_windows = U_windows * windows_area * (T_amb - T_0_in)

    # Walls
    Qdot_wall = U_wall * walls_area * (T_amb - T_0_in)

    # Infiltration and ventilation
    U_mph = U * 2.23694    # m/s to mph
    A_exposed_ft3 = A_exposed * 10.7639    # m3 to ft3

    dT = ((T_0_in - 273)*9/5 + 32) - ((T_amb - 273)*9/5 + 32)           # °C to °F

    # dTcopy = m.addVar(lb=-100, ub=100, name = "dTcopy")
    # abs_dT = m.addVar(lb=0, ub=100, name="abs_dT")
    # dTcopy = m.addVar(name = "dTcopy")
    # abs_dT = m.addVar(name="abs_dT")

    # m.addConstr(dTcopy == dT)
    # m.addConstr(abs_dT == gp.abs_(dTcopy))
    abs_dT = abs(dT)
    
    # m.addConstr(abs_dT >= dT)
    # m.addConstr(abs_dT >= -dT)


    A_unit = 0.01   #

    # sqrt_expr = m.addVar(lb=0, ub=10, name="sqrt_expr")
    # sqrt_input = m.addVar(lb=0, ub=10, name="sqrt_input")
    # sqrt_expr = m.addVar(name="sqrt_expr")
    # sqrt_input = m.addVar(name="sqrt_input")

    # m.addConstr(sqrt_input == C_stack * abs_dT + C_wind * U_mph**2)
    # m.addGenConstrPow(sqrt_input, sqrt_expr, 0.5, name="sqrt_constraint")

    # m.addConstr(sqrt_expr * sqrt_expr == C_stack * abs_dT + C_wind * U_mph**2)

    sqrt_expr = math.sqrt(C_stack * abs_dT + C_wind * U_mph**2)

    infiltrationAirflow =  A_exposed_ft3*A_unit*sqrt_expr*0.47194745/1000
    
    roof_Area_ft3 = roof_Area * 10.7639    # m3 to ft3
    ventilationAirflow =  (0.03*roof_Area_ft3 + 7.5*(1+N_bedrooms))*0.47194745/1000


    Qdot_iv = -c_air*airDensity*(infiltrationAirflow + ventilationAirflow)*(T_0_in -T_amb)


    Qdot_D = Qdot_roof + Qdot_windows + Qdot_wall + Qdot_iv

    return Qdot_D

def House_Thermal_losses_G(houseType, T_0_in, T_amb, m):

    #############################   Parameters ################################

    U = 1
    C_stack=0.015
    C_wind=0.0012
    N_bedrooms=1

    # Convective heat transfer coefficients [W/m^2K]
    h_air_wall = 0.9             # Indoor air -> walls, scaled to R-value of a C-label house
    h_wall_atm = 0.9             # Walls -> atmosphere, scaled to R-value of a C-label house
    h_air_window = 25            # Indoor air -> windows
    h_window_atm = 32            # Windows -> atmosphere
    h_air_roof = 12              # Indoor air -> roof
    h_roof_atm = 38              # Roof -> atmosphere

    # Air
    c_air = 1005.4               # Specific heat of air at 273 K [J/kgK]
    airDensity = 1.025           # Densiity of air at 293 K [kg/m^3]
    kAir = 0.0257                # Thermal conductivity of air at 293 K [W/mK]

    if houseType == 1:
        windows_area = 213
        lenHouse = 35             # House length [m]
        widHouse = 25             # House width [m]
        htHouse = 6               # House height [m]
        roof_Area = 874

    if houseType == 2:
        windows_area = 400
        lenHouse = 50             # House length [m]
        widHouse = 30             # House width [m]
        htHouse = 7               # House height [m]
        roof_Area = 1504

    if houseType == 3:
        windows_area = 647
        lenHouse = 70             # House length [m]
        widHouse = 40             # House width [m]
        htHouse = 8               # House height [m]
        roof_Area = 3130

    LWindow = 0.004                 # Thickness of a single window pane [m]
    LCavity = 0.014                 # Thickness of the cavity between the double glass window [m]
    kWindow = 0.8                   # Thermal conductivity of glass [W/mK]

    U_windows = ((1/h_air_window) + (LWindow/kWindow) +
                 (LCavity/kAir) + (LWindow/kWindow) + (1/h_window_atm))**-1

    # Walls (concrete)
    LWall = 0.25           # Wall thickness [m]
    kWall = 0.14           # Thermal conductivity [W/mK]
    walls_area = 2*(lenHouse + widHouse) * htHouse - windows_area
    U_wall = ((1/h_air_wall) + (LWall / kWall) + (1/h_wall_atm))**-1

    # Roof (glass fiber)
    LRoof = 0.2            # Roof thickness [m]
    kRoof = 0.04           # Thermal conductivity of glass fiber [W/mK]
    U_roof = ((1/h_air_roof) + (LRoof/kRoof) + (1/h_roof_atm))**-1

    A_exposed = walls_area + windows_area



    ############################   Calculations ###############################
    ################### Thermal carrier ######################

    ## Thermal losses
    # Roof
    Qdot_roof = U_roof * roof_Area * (T_amb - T_0_in)

    # Windows
    Qdot_windows = U_windows * windows_area * (T_amb - T_0_in)

    # Walls
    Qdot_wall = U_wall * walls_area * (T_amb - T_0_in)

    # Infiltration and ventilation
    U_mph = U * 2.23694    # m/s to mph
    A_exposed_ft3 = A_exposed * 10.7639    # m3 to ft3

    dT = ((T_0_in - 273)*9/5 + 32) - ((T_amb - 273)*9/5 + 32)           # °C to °F

    dTcopy = m.addVar(lb=-100, ub=100, name = "dTcopy")
    abs_dT = m.addVar(lb=0, ub=100, name="abs_dT")
    # dTcopy = m.addVar(name = "dTcopy")
    # abs_dT = m.addVar(name="abs_dT")

    m.addConstr(dTcopy == dT)
    m.addConstr(abs_dT == gp.abs_(dTcopy))
    
    # m.addConstr(abs_dT >= dT)
    # m.addConstr(abs_dT >= -dT)


    A_unit = 0.01   #

    sqrt_expr = m.addVar(lb=0, ub=10, name="sqrt_expr")
    sqrt_input = m.addVar(lb=0, ub=10, name="sqrt_input")
    # sqrt_expr = m.addVar(name="sqrt_expr")
    # sqrt_input = m.addVar(name="sqrt_input")

    m.addConstr(sqrt_input == C_stack * abs_dT + C_wind * U_mph**2)
    m.addGenConstrPow(sqrt_input, sqrt_expr, 0.5, name="sqrt_constraint")

    # m.addConstr(sqrt_expr * sqrt_expr == C_stack * abs_dT + C_wind * U_mph**2)

    infiltrationAirflow =  A_exposed_ft3*A_unit*sqrt_expr*0.47194745/1000
    
    roof_Area_ft3 = roof_Area * 10.7639    # m3 to ft3
    ventilationAirflow =  (0.03*roof_Area_ft3 + 7.5*(1+N_bedrooms))*0.47194745/1000


    Qdot_iv = -c_air*airDensity*(infiltrationAirflow + ventilationAirflow)*(T_0_in -T_amb)


    Qdot_D = Qdot_roof + Qdot_windows + Qdot_wall + Qdot_iv

    return Qdot_D