# -*- coding: utf-8 -*-
"""
The ``smarts`` module contains functions for calling SMARTS: Simple Model of the
Atmoshperic Radiative Transfer of Sunshine, from NREL, developed by 
Dr. Christian Gueymard. 

SMARTS software can be obtained from: 
    https://www.nrel.gov/grid/solar-resource/smarts.html

Users will be responsible to obtain a copy of SMARTS  from NREL, 
honor it’s license, and download the SMART files into their PVLib folder.

This wrapper is shared under a BSD-3-Clause License, and was
originally coded in Matlab by Juan Russo (2001), updated and ported to python
by Silvana Ayala (2019-2020). Original Matlab wrapper was made for graduate studies 
at the University of Arizona, python porting by NREL. 

Please read the license and Readme files for more information, proper use, citing, and copyrights.
    
"""

def _material_to_code(material):
    # Comments include Description, File name(.DAT extension), Reflection, Type*, Spectral range(um), Category*
    # *KEYS: L Lambertian, NL Non-Lambertian, SP Specular, M Manmade materials, S Soils and rocks, U User defined, V Vegetation, W Water, snow, or ice
    material_map = { 'UsrLamb':     '0',  # User-defined spectral reflectance Albedo L Userdefined
                     'UsrNLamb':    '1',  # User-defined spectral reflectance Albedo NL Userdefined
                     'Water':       '2',  # Water or calm ocean (calculated) SP 0.28 4.0 W
                     'Snow':        '3',  # Fresh dry snow Snow NL 0.3 2.48 W
                     'Neve':        '4',  # Snow on a mountain neve Neve NL 0.45 1.65 W
                     'Basalt':      '5',  # Basalt rock Basalt NL 0.3 2.48 S
                     'Dry_sand':    '6',  # Dry sand Dry_sand NL 0.32 0.99 S
                     'WiteSand':    '7',  # Sand from White Sands, NM WiteSand NL 0.5 2.48 S
                     'Soil':        '8',  # Bare soil Soil NL 0.28 4.0 S
                     'Dry_clay':    '9',  # Dry clay soil Dry_clay NL 0.5 2.48 S
                     'Wet_clay':    '10', # Wet clay soil Wet_clay NL 0.5 2.48 S
                     'Alfalfa':     '11', # Alfalfa Alfalfa NL 0.3 0.8 V
                     'Grass':       '12', # Green grass Grass NL 0.3 1.19 V
                     'RyeGrass':    '13', # Perennial rye grass RyeGrass NL 0.44 2.28 V
                     'Meadow1':     '14', # Alpine meadow Meadow1 NL 0.4 0.85 V
                     'Meadow2':     '15', # Lush meadow Meadow2 NL 0.4 0.9 V
                     'Wheat':       '16', # Wheat crop Wheat NL 0.42 2.26 V
                     'PineTree':    '17', # Ponderosa pine tree PineTree NL 0.34 2.48 V
                     'Concrete':    '18', # Concrete slab Concrete NL 0.3 1.3 M
                     'BlckLoam':    '19', # Black loam BlckLoam NL 0.4 4.0 S
                     'BrwnLoam':    '20', # Brown loam BrwnLoam NL 0.4 4.0 S
                     'BrwnSand':    '21', # Brown sand BrwnSand NL 0.4 4.0 S
                     'Conifers':    '22', # Conifer trees Conifers NL 0.302 4.0 V
                     'DarkLoam':    '23', # Dark loam DarkLoam NL 0.46-4.0 S
                     'DarkSand':    '24', # Dark sand DarkSand NL 0.4 4.0 S
                     'Decidous':    '25', # Decidous trees Decidous NL 0.302 4.0 V
                     'DryGrass':    '26', # Dry grass (sod) DryGrass NL 0.38 4.0 V
                     'DuneSand':    '27', # Dune sand DuneSand NL 0.4 4.0 S
                     'FineSnow':    '28', # Fresh fine snow FineSnow NL 0.3 4.0 W
                     'GrnGrass':    '29', # Green rye grass (sod) GrnGrass NL 0.302 4.0 V
                     'GrnlSnow':    '30', # Granular snow GrnlSnow NL 0.3 4.0 W
                     'LiteClay':    '31', # Light clay LiteClay NL 0.4 4.0 S
                     'LiteLoam':    '32', # Light loam LiteLoam NL 0.431 4.0 S
                     'LiteSand':    '33', # Light sand LiteSand NL 0.4 4.0 S
                     'PaleLoam':    '34', # Pale loam PaleLoam NL 0.4 4.0 S
                     'Seawater':    '35', # Sea water Seawater NL 2.079 4.0 W
                     'SolidIce':    '36', # Solid ice SolidIce NL 0.3 4.0 W
                     'Dry_Soil':    '37', # Dry soil Dry_Soil NL 0.28 4.0 S
                     'LiteSoil':    '38', # Light soil LiteSoil NL 0.28 4.0 S
                     'RConcrte':    '39', # Old runway concrete RConcrte NL 0.3 4.0 M
                     'RoofTile':    '40', # Terracota roofing clay tile RoofTile NL 0.3 4.0 M
                     'RedBrick':    '41', # Red construction brick RedBrick NL 0.3 4.0 M
                     'Asphalt':     '42', # Old runway asphalt Asphalt NL 0.3 4.0 M
                     'TallCorn':    '43', # Tall green corn TallCorn NL 0.36-1.0 V
                     'SndGravl':    '44', # Sand & gravel SndGravl NL 0.45-1.04 S
                     'Fallow':      '45', # Fallow field Fallow NL 0.32-1.19 S
                     'Birch':       '46', # Birch leaves Birch NL 0.36-2.48 V
                     'WetSoil':     '47', # Wet sandy soil WetSSoil NL 0.48-2.48 S
                     'Gravel':      '48', # Gravel Gravel NL 0.32-1.3 S
                     'WetClay2':    '49', # Wet red clay WetClay2 NL 0.52-2.48 S
                     'WetSilt':     '50', # Wet silt WetSilt NL 0.52-2.48 S
                     'LngGrass':    '51', # Dry long grass LngGrass NL 0.277-2.976 V
                     'LwnGrass':    '52', # Lawn grass (generic bluegrass) LwnGrass NL 0.305-2.944 V
                     'OakTree':     '53', # Deciduous oak tree leaves OakTree NL 0.35-2.5 V
                     'Pinion':      '54', # Pinion pinetree needles Pinion NL 0.301-2.592 V
                     'MeltSnow':    '55', # Melting snow (slush) MeltSnow NL 0.35-2.5 W
                     'Plywood':     '56', # Plywood sheet (new, pine, 4-ply) Plywood NL 0.35-2.5 M
                     'WiteVinl':    '57', # White vinyl plastic sheet, 0.15 mm WiteVinl NL 0.35-2.5 M
                     'FibrGlss':    '58', # Clear fiberglass greenhouse roofing FibrGlss NL 0.35-2.5 M
                     'ShtMetal':    '59', # Galvanized corrugated sheet metal, new ShtMetal NL 0.35-2.5 M
                     'Wetland':     '60', # Wetland vegetation canopy, Yellowstone Wetland NL 0.409-2.478 V
                     'SageBrsh':    '61', # Sagebrush canopy, Yellowstone SageBrsh NL 0.409-2.478 V
                     'FirTrees':    '62', # Fir trees, Colorado FirTrees NL 0.353-2.592 V
                     'CSeaWatr':    '63', # Coastal seawater, Pacific CSeaWatr NL 0.277-2.976 W
                     'OSeaWatr':    '64', # Open ocean seawater, Atlantic OSeaWatr NL 0.277-2.976 W
                     'GrazingField':'65', # Grazing field (unfertilized) GrazingField NL 0.401-2.499 V
                     'Spruce':      '66'  # Young Norway spruce tree (needles) Spruce NL 0.39-0.845 V
                }
    
    if not material:
        return material_map.keys()
    if material not in material_map:
        print(f"Unknown material specified: '{material}'")
        return None
    return material_map.get(material)

def SMARTSSpectra(IOUT,YEAR,MONTH,DAY,HOUR, LATIT, LONGIT, ALTIT, ZONE, material='LiteSoil', min_wvl='280', max_wvl='4000'):
    r'''
    This function calculates the spectral albedo for a given material. If no 
    material is provided, the function will return a list of all valid 
    materials.

    Parameters
    ----------
    material : string
        Unique identifier for ground cover. Pass None to retreive a list of
        all valid materials.
    WLMN : string
        Minimum wavelength to retreive
    WLMX : string
        Maximum wavelength to retreive
    YEAR : string
        Year
    MONTH : string
        Month
    DAY : string
        Day
    HOUR : string
        Hour, in 24 hour format.
    LATIT : string
        Latitude of the location.
    LONGIT : string
        Longitude of the location.
    ALTIT : string
        elevation of the ground surface above sea level [km]
    ZONE : string
        Timezone
        
        

    Returns
    -------
    data : pandas
        Matrix with first column representing wavelength (in nm) and second
        column representing albedo of specified material at the wavelength
    
    Updates:
           6/20 Creation of second function to use zenith and azimuth M. Monarch
    '''

    ## Card 1: Comment. 64 characters max. In theory no spaces but yes underscores.
    CMNT = 'ASTMG173-03 (AM1.5 Standard)'
    
    ## Card 2: ISPR is an option for site's pressure.
    # ISPR = 0 to input SPR on Card 2a
    # ISPR = 1 to input SPR, ALTIT and HEIGHT on Card 2a
    # ISPR = 2 to input LATIT, ALTIT and HEIGHT on Card 2a.
    ISPR = '1'
    
    # Card 2a (if ISPR = 0): SPR
    SPR = '1013.25' #mbar
    
    # Card 2a (if ISPR = 1): SPR, ALTIT, HEIGHT
    # SPR: Surface pressure (mb).
    # ALTIT: Site's altitude, i.e., elevation of the ground surface above sea level (km); must be
    # <= 100 km. In case of a flying object, ALTIT refers to the ground surface below it.
    # HEIGHT: Height of the simulated object above the ground surface underneath (km); must be
    # <= 100 km (new input).
    # The total ALTIT + HEIGHT is the altitude of the simulated object above sea level and
    # must be <= 100 km.
    
    # Card 2a (if ISPR = 2): LATIT, ALTIT, HEIGHT
    # LATIT: Site's latitude (decimal degrees, positive North, negative South); e.g., -17.533 for
    # Papeete, Tahiti. If LATIT is unknown, enter 45.0.
    # ALTIT: Site's altitude, i.e., elevation of the ground surface above sea level (km); must be
    # <= 100 km. In case of a flying object, ALTIT refers to the ground surface below it.
    # HEIGHT: Height of the simulated object above the ground surface underneath (km); must be
    # <= 100 km (new input).
    # The total ALTIT + HEIGHT is the altitude of the simulated object above sea level and
    # must be <= 100 km.
    
    ALTIT = ALTIT
    HEIGHT = '0'
    #LATIT = LATIT 
    
    ## Card 3: IATMOS is an option to select the proper default atmosphere
    # Its value can be either 0 or 1.
    # Set IATMOS = 0 to define a realistic (i.e., non-reference) atmosphere. Card 3a will then have to
    # provide TAIR, RH, SEASON, TDAY.
    # Set IATMOS = 1 to select one of 10 default reference atmospheres (i.e., for ideal conditions). The
    # shortened name of this atmosphere must be provided by ATMOS on Card 3a.
    
    IATMOS = '1'
    
    # Card 3a (if IATMOS = 1): ATMOS
    # ATMOS is the name of the selected reference atmosphere; 4 characters max. This name can
    # be one of the following: 
    #    USSA   (U.S. Standard Atmosphere)   MLS   (Mid-Latitude Summer) 
    #    MLW   (Mid-Latitude Winter)   SAS   (Sub-Arctic Summer) 
    #   SAW   (Sub-Arctic Winter)   TRL   (Tropical)   STS   (Sub-Tropical Summer)
    #   STW   (Sub-Tropical Winter)   AS   (Arctic Summer)   AW   (Arctic Winter)
    
    ATMOS = 'USSA'
    
    # Card 3a(if IATMOS = 0): TAIR, RH, SEASON, TDAY.
    # RH: Relative humidity at site level (%).
    # SEASON: Can be either `WINTER` or `SUMMER`, for calculation of precipitable water and
    # stratospheric temperature. If the true season is Fall, select WINTER. Select SUMMER if the
    # true season is Spring. SEASON slightly affects the ozone effective temperature and the
    # aerosol optical characteristics.
    # TAIR: Atmospheric temperature at site level (°C). Acceptable range: -120 < TAIR < 50.
    # TDAY: Average daily temperature at site level (°C). For a flying object (HEIGHT > 0), this
    # is a reference temperature for various calculations, therefore it is important to provide a
    # realistic value in this case in particular. Acceptable range: -120 < TDAY < 50.
    
    RH = ''
    TAIR = ''
    SEASON = ''
    TDAY = ''
    
    ## Card 4: IH2O is an option to select the correct water vapor data. All water vapor calculations involve
    # precipitable water, W. The following values of IH2O are possible:
    # 0, to input W on Card 4a
    # 1, if W is to be defaulted to a value prescribed by the selected reference atmosphere and the site
    # altitude (thus if IATMOS = 1 on Card 3). If IATMOS != 1, USSA will be defaulted for this step.
    # 2, if W is to be calculated by the program from TAIR and RH (thus if IATMOS = 0 on Card 3). This
    # calculation is only approximate (particularly if HEIGHT > 0) and therefore this option is not
    # recommended.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    IH2O = '1'
    
    # Card 4a: (if IH2O = 0): W is precipitable water above the site altitude
    # in units of cm, or equivalently, g/cm2; it must be <= 12.
    W = ''
    
    ## Card 5: IO3 is an option to select the appropriate ozone abundance input.
    # IO3 = 0 to input IALT and AbO3 on Card 5a
    # IO3 = 1 to use a default value for AbO3 according to the reference atmosphere selected by
    # IATMOS. If IATMOS != 1, USSA will be defaulted for this calculation.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    
    IO3 = '1'
    
    # Card 5a (if IO3 = 0): IALT, AbO3
    # IALT is an option to select the appropriate ozone column altitude correction.
    # IALT = 0 bypasses the altitude correction, so that the value of AbO3 on
    # Card 5a is used as is. IALT = 1 should be rather used if a vertical
    # profile correction needs to be applied (in case of an elevated site when
    # the value of AbO3 is known only at sea level). 
    
    IALT = ''
    AbO3 = ''
    
    ## Card 6 IGAS is an option to define the correct conditions for gaseous absorption and atmospheric pollution. 
    # IGAS = 0 if ILOAD on Card 6a is to be read so that extra gaseous absorption calculations
    # (corresponding to the gas load in the lower troposphere due to pollution or absence thereof) can be
    # initiated;
    # IGAS =1 if all gas abundances (except carbon dioxide, ozone and water vapor see Cards 4a, 5a,
    # and 7) are to be defaulted, using average vertical profiles.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    
    IGAS = '0'
    
    # Card 6a  (if IGAS = 0): ILOAD is an option for tropospheric pollution, only used if IGAS = 0.
    # For ILOAD = 0, Card 6b will be read with the concentrations of 10 pollutants.
    # ILOAD = 1 selects default PRISTINE ATMOSPHERIC conditions, leading to slightly
    # reduced abundances of some gases compared to the initial default obtained with the selected
    # reference atmosphere.
    # Setting ILOAD to 2-4 will increase the concentration of the 10 pollutants to possibly
    # represent typical urban conditions: LIGHT POLLUTION (ILOAD = 2), MODERATE
    # POLLUTION (ILOAD = 3), and SEVERE POLLUTION (ILOAD = 4).
    
    ILOAD = '1'
    
    # Card 6b (if IGAS = 0 and ILOAD = 0): ApCH2O, ApCH4, ApCO, ApHNO2,
    # ApHNO3, ApNO, ApNO2, ApNO3, ApO3, ApSO2
    # ApCH2O: Formaldehyde volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApCH4: Methane volumetric concentration in the assumed 1-km deep tropospheric pollution
    # layer (ppmv).
    # ApCO: Carbon monoxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv), Card 6b.
    # ApHNO2: Nitrous acid volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApHNO3: Nitric acid volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO: Nitric oxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO2: Nitrogen dioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO3: Nitrogen trioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApO3: Ozone volumetric concentration in the assumed 1-km deep tropospheric pollution
    # layer (ppmv).
    # ApSO2: Sulfur dioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    
    ApCH2O = ''
    ApCH4 = ''
    ApCO = ''
    ApHNO2 = ''
    ApHNO3 = ''
    ApNO = ''
    ApNO2 = ''
    ApNO3 = ''
    ApO3 = ''
    ApSO2 =''
    
    ## Card 7 qCO2 carbon dioxide columnar volumetric concentration (ppmv).
    qCO2 = '0.0'
    
    # Card 7a ISPCTR 
    # is an option to select the proper extraterrestrial
    # spectrum. This option allows to choose one out of ten possible spectral
    # files (``Spctrm_n.dat``, where n = 0-8 or n = U).  
    # -1  Spctrm_U.dat  N/A User User
    # 0  Spctrm_0.dat  N/A Gueymard, 2004 (synthetic) 1366.10
    # 1  Spctrm_1.dat  N/A Gueymard, unpublished (synthetic) 1367.00
    # 2  Spctrm_2.dat  cebchkur MODTRAN, Cebula/Chance/Kurucz 1362.12
    # 3  Spctrm_3.dat  chkur MODTRAN, Chance/Kurucz 1359.75
    # 4  Spctrm_4.dat  newkur MODTRAN, New Kurucz 1368.00
    # 5  Spctrm_5.dat  oldkur MODTRAN, Old Kurucz 1373.16
    # 6  Spctrm_6.dat  thkur MODTRAN, Thuillier/Kurucz 1376.23
    # 7  Spctrm_7.dat  MODTRAN2 Wehrli/WRC/WMO, 1985 1367.00
    # 8  Spctrm_8.dat  N/A ASTM E490, 2000 (synthetic) 1366.10
    
    ISPCTR ='0'
    
    ## Card 8: AEROS selects the aerosol model, with one of the following twelve possible choices:
    #  S&F_RURAL ,  S&F_URBAN ,  S&F_MARIT ,  S&F_TROPO , These four choices
    # refer respectively to the Rural, Urban, Maritime and Tropospheric aerosol
    # models (Shettle and Fenn, 1979), which are humidity dependent and common with MODTRAN. 
    #  SRA_CONTL ,  SRA_URBAN ,  SRA_MARIT , These three choices refer
    # respectively to the Continental, Urban, and Maritime aerosol models of
    # the IAMAP preliminary standard atmosphere (IAMAP, 1986). 
    #  B&D_C ,  B&D_C1 , These two choices refer respectively to the Braslau &
    # Dave aerosol type C and C1, themselves based on Deirmendjian's Haze L model. 
    #  DESERT_MIN ,  DESERT_MAX  DESERT_MIN corresponds to background (normal)
    # conditions in desert areas, whereas DESERT_MAX corresponds to extremely
    # turbid conditions (sandstorms).  
    # 'USER' Card 8a is then necessary to input user-supplied aerosol information.
    
    AEROS = 'S&F_TROPO' 
    # Card 8a: 
    # if AEROS =  USER : ALPHA1, ALPHA2, OMEGL, GG These 4 variables must represent broadband average values only!
    # ALPHA1: Average value of Ångström's wavelength exponent  $\alpha$ for wavelengths < 500 nm
    # (generally between 0.0 and 2.6).
    # ALPHA2: Average value of Ångström's wavelength exponent  $\alpha$ for wavelengths >= 500 nm
    # (generally between 0.0 and 2.6).
    # OMEGL: Aerosol single scattering albedo (generally between 0.6 and 1.0).
    # GG: Aerosol asymmetry parameter (generally between 0.5 and 0.9).
    ALPHA1 = ''
    ALPHA2 = ''
    OMEGL = ''
    GG = ''
    
    ## Card 9: ITURB is an option to select the correct turbidity data input. The different options are:
    # 0, to read TAU5 on Card 9a
    # 1, to read BETA on Card 9a
    # 2, to read BCHUEP on Card 9a
    # 3, to read RANGE on Card 9a
    # 4, to read VISI on Card 9a
    # 5, to read TAU550 on Card 9a (new option).
    
    ITURB = '0'
    
    #Card 9a Turbidity value
    TAU5 = '0.00' #if ITURB == 0
    BETA = '' #if ITURB == 1
    BCHUEP = '' #if ITURB == 2
    RANGE = '' #if ITURB == 3
    VISI = '' #if ITURB == 4
    TAU550 = '' #if ITURB == 5
    
    ## Card 10: Far Field Albedo for backscattering
    IALBDX = _material_to_code(material)
    
    # Card 10a:
    RHOX = ''
                            # Zonal broadband Lambertian ground albedo (for backscattering calculations); must
                            # be between 0 and 1.
                            
    # Card 10b: ITILT is an option for tilted surface calculations. 
    #Select ITILT= 0 for no such calculation, 
    #ITILT = 1 to initiate these calculations using information on Card 10c.
    ITILT = '1'
    
    # Card 10c:
    # IALBDG is identical to IALBDX (see Card 10) except that it relates to the foreground local
    # albedo seen by a tilted surface. The list of options is identical to that of IALBDG and thus
    # extends from 1 to 64 (new).
    # TILT: Tilt angle of the receiving surface (0 to 90 decimal deg.); e.g. 90.0 for a vertical
    # plane. Use -999 for a sun-tracking surface.
    # WAZIM: Surface azimuth (0 to 360 decimal deg.) counted clockwise from North; e.g., 270
    # deg. for a surface facing West. Use -999 for a sun-tracking surface.
    
    IALBDG = IALBDX 
    TILT = '0.0'
    WAZIM = '180.0'
    
    # Card 10d:
    # RHOG: Local broadband Lambertian foreground albedo (for tilted plane calculations), Card
    # 10d (if IALBDG = -1); usually between 0.05 and 0.90.
    RHOG = ''
    
    ## Card 11: Spectral range for all Calculations
    WLMN = min_wvl #Min wavelength
    WLMX = max_wvl #Max wavelength
    SUNCOR = '1.0' 
        #Correction factor for irradiance is a correction factor equal to the inverse squared actual radius vector, or true Sun-Earth
        # distance; e.g., SUNCOR = 1.024.
        # SUNCOR varies naturally between 0.966 and 1.034, adding 3.4% to the irradiance in January
        # and reducing it by 3.4% in July. It is calculated by the program if the solar position is calculated
        # from date & time, i.e., if IMASS = 3 on Card 17, thus overwriting the input SUNCOR value on
        # Card 11. If solar position is directly input instead (IMASS = 3), SUNCOR should be set to 1.0 if
        # the average extraterrestrial irradiance (or solar constant, see SOLARC) is to be used, or to any
        # other number between 0.966 and 1.034 to correct it for distance if so desired.

    SOLARC = '1367.0' #Solar constant
    
    
    ## Card 12: Output results selection:
    # IPRT is an option to select the results to be printed on Files 16 and 17. Only broadband results are
    # output (to File 16) if IPRT = 0. Spectral results are added to File 16,
    # and Card 12a is read, if IPRT = 1. Spectral results are rather printed to
    # File 17 (in a spreadsheet-like format) if IPRT = 2. Finally, spectral
    # results are printed to both File 16 and 17 if IPRT = 3. Cards 
    # 12b and 12c are read if IPRT = 2 or 3 (see IOTOT and IOUT).
    
    IPRT = '2'
    
    # Card 12a: Min, Max and Step wavelength (nm) (Output can be different than
    # calculation...
    WPMN = WLMN
    WPMX = WLMX
    INTVL = '.5'
    
    # Card 12b: Total number of output variables:
    #IOTOT = XXX #This is determined with the input of this function
    
    # Card 12c: Variables to output selection 
    #(space separated numbers 1-43 according to the table below:
    IOUT = IOUT
    
    
    ## Card 13: Circumsolar Calculation
    # ICIRC is an option controlling the calculation of circumsolar radiation, which is useful when
    # simulating any type of radiometer (spectral or broadband) equipped with a collimator.
    # ICIRC = 0 bypasses these calculations.
    # ICIRC = 1 indicates that a typical radiometer needs to be simulated. The geometry of its collimator
    # must then defined on Card 13a.
    
    ICIRC = '0'
    
    #Card 13a (if ICIRC = 1): SLOPE, APERT, LIMIT
    SLOPE = ''
    APERT = ''
    LIMIT = ''
    
    ## Card 14 Option for using the scanning/smoothing virtual filter of the postprocessor.
    # The smoothed results are output on a spreadsheet-ready file, File 18 (``smarts295.scn.txt``). This postprocessor is
    # activated if ISCAN = 1, not if ISCAN = 0. Card 14a is read if ISCAN = 1.
    
    ISCAN = '0'
    
    # Card 14a (if ISCAN = 1): IFILT, WV1, WV2, STEP, FWHM
    IFILT = ''
    WV1 = ''
    WV2 = ''
    STEP = ''
    FWHM = ''
    
    ## Card 15 ILLUM: Option for illuminance, luminous efficacy and photosynthetically active radiation (PAR)
    # calculations. These calculations take place if ILLUM = -1, 1, -2 or 2, and are bypassed if ILLUM = 0.
    # With ILLUM = -1 or 1, illuminance calculations are based on the CIE photopic curve (or Vlambda
    # curve) of 1924, as supplied in File ``VLambda.dat``. With ILLUM = -2 or 2, the same calculations are
    # done but the revised CIE photopic curve of 1988 is rather used (from File ``VMLambda.dat``). Note
    # that selecting ILLUM = 1 or -1 will override WLMN and WLMX (see Card 11) so that calculations
    # are done between at least 360 and 830 nm.
    # Moreover, if ILLUM = 1 or 2, luminous efficacy calculations are added to the illuminance
    # calculations. This overrides the values of WLMN and WLMX on Card 11, and replaces them by 280
    # and 4000, respectively.
    
    ILLUM = '0'
    
    ## Card  16: Option for special broadband UV calculations. Select IUV = 0 for no special UV calculation, 
    # IUV = 1 to initiate such calculations. These include UVA, UVB, UV index, and
    # different action weighted irradiances of interest in photobiology.
    # Note that IUV = 1 overrides WLMN and WLMX so that calculations are done between at least 280
    # and 400 nm. The spectral results are also printed between at least 280 and 400 nm, irrespective of
    # the IPRT, WPMN, and WPMX values.
    
    IUV = '0'
    
    ## Card 17:
    # Option for solar position and air mass calculations. Set IMASS to:
    # 0, if inputs are to be ZENIT, AZIM on Card 17a
    # 1, if inputs are to be ELEV, AZIM on Card 17a
    # 2, if input is to be AMASS on Card 17a
    # 3, if inputs are to be YEAR, MONTH, DAY, HOUR, LATIT, LONGIT, ZONE on Card 17a
    # 4, if inputs are to be MONTH, LATIT, DSTEP on Card 17a (for a daily calculation).
    IMASS = '3'

    
    # Card 17a: IMASS = 0 Zenith and azimuth
    ZENITH = ''
    AZIM = ''
    
    # Card 17a: IMASS = 1 Elevation and Azimuth
    ELEV = ''
    
    # Card 17a: IMASS = 2 Input air mass directly
    AMASS = ''
    
    # Card 17a: IMASS = 3 Input date, time and coordinates
    YEAR = YEAR
    MONTH = MONTH
    DAY = DAY
    HOUR = HOUR
    LATIT = LATIT
    LONGIT = LONGIT
    ZONE = ZONE
    
    # Card 17a: IMASS = 4 Input Moth, Latitude and DSTEP
    DSTEP = ''

    output = _smartsAll(CMNT, ISPR, SPR, ALTIT, HEIGHT, LATIT, IATMOS, ATMOS, RH, TAIR, SEASON, TDAY, IH2O, W, IO3, IALT, AbO3, IGAS, ILOAD, ApCH2O, ApCH4, ApCO, ApHNO2, ApHNO3, ApNO,ApNO2, ApNO3, ApO3, ApSO2, qCO2, ISPCTR, AEROS, ALPHA1, ALPHA2, OMEGL, GG, ITURB, TAU5, BETA, BCHUEP, RANGE, VISI, TAU550, IALBDX, RHOX, ITILT, IALBDG,TILT, WAZIM,  RHOG, WLMN, WLMX, SUNCOR, SOLARC, IPRT, WPMN, WPMX, INTVL, IOUT, ICIRC, SLOPE, APERT, LIMIT, ISCAN, IFILT, WV1, WV2, STEP, FWHM, ILLUM,IUV, IMASS, ZENITH, AZIM, ELEV, AMASS, YEAR, MONTH, DAY, HOUR, LONGIT, ZONE, DSTEP)

    return output



def SMARTSSpectraZenAzm(IOUT, ZENITH, AZIM, material='LiteSoil', SPR='1013.25', min_wvl='280', max_wvl='4000'):
    r'''
    This function calculates the spectral albedo for a given material. If no 
    material is provided, the function will return a list of all valid 
    materials.

    Parameters
    ----------
    material : string
        Unique identifier for ground cover. Pass None to retreive a list of
        all valid materials.
    WLMN : string
        Minimum wavelength to retreive
    WLMX : string
        Maximum wavelength to retreive
    ZENITH : string
        Zenith angle of sun
    AZIM : string
        Azimuth of sun
    SPR : string
        Site Pressure [mbars]. Default: SPR = '1013.25'
        
        

    Returns
    -------
    data : pandas
        Matrix with first column representing wavelength (in nm) and second
        column representing albedo of specified material at the wavelength
    
    Updates:
           6/20 Creation of second function to use zenith and azimuth M. Monarch
    '''

    ## Card 1: Comment. 64 characters max. In theory no spaces but yes underscores.
    CMNT = 'ASTMG173-03 (AM1.5 Standard)'   
    
    ## Card 2: ISPR is an option for site's pressure.
    # ISPR = 0 to input SPR on Card 2a
    # ISPR = 1 to input SPR, ALTIT and HEIGHT on Card 2a
    # ISPR = 2 to input LATIT, ALTIT and HEIGHT on Card 2a.
    ISPR = '0'
    
    # Card 2a (if ISPR = 0): SPR
    SPR = SPR #mbar
    
    # Card 2a (if ISPR = 1): SPR, ALTIT, HEIGHT
    # SPR: Surface pressure (mb).
    # ALTIT: Site's altitude, i.e., elevation of the ground surface above sea level (km); must be
    # <= 100 km. In case of a flying object, ALTIT refers to the ground surface below it.
    # HEIGHT: Height of the simulated object above the ground surface underneath (km); must be
    # <= 100 km (new input).
    # The total ALTIT + HEIGHT is the altitude of the simulated object above sea level and
    # must be <= 100 km.
    
    # Card 2a (if ISPR = 2): LATIT, ALTIT, HEIGHT
    # LATIT: Site's latitude (decimal degrees, positive North, negative South); e.g., -17.533 for
    # Papeete, Tahiti. If LATIT is unknown, enter 45.0.
    # ALTIT: Site's altitude, i.e., elevation of the ground surface above sea level (km); must be
    # <= 100 km. In case of a flying object, ALTIT refers to the ground surface below it.
    # HEIGHT: Height of the simulated object above the ground surface underneath (km); must be
    # <= 100 km (new input).
    # The total ALTIT + HEIGHT is the altitude of the simulated object above sea level and
    # must be <= 100 km.
    
    ALTIT = '' 
    HEIGHT = ''
    #LATIT = LATIT
    
    ## Card 3: IATMOS is an option to select the proper default atmosphere
    # Its value can be either 0 or 1.
    # Set IATMOS = 0 to define a realistic (i.e., non-reference) atmosphere. Card 3a will then have to
    # provide TAIR, RH, SEASON, TDAY.
    # Set IATMOS = 1 to select one of 10 default reference atmospheres (i.e., for ideal conditions). The
    # shortened name of this atmosphere must be provided by ATMOS on Card 3a.
    
    IATMOS = '1'
    
    # Card 3a (if IATMOS = 1): ATMOS
    # ATMOS is the name of the selected reference atmosphere; 4 characters max. This name can
    # be one of the following: 
    #    USSA   (U.S. Standard Atmosphere)   MLS   (Mid-Latitude Summer) 
    #    MLW   (Mid-Latitude Winter)   SAS   (Sub-Arctic Summer) 
    #   SAW   (Sub-Arctic Winter)   TRL   (Tropical)   STS   (Sub-Tropical Summer)
    #   STW   (Sub-Tropical Winter)   AS   (Arctic Summer)   AW   (Arctic Winter)
    
    ATMOS = 'USSA'
    
    # Card 3a(if IATMOS = 0): TAIR, RH, SEASON, TDAY.
    # RH: Relative humidity at site level (%).
    # SEASON: Can be either `WINTER` or `SUMMER`, for calculation of precipitable water and
    # stratospheric temperature. If the true season is Fall, select WINTER. Select SUMMER if the
    # true season is Spring. SEASON slightly affects the ozone effective temperature and the
    # aerosol optical characteristics.
    # TAIR: Atmospheric temperature at site level (°C). Acceptable range: -120 < TAIR < 50.
    # TDAY: Average daily temperature at site level (°C). For a flying object (HEIGHT > 0), this
    # is a reference temperature for various calculations, therefore it is important to provide a
    # realistic value in this case in particular. Acceptable range: -120 < TDAY < 50.
    
    RH = ''
    TAIR = ''
    SEASON = ''
    TDAY = ''
    
    ## Card 4: IH2O is an option to select the correct water vapor data. All water vapor calculations involve
    # precipitable water, W. The following values of IH2O are possible:
    # 0, to input W on Card 4a
    # 1, if W is to be defaulted to a value prescribed by the selected reference atmosphere and the site
    # altitude (thus if IATMOS = 1 on Card 3). If IATMOS != 1, USSA will be defaulted for this step.
    # 2, if W is to be calculated by the program from TAIR and RH (thus if IATMOS = 0 on Card 3). This
    # calculation is only approximate (particularly if HEIGHT > 0) and therefore this option is not
    # recommended.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    IH2O = '1'
    
    # Card 4a: (if IH2O = 0): W is precipitable water above the site altitude
    # in units of cm, or equivalently, g/cm2; it must be <= 12.
    W = ''
    
    ## Card 5: IO3 is an option to select the appropriate ozone abundance input.
    # IO3 = 0 to input IALT and AbO3 on Card 5a
    # IO3 = 1 to use a default value for AbO3 according to the reference atmosphere selected by
    # IATMOS. If IATMOS != 1, USSA will be defaulted for this calculation.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    
    IO3 = '1'
    
    # Card 5a (if IO3 = 0): IALT, AbO3
    # IALT is an option to select the appropriate ozone column altitude correction.
    # IALT = 0 bypasses the altitude correction, so that the value of AbO3 on
    # Card 5a is used as is. IALT = 1 should be rather used if a vertical
    # profile correction needs to be applied (in case of an elevated site when
    # the value of AbO3 is known only at sea level). 
    
    IALT = ''
    AbO3 = ''
    
    ## Card 6 IGAS is an option to define the correct conditions for gaseous absorption and atmospheric pollution. 
    # IGAS = 0 if ILOAD on Card 6a is to be read so that extra gaseous absorption calculations
    # (corresponding to the gas load in the lower troposphere due to pollution or absence thereof) can be
    # initiated;
    # IGAS =1 if all gas abundances (except carbon dioxide, ozone and water vapor see Cards 4a, 5a,
    # and 7) are to be defaulted, using average vertical profiles.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    
    IGAS = '0'
    
    # Card 6a  (if IGAS = 0): ILOAD is an option for tropospheric pollution, only used if IGAS = 0.
    # For ILOAD = 0, Card 6b will be read with the concentrations of 10 pollutants.
    # ILOAD = 1 selects default PRISTINE ATMOSPHERIC conditions, leading to slightly
    # reduced abundances of some gases compared to the initial default obtained with the selected
    # reference atmosphere.
    # Setting ILOAD to 2-4 will increase the concentration of the 10 pollutants to possibly
    # represent typical urban conditions: LIGHT POLLUTION (ILOAD = 2), MODERATE
    # POLLUTION (ILOAD = 3), and SEVERE POLLUTION (ILOAD = 4).
    
    ILOAD = '1'
    
    # Card 6b (if IGAS = 0 and ILOAD = 0): ApCH2O, ApCH4, ApCO, ApHNO2,
    # ApHNO3, ApNO, ApNO2, ApNO3, ApO3, ApSO2
    # ApCH2O: Formaldehyde volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApCH4: Methane volumetric concentration in the assumed 1-km deep tropospheric pollution
    # layer (ppmv).
    # ApCO: Carbon monoxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv), Card 6b.
    # ApHNO2: Nitrous acid volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApHNO3: Nitric acid volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO: Nitric oxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO2: Nitrogen dioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO3: Nitrogen trioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApO3: Ozone volumetric concentration in the assumed 1-km deep tropospheric pollution
    # layer (ppmv).
    # ApSO2: Sulfur dioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    
    ApCH2O = ''
    ApCH4 = ''
    ApCO = ''
    ApHNO2 = ''
    ApHNO3 = ''
    ApNO = ''
    ApNO2 = ''
    ApNO3 = ''
    ApO3 = ''
    ApSO2 =''
    
    ## Card 7 qCO2 carbon dioxide columnar volumetric concentration (ppmv).
    qCO2 = '0.0'
    
    # Card 7a ISPCTR 
    # is an option to select the proper extraterrestrial
    # spectrum. This option allows to choose one out of ten possible spectral
    # files (``Spctrm_n.dat``, where n = 0-8 or n = U).  
    # -1  Spctrm_U.dat  N/A User User
    # 0  Spctrm_0.dat  N/A Gueymard, 2004 (synthetic) 1366.10
    # 1  Spctrm_1.dat  N/A Gueymard, unpublished (synthetic) 1367.00
    # 2  Spctrm_2.dat  cebchkur MODTRAN, Cebula/Chance/Kurucz 1362.12
    # 3  Spctrm_3.dat  chkur MODTRAN, Chance/Kurucz 1359.75
    # 4  Spctrm_4.dat  newkur MODTRAN, New Kurucz 1368.00
    # 5  Spctrm_5.dat  oldkur MODTRAN, Old Kurucz 1373.16
    # 6  Spctrm_6.dat  thkur MODTRAN, Thuillier/Kurucz 1376.23
    # 7  Spctrm_7.dat  MODTRAN2 Wehrli/WRC/WMO, 1985 1367.00
    # 8  Spctrm_8.dat  N/A ASTM E490, 2000 (synthetic) 1366.10
    
    ISPCTR ='0'
    
    ## Card 8: AEROS selects the aerosol model, with one of the following twelve possible choices:
    #  S&F_RURAL ,  S&F_URBAN ,  S&F_MARIT ,  S&F_TROPO , These four choices
    # refer respectively to the Rural, Urban, Maritime and Tropospheric aerosol
    # models (Shettle and Fenn, 1979), which are humidity dependent and common with MODTRAN. 
    #  SRA_CONTL ,  SRA_URBAN ,  SRA_MARIT , These three choices refer
    # respectively to the Continental, Urban, and Maritime aerosol models of
    # the IAMAP preliminary standard atmosphere (IAMAP, 1986). 
    #  B&D_C ,  B&D_C1 , These two choices refer respectively to the Braslau &
    # Dave aerosol type C and C1, themselves based on Deirmendjian s Haze L model. 
    #  DESERT_MIN ,  DESERT_MAX  DESERT_MIN corresponds to background (normal)
    # conditions in desert areas, whereas DESERT_MAX corresponds to extremely
    # turbid conditions (sandstorms).  
    # 'USER' Card 8a is then necessary to input user-supplied aerosol information.
    
    AEROS = 'S&F_TROPO' 
    # Card 8a: 
    # if AEROS =  USER : ALPHA1, ALPHA2, OMEGL, GG These 4 variables must represent broadband average values only!
    # ALPHA1: Average value of Ångström`s wavelength exponent $\alpha$ for wavelengths < 500 nm
    # (generally between 0.0 and 2.6).
    # ALPHA2: Average value of Ångström`s wavelength exponent $\alpha$ for wavelengths >= 500 nm
    # (generally between 0.0 and 2.6).
    # OMEGL: Aerosol single scattering albedo (generally between 0.6 and 1.0).
    # GG: Aerosol asymmetry parameter (generally between 0.5 and 0.9).
    ALPHA1 = ''
    ALPHA2 = ''
    OMEGL = ''
    GG = ''
    
    ## Card 9: ITURB is an option to select the correct turbidity data input. The different options are:
    # 0, to read TAU5 on Card 9a
    # 1, to read BETA on Card 9a
    # 2, to read BCHUEP on Card 9a
    # 3, to read RANGE on Card 9a
    # 4, to read VISI on Card 9a
    # 5, to read TAU550 on Card 9a (new option).
    
    ITURB = '0'
    
    #Card 9a Turbidity value
    TAU5 = '0.00' #if ITURB == 0
    BETA = '' #if ITURB == 1
    BCHUEP = '' #if ITURB == 2
    RANGE = '' #if ITURB == 3
    VISI = '' #if ITURB == 4
    TAU550 = '' #if ITURB == 5
    
    ## Card 10: Far Field Albedo for backscattering
    IALBDX = _material_to_code(material)
    
    # Card 10a:
    RHOX = ''
                            # Zonal broadband Lambertian ground albedo (for backscattering calculations); must
                            # be between 0 and 1.
                            
    # Card 10b: ITILT is an option for tilted surface calculations. 
    #Select ITILT= 0 for no such calculation, 
    #ITILT = 1 to initiate these calculations using information on Card 10c.
    ITILT = '1'
    
    # Card 10c:
    # IALBDG is identical to IALBDX (see Card 10) except that it relates to the foreground local
    # albedo seen by a tilted surface. The list of options is identical to that of IALBDG and thus
    # extends from 1 to 64 (new).
    # TILT: Tilt angle of the receiving surface (0 to 90 decimal deg.); e.g. 90.0 for a vertical
    # plane. Use -999 for a sun-tracking surface.
    # WAZIM: Surface azimuth (0 to 360 decimal deg.) counted clockwise from North; e.g., 270
    # deg. for a surface facing West. Use -999 for a sun-tracking surface.
    
    IALBDG = IALBDX 
    TILT = '0.0'
    WAZIM = '180.0'
    
    # Card 10d:
    # RHOG: Local broadband Lambertian foreground albedo (for tilted plane calculations), Card
    # 10d (if IALBDG = -1); usually between 0.05 and 0.90.
    RHOG = ''
    
    ## Card 11: Spectral range for all Calculations
    WLMN = min_wvl #Min wavelength
    WLMX = max_wvl #Max wavelength
    SUNCOR = '1.0' 
        #Correction factor for irradiance is a correction factor equal to the inverse squared actual radius vector, or true Sun-Earth
        # distance; e.g., SUNCOR = 1.024.
        # SUNCOR varies naturally between 0.966 and 1.034, adding 3.4% to the irradiance in January
        # and reducing it by 3.4% in July. It is calculated by the program if the solar position is calculated
        # from date & time, i.e., if IMASS = 3 on Card 17, thus overwriting the input SUNCOR value on
        # Card 11. If solar position is directly input instead (IMASS = 3), SUNCOR should be set to 1.0 if
        # the average extraterrestrial irradiance (or solar constant, see SOLARC) is to be used, or to any
        # other number between 0.966 and 1.034 to correct it for distance if so desired.

    SOLARC = '1367.0' #Solar constant
    
    
    ## Card 12: Output results selection:
    # IPRT is an option to select the results to be printed on Files 16 and 17. Only broadband results are
    # output (to File 16) if IPRT = 0. Spectral results are added to File 16,
    # and Card 12a is read, if IPRT = 1. Spectral results are rather printed to
    # File 17 (in a spreadsheet-like format) if IPRT = 2. Finally, spectral
    # results are printed to both File 16 and 17 if IPRT = 3. Cards 
    # 12b and 12c are read if IPRT = 2 or 3 (see IOTOT and IOUT).
    
    IPRT = '2'
    
    # Card 12a: Min, Max and Step wavelength (nm) (Output can be different than
    # calculation...
    WPMN = WLMN
    WPMX = WLMX
    INTVL = '.5'
    
    # Card 12b: Total number of output variables:
    #IOTOT = XXX #This is determined with the input of this function
    
    # Card 12c: Variables to output selection 
    #(space separated numbers 1-43 according to the table below:
    #IOUT = '30 31'
    
    
    ## Card 13: Circumsolar Calculation
    # ICIRC is an option controlling the calculation of circumsolar radiation, which is useful when
    # simulating any type of radiometer (spectral or broadband) equipped with a collimator.
    # ICIRC = 0 bypasses these calculations.
    # ICIRC = 1 indicates that a typical radiometer needs to be simulated. The geometry of its collimator
    # must then defined on Card 13a.
    
    ICIRC = '0'
    
    #Card 13a (if ICIRC = 1): SLOPE, APERT, LIMIT
    SLOPE = ''
    APERT = ''
    LIMIT = ''
    
    ## Card 14 Option for using the scanning/smoothing virtual filter of the postprocessor.
    # The smoothed results are output on a spreadsheet-ready file, File 18 (``smarts295.scn.txt``). This postprocessor is
    # activated if ISCAN = 1, not if ISCAN = 0. Card 14a is read if ISCAN = 1.
    
    ISCAN = '0'
    
    # Card 14a (if ISCAN = 1): IFILT, WV1, WV2, STEP, FWHM
    IFILT = ''
    WV1 = ''
    WV2 = ''
    STEP = ''
    FWHM = ''
    
    ## Card 15 ILLUM: Option for illuminance, luminous efficacy and photosynthetically active radiation (PAR)
    # calculations. These calculations take place if ILLUM = -1, 1, -2 or 2, and are bypassed if ILLUM = 0.
    # With ILLUM = -1 or 1, illuminance calculations are based on the CIE photopic curve (or Vlambda
    # curve) of 1924, as supplied in File ``VLambda.dat``. With ILLUM = -2 or 2, the same calculations are
    # done but the revised CIE photopic curve of 1988 is rather used (from File ``VMLambda.dat``). Note
    # that selecting ILLUM = 1 or -1 will override WLMN and WLMX (see Card 11) so that calculations
    # are done between at least 360 and 830 nm.
    # Moreover, if ILLUM = 1 or 2, luminous efficacy calculations are added to the illuminance
    # calculations. This overrides the values of WLMN and WLMX on Card 11, and replaces them by 280
    # and 4000, respectively.
    
    ILLUM = '0'
    
    ## Card  16: Option for special broadband UV calculations. Select IUV = 0 for no special UV calculation, 
    # IUV = 1 to initiate such calculations. These include UVA, UVB, UV index, and
    # different action weighted irradiances of interest in photobiology.
    # Note that IUV = 1 overrides WLMN and WLMX so that calculations are done between at least 280
    # and 400 nm. The spectral results are also printed between at least 280 and 400 nm, irrespective of
    # the IPRT, WPMN, and WPMX values.
    
    IUV = '0'
    
    ## Card 17:
    # Option for solar position and air mass calculations. Set IMASS to:
    # 0, if inputs are to be ZENIT, AZIM on Card 17a
    # 1, if inputs are to be ELEV, AZIM on Card 17a
    # 2, if input is to be AMASS on Card 17a
    # 3, if inputs are to be YEAR, MONTH, DAY, HOUR, LATIT, LONGIT, ZONE on Card 17a
    # 4, if inputs are to be MONTH, LATIT, DSTEP on Card 17a (for a daily calculation).
    IMASS = '0'

    
    # Card 17a: IMASS = 0 Zenith and azimuth
    #ZENITH = ''
    #AZIM = ''
    
    # Card 17a: IMASS = 1 Elevation and Azimuth
    ELEV = ''
    
    # Card 17a: IMASS = 2 Input air mass directly
    AMASS = ''
    
    # Card 17a: IMASS = 3 Input date, time and coordinates
    YEAR = ''
    MONTH = ''
    DAY = ''
    HOUR = ''
    LATIT = ''
    LONGIT = ''
    ZONE = ''
    
    # Card 17a: IMASS = 4 Input Moth, Latitude and DSTEP
    DSTEP = ''

    output = _smartsAll(CMNT, ISPR, SPR, ALTIT, HEIGHT, LATIT, IATMOS, ATMOS, RH, TAIR, SEASON, TDAY, IH2O, W, IO3, IALT, AbO3, IGAS, ILOAD, ApCH2O, ApCH4, ApCO, ApHNO2, ApHNO3, ApNO,ApNO2, ApNO3, ApO3, ApSO2, qCO2, ISPCTR, AEROS, ALPHA1, ALPHA2, OMEGL, GG, ITURB, TAU5, BETA, BCHUEP, RANGE, VISI, TAU550, IALBDX, RHOX, ITILT, IALBDG,TILT, WAZIM,  RHOG, WLMN, WLMX, SUNCOR, SOLARC, IPRT, WPMN, WPMX, INTVL, IOUT, ICIRC, SLOPE, APERT, LIMIT, ISCAN, IFILT, WV1, WV2, STEP, FWHM, ILLUM,IUV, IMASS, ZENITH, AZIM, ELEV, AMASS, YEAR, MONTH, DAY, HOUR, LONGIT, ZONE, DSTEP)

    return output



def SMARTSTMY3(IOUT,YEAR,MONTH,DAY,HOUR, LATIT, LONGIT, ALTIT, ZONE, RHOG,
               W, RH, TAIR, SEASON, TDAY, SPR, HEIGHT='0',
               material='DryGrass', min_wvl='280', max_wvl='4000'):

    r'''
    This function calculates the spectral albedo for a given material. If no 
    material is provided, the function will return a list of all valid 
    materials.

    Parameters
    ----------
    material : string
        Unique identifier for ground cover. Pass None to retreive a list of
        all valid materials.
    WLMN : string
        Minimum wavelength to retreive
    WLMX : string
        Maximum wavelength to retreive
    YEAR : string
        Year
    MONTH : string
        Month
    DAY : string
        Day
    HOUR : string
        Hour, in 24 hour format.
    LATIT : string
        Latitude of the location.
    LONGIT : string
        Longitude of the location.
    ALTIT : string
        elevation of the ground surface above sea level [km].
        WARNING: Please note that TMY3 data is in meters, convert before using this
        function.
    ZONE : string
        Timezone
    RHOG : string
        Local broadband Lambertian foreground albedo (for tilted plane calculations)
    W : string
        Precipitable water above the site altitude, in units of cm or equivalently
        g/cm2/
    RH : string
        Relative Humidity
    TAIR : string
        Temperature.
    SEASON : string
        Season, either 'WINTER' or 'SUMMER'. If Spring, use 'SUMMER'. If
        Autumn, use 'WINTER'.
    TDAY : string
        Average of the day's temperature.        
    HEIGHT : string
        Altitude of the simulated object over the surface, in km.
    SPR : string
        Site pressure, in mbars.
        
    Returns
    -------
    data : pandas
        Matrix with first column representing wavelength (in nm) and second
        column representing albedo of specified material at the wavelength
    
    '''

    if float(ALTIT) > 800:
        print("Altitude should be in km. Are you in Mt. Everest or above or",
              "using meters? This might fail but we'll attempt to continue.")
    
    ## Card 1: Comment. 64 characters max. In theory no spaces but yes underscores.
    CMNT = 'TMY Parameters Spectra'
    
    ## Card 2: ISPR is an option for site's pressure.
    # ISPR = 0 to input SPR on Card 2a
    # ISPR = 1 to input SPR, ALTIT and HEIGHT on Card 2a
    # ISPR = 2 to input LATIT, ALTIT and HEIGHT on Card 2a.
    ISPR = '1'
    
    # Card 2a (if ISPR = 0): SPR
    SPR = SPR #mbar
    
    # Card 2a (if ISPR = 1): SPR, ALTIT, HEIGHT
    # SPR: Surface pressure (mb).
    # ALTIT: Site's altitude, i.e., elevation of the ground surface above sea level (km); must be
    # <= 100 km. In case of a flying object, ALTIT refers to the ground surface below it.
    # HEIGHT: Height of the simulated object above the ground surface underneath (km); must be
    # <= 100 km (new input).
    # The total ALTIT + HEIGHT is the altitude of the simulated object above sea level and
    # must be <= 100 km.
    
    # Card 2a (if ISPR = 2): LATIT, ALTIT, HEIGHT
    # LATIT: Site's latitude (decimal degrees, positive North, negative South); e.g., -17.533 for
    # Papeete, Tahiti. If LATIT is unknown, enter 45.0.
    # ALTIT: Site's altitude, i.e., elevation of the ground surface above sea level (km); must be
    # <= 100 km. In case of a flying object, ALTIT refers to the ground surface below it.
    # HEIGHT: Height of the simulated object above the ground surface underneath (km); must be
    # <= 100 km (new input).
    # The total ALTIT + HEIGHT is the altitude of the simulated object above sea level and
    # must be <= 100 km.
    
    ALTIT = ALTIT
    HEIGHT = HEIGHT
    #LATIT = LATIT 

    ## Card 3: IATMOS is an option to select the proper default atmosphere
    # Its value can be either 0 or 1.
    # Set IATMOS = 0 to define a realistic (i.e., non-reference) atmosphere. Card 3a will then have to
    # provide TAIR, RH, SEASON, TDAY.
    # Set IATMOS = 1 to select one of 10 default reference atmospheres (i.e., for ideal conditions). The
    # shortened name of this atmosphere must be provided by ATMOS on Card 3a.
    
    IATMOS = '0'
    
    # Card 3a (if IATMOS = 1): ATMOS
    # ATMOS is the name of the selected reference atmosphere; 4 characters max. This name can
    # be one of the following: 
    #    USSA   (U.S. Standard Atmosphere)   MLS   (Mid-Latitude Summer) 
    #    MLW   (Mid-Latitude Winter)   SAS   (Sub-Arctic Summer) 
    #   SAW   (Sub-Arctic Winter)   TRL   (Tropical)   STS   (Sub-Tropical Summer)
    #   STW   (Sub-Tropical Winter)   AS   (Arctic Summer)   AW   (Arctic Winter)
    
    ATMOS = 'USSA'
    
    # Card 3a(if IATMOS = 0): TAIR, RH, SEASON, TDAY.
    # RH: Relative humidity at site level (%).
    # SEASON: Can be either `WINTER` or `SUMMER`, for calculation of precipitable water and
    # stratospheric temperature. If the true season is Fall, select WINTER. Select SUMMER if the
    # true season is Spring. SEASON slightly affects the ozone effective temperature and the
    # aerosol optical characteristics.
    # TAIR: Atmospheric temperature at site level (°C). Acceptable range: -120 < TAIR < 50.
    # TDAY: Average daily temperature at site level (°C). For a flying object (HEIGHT > 0), this
    # is a reference temperature for various calculations, therefore it is important to provide a
    # realistic value in this case in particular. Acceptable range: -120 < TDAY < 50.
    
    RH = RH
    TAIR = TAIR
    SEASON = SEASON
    TDAY = TDAY
    
    ## Card 4: IH2O is an option to select the correct water vapor data. All water vapor calculations involve
    # precipitable water, W. The following values of IH2O are possible:
    # 0, to input W on Card 4a
    # 1, if W is to be defaulted to a value prescribed by the selected reference atmosphere and the site
    # altitude (thus if IATMOS = 1 on Card 3). If IATMOS != 1, USSA will be defaulted for this step.
    # 2, if W is to be calculated by the program from TAIR and RH (thus if IATMOS = 0 on Card 3). This
    # calculation is only approximate (particularly if HEIGHT > 0) and therefore this option is not
    # recommended.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    
    IH2O = '0'
    
    # Card 4a: (if IH2O = 0): W is precipitable water above the site altitude
    # in units of cm, or equivalently, g/cm2; it must be <= 12.
    
    W = W
    
    if float(W) == 0 or float(W) > 12:
        print("Switching to calculating W")
        IH2O = '2'
        
    
    ## Card 5: IO3 is an option to select the appropriate ozone abundance input.
    # IO3 = 0 to input IALT and AbO3 on Card 5a
    # IO3 = 1 to use a default value for AbO3 according to the reference atmosphere selected by
    # IATMOS. If IATMOS != 1, USSA will be defaulted for this calculation.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    IO3 = '1'

    # Card 5a (if IO3 = 0): IALT, AbO3
    # IALT is an option to select the appropriate ozone column altitude correction.
    # IALT = 0 bypasses the altitude correction, so that the value of AbO3 on
    # Card 5a is used as is. IALT = 1 should be rather used if a vertical
    # profile correction needs to be applied (in case of an elevated site when
    # the value of AbO3 is known only at sea level). 
    
    IALT = ''
    AbO3 = ''
    
    ## Card 6 IGAS is an option to define the correct conditions for gaseous absorption and atmospheric pollution. 
    # IGAS = 0 if ILOAD on Card 6a is to be read so that extra gaseous absorption calculations
    # (corresponding to the gas load in the lower troposphere due to pollution or absence thereof) can be
    # initiated;
    # IGAS =1 if all gas abundances (except carbon dioxide, ozone and water vapor see Cards 4a, 5a,
    # and 7) are to be defaulted, using average vertical profiles.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    
    IGAS = '0'
    
    # Card 6a  (if IGAS = 0): ILOAD is an option for tropospheric pollution, only used if IGAS = 0.
    # For ILOAD = 0, Card 6b will be read with the concentrations of 10 pollutants.
    # ILOAD = 1 selects default PRISTINE ATMOSPHERIC conditions, leading to slightly
    # reduced abundances of some gases compared to the initial default obtained with the selected
    # reference atmosphere.
    # Setting ILOAD to 2-4 will increase the concentration of the 10 pollutants to possibly
    # represent typical urban conditions: LIGHT POLLUTION (ILOAD = 2), MODERATE
    # POLLUTION (ILOAD = 3), and SEVERE POLLUTION (ILOAD = 4).
    
    ILOAD = '1'
    
    # Card 6b (if IGAS = 0 and ILOAD = 0): ApCH2O, ApCH4, ApCO, ApHNO2,
    # ApHNO3, ApNO, ApNO2, ApNO3, ApO3, ApSO2
    # ApCH2O: Formaldehyde volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApCH4: Methane volumetric concentration in the assumed 1-km deep tropospheric pollution
    # layer (ppmv).
    # ApCO: Carbon monoxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv), Card 6b.
    # ApHNO2: Nitrous acid volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApHNO3: Nitric acid volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO: Nitric oxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO2: Nitrogen dioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO3: Nitrogen trioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApO3: Ozone volumetric concentration in the assumed 1-km deep tropospheric pollution
    # layer (ppmv).
    # ApSO2: Sulfur dioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    
    ApCH2O = ''
    ApCH4 = ''
    ApCO = ''
    ApHNO2 = ''
    ApHNO3 = ''
    ApNO = ''
    ApNO2 = ''
    ApNO3 = ''
    ApO3 = ''
    ApSO2 =''
    
    ## Card 7 qCO2 carbon dioxide columnar volumetric concentration (ppmv).
    qCO2 = '0.0'
    
    # Card 7a ISPCTR 
    # is an option to select the proper extraterrestrial
    # spectrum. This option allows to choose one out of ten possible spectral
    # files (``Spctrm_n.dat``, where n = 0-8 or n = U).
    # -1  Spctrm_U.dat  N/A User User
    # 0  Spctrm_0.dat  N/A Gueymard, 2004 (synthetic) 1366.10
    # 1  Spctrm_1.dat  N/A Gueymard, unpublished (synthetic) 1367.00
    # 2  Spctrm_2.dat  cebchkur MODTRAN, Cebula/Chance/Kurucz 1362.12
    # 3  Spctrm_3.dat  chkur MODTRAN, Chance/Kurucz 1359.75
    # 4  Spctrm_4.dat  newkur MODTRAN, New Kurucz 1368.00
    # 5  Spctrm_5.dat  oldkur MODTRAN, Old Kurucz 1373.16
    # 6  Spctrm_6.dat  thkur MODTRAN, Thuillier/Kurucz 1376.23
    # 7  Spctrm_7.dat  MODTRAN2 Wehrli/WRC/WMO, 1985 1367.00
    # 8  Spctrm_8.dat  N/A ASTM E490, 2000 (synthetic) 1366.10
    
    ISPCTR ='0'
    
    ## Card 8: AEROS selects the aerosol model, with one of the following twelve possible choices:
    #  S&F_RURAL ,  S&F_URBAN ,  S&F_MARIT ,  S&F_TROPO , These four choices
    # refer respectively to the Rural, Urban, Maritime and Tropospheric aerosol
    # models (Shettle and Fenn, 1979), which are humidity dependent and common with MODTRAN. 
    #  SRA_CONTL ,  SRA_URBAN ,  SRA_MARIT , These three choices refer
    # respectively to the Continental, Urban, and Maritime aerosol models of
    # the IAMAP preliminary standard atmosphere (IAMAP, 1986). 
    #  B&D_C ,  B&D_C1 , These two choices refer respectively to the Braslau &
    # Dave aerosol type C and C1, themselves based on Deirmendjian's Haze L model. 
    #  DESERT_MIN ,  DESERT_MAX  DESERT_MIN corresponds to background (normal)
    # conditions in desert areas, whereas DESERT_MAX corresponds to extremely
    # turbid conditions (sandstorms).  
    # 'USER' Card 8a is then necessary to input user-supplied aerosol information.
    
    AEROS = 'S&F_TROPO' 
    # Card 8a: 
    # if AEROS =  USER : ALPHA1, ALPHA2, OMEGL, GG These 4 variables must represent broadband average values only!
    # ALPHA1: Average value of Ångström's wavelength exponent $\alpha$ for wavelengths < 500 nm
    # (generally between 0.0 and 2.6).
    # ALPHA2: Average value of Ångström's wavelength exponent $\alpha$ for wavelengths >= 500 nm
    # (generally between 0.0 and 2.6).
    # OMEGL: Aerosol single scattering albedo (generally between 0.6 and 1.0).
    # GG: Aerosol asymmetry parameter (generally between 0.5 and 0.9).
    ALPHA1 = ''
    ALPHA2 = ''
    OMEGL = ''
    GG = ''
    
    ## Card 9: ITURB is an option to select the correct turbidity data input. The different options are:
    # 0, to read TAU5 on Card 9a
    # 1, to read BETA on Card 9a
    # 2, to read BCHUEP on Card 9a
    # 3, to read RANGE on Card 9a
    # 4, to read VISI on Card 9a
    # 5, to read TAU550 on Card 9a (new option).
    
    ITURB = '0'
    
    #Card 9a Turbidity value
    TAU5 = '0.00' #if ITURB == 0
    BETA = '' #if ITURB == 1
    BCHUEP = '' #if ITURB == 2
    RANGE = '' #if ITURB == 3
    VISI = '' #if ITURB == 4
    TAU550 = '' #if ITURB == 5
    
    ## Card 10: Far Field Albedo for backscattering
    IALBDX = _material_to_code(material)
    
    # Card 10a:
    RHOX = ''
                            # Zonal broadband Lambertian ground albedo (for backscattering calculations); must
                            # be between 0 and 1.
                            
    # Card 10b: ITILT is an option for tilted surface calculations. 
    #Select ITILT= 0 for no such calculation, 
    #ITILT = 1 to initiate these calculations using information on Card 10c.
    ITILT = '1'
    
    # Card 10c:
    # IALBDG is identical to IALBDX (see Card 10) except that it relates to the foreground local
    # albedo seen by a tilted surface. The list of options is identical to that of IALBDG and thus
    # extends from 1 to 64 (new).
    # TILT: Tilt angle of the receiving surface (0 to 90 decimal deg.); e.g. 90.0 for a vertical
    # plane. Use -999 for a sun-tracking surface.
    # WAZIM: Surface azimuth (0 to 360 decimal deg.) counted clockwise from North; e.g., 270
    # deg. for a surface facing West. Use -999 for a sun-tracking surface.
    
    IALBDG = '-1' #Sil check if this should be -1 or 1.
    TILT = '0.0'
    WAZIM = '180.0'
    
    # Card 10d:
    # RHOG: Local broadband Lambertian foreground albedo (for tilted plane calculations), Card
    # 10d (if IALBDG = -1); usually between 0.05 and 0.90.
    RHOG = RHOG
    
    ## Card 11: Spectral range for all Calculations
    WLMN = min_wvl #Min wavelength
    WLMX = max_wvl #Max wavelength
    SUNCOR = '1.0' 
        #Correction factor for irradiance is a correction factor equal to the inverse squared actual radius vector, or true Sun-Earth
        # distance; e.g., SUNCOR = 1.024.
        # SUNCOR varies naturally between 0.966 and 1.034, adding 3.4% to the irradiance in January
        # and reducing it by 3.4% in July. It is calculated by the program if the solar position is calculated
        # from date & time, i.e., if IMASS = 3 on Card 17, thus overwriting the input SUNCOR value on
        # Card 11. If solar position is directly input instead (IMASS = 3), SUNCOR should be set to 1.0 if
        # the average extraterrestrial irradiance (or solar constant, see SOLARC) is to be used, or to any
        # other number between 0.966 and 1.034 to correct it for distance if so desired.

    SOLARC = '1367.0' #Solar constant
    
    
    ## Card 12: Output results selection:
    # IPRT is an option to select the results to be printed on Files 16 and 17. Only broadband results are
    # output (to File 16) if IPRT = 0. Spectral results are added to File 16,
    # and Card 12a is read, if IPRT = 1. Spectral results are rather printed to
    # File 17 (in a spreadsheet-like format) if IPRT = 2. Finally, spectral
    # results are printed to both File 16 and 17 if IPRT = 3. Cards 
    # 12b and 12c are read if IPRT = 2 or 3 (see IOTOT and IOUT).
    IPRT = '2'
    
    # Card 12a: Min, Max and Step wavelength (nm) (Output can be different than
    # calculation...
    WPMN = WLMN
    WPMX = WLMX
    INTVL = '.5'
    
    # Card 12b: Total number of output variables:
    #IOTOT = XXX #This is determined with the input of this function
    
    # Card 12c: Variables to output selection 
    #(space separated numbers 1-43 according to the table below:
    #IOUT = '30 31'
    
    
    ## Card 13: Circumsolar Calculation
    # ICIRC is an option controlling the calculation of circumsolar radiation, which is useful when
    # simulating any type of radiometer (spectral or broadband) equipped with a collimator.
    # ICIRC = 0 bypasses these calculations.
    # ICIRC = 1 indicates that a typical radiometer needs to be simulated. The geometry of its collimator
    # must then defined on Card 13a.
    
    ICIRC = '0'
    
    #Card 13a (if ICIRC = 1): SLOPE, APERT, LIMIT
    SLOPE = ''
    APERT = ''
    LIMIT = ''
    
    ## Card 14 Option for using the scanning/smoothing virtual filter of the postprocessor.
    # The smoothed results are output on a spreadsheet-ready file, File 18 (``smarts295.scn.txt``). This postprocessor is
    # activated if ISCAN = 1, not if ISCAN = 0. Card 14a is read if ISCAN = 1.
    
    ISCAN = '0'
    
    # Card 14a (if ISCAN = 1): IFILT, WV1, WV2, STEP, FWHM
    IFILT = ''
    WV1 = ''
    WV2 = ''
    STEP = ''
    FWHM = ''
    
    ## Card 15 ILLUM: Option for illuminance, luminous efficacy and photosynthetically active radiation (PAR)
    # calculations. These calculations take place if ILLUM = -1, 1, -2 or 2, and are bypassed if ILLUM = 0.
    # With ILLUM = -1 or 1, illuminance calculations are based on the CIE photopic curve (or Vlambda
    # curve) of 1924, as supplied in File ``VLambda.dat``. With ILLUM = -2 or 2, the same calculations are
    # done but the revised CIE photopic curve of 1988 is rather used (from File ``VMLambda.dat``). Note
    # that selecting ILLUM = 1 or -1 will override WLMN and WLMX (see Card 11) so that calculations
    # are done between at least 360 and 830 nm.
    # Moreover, if ILLUM = 1 or 2, luminous efficacy calculations are added to the illuminance
    # calculations. This overrides the values of WLMN and WLMX on Card 11, and replaces them by 280
    # and 4000, respectively.
    
    ILLUM = '0'
    
    ## Card  16: Option for special broadband UV calculations. Select IUV = 0 for no special UV calculation, 
    # IUV = 1 to initiate such calculations. These include UVA, UVB, UV index, and
    # different action weighted irradiances of interest in photobiology.
    # Note that IUV = 1 overrides WLMN and WLMX so that calculations are done between at least 280
    # and 400 nm. The spectral results are also printed between at least 280 and 400 nm, irrespective of
    # the IPRT, WPMN, and WPMX values.
    
    IUV = '0'
    
    ## Card 17:
    # Option for solar position and air mass calculations. Set IMASS to:
    # 0, if inputs are to be ZENIT, AZIM on Card 17a
    # 1, if inputs are to be ELEV, AZIM on Card 17a
    # 2, if input is to be AMASS on Card 17a
    # 3, if inputs are to be YEAR, MONTH, DAY, HOUR, LATIT, LONGIT, ZONE on Card 17a
    # 4, if inputs are to be MONTH, LATIT, DSTEP on Card 17a (for a daily calculation).
    IMASS = '3'

    
    # Card 17a: IMASS = 0 Zenith and azimuth
    ZENITH = ''
    AZIM = ''
    
    # Card 17a: IMASS = 1 Elevation and Azimuth
    ELEV = ''
    
    # Card 17a: IMASS = 2 Input air mass directly
    AMASS = ''
    
    # Card 17a: IMASS = 3 Input date, time and coordinates
    YEAR = YEAR
    MONTH = MONTH
    DAY = DAY
    HOUR = HOUR
    LATIT = LATIT
    LONGIT = LONGIT
    ZONE = ZONE
    
    # Card 17a: IMASS = 4 Input Moth, Latitude and DSTEP
    DSTEP = ''

    output = _smartsAll(CMNT, ISPR, SPR, ALTIT, HEIGHT, LATIT, IATMOS, ATMOS, RH, TAIR, SEASON, TDAY, IH2O, W, IO3, IALT, AbO3, IGAS, ILOAD, ApCH2O, ApCH4, ApCO, ApHNO2, ApHNO3, ApNO,ApNO2, ApNO3, ApO3, ApSO2, qCO2, ISPCTR, AEROS, ALPHA1, ALPHA2, OMEGL, GG, ITURB, TAU5, BETA, BCHUEP, RANGE, VISI, TAU550, IALBDX, RHOX, ITILT, IALBDG,TILT, WAZIM,  RHOG, WLMN, WLMX, SUNCOR, SOLARC, IPRT, WPMN, WPMX, INTVL, IOUT, ICIRC, SLOPE, APERT, LIMIT, ISCAN, IFILT, WV1, WV2, STEP, FWHM, ILLUM,IUV, IMASS, ZENITH, AZIM, ELEV, AMASS, YEAR, MONTH, DAY, HOUR, LONGIT, ZONE, DSTEP)

    return output



def SMARTSSRRL(IOUT,YEAR,MONTH,DAY,HOUR, LATIT, LONGIT, ALTIT, ZONE, 
               W, RH, TAIR, SEASON, TDAY, SPR, TILT, WAZIM,
               RHOG, ALPHA1, ALPHA2, OMEGL, GG, BETA, TAU5, HEIGHT='0', 
               material='DryGrass', min_wvl='280', max_wvl='4000'):

    r'''
    This function calculates the spectral albedo for a given material. If no 
    material is provided, the function will return a list of all valid 
    materials.

    Parameters
    ----------

    YEAR : string
        Year
    MONTH : string
        Month
    DAY : string
        Day
    HOUR : string
        Hour, in 24 hour format.
    LATIT : string
        Latitude of the location.
    LONGIT : string
        Longitude of the location.
    ALTIT : string
        elevation of the ground surface above sea level [km].
        WARNING: Please note that TMY3 data is in meters, convert before using this
        function.
    ZONE : string
        Timezone
    W : string
        Precipitable water above the site altitude, in units of cm or equivalently
        g/cm2/
    RH : string
        Relative Humidity
    TAIR : string
        Temperature.
    SEASON : string
        Season, either 'WINTER' or 'SUMMER'. If Spring, use 'SUMMER'. If
        Autumn, use 'WINTER'.
    TDAY : string
        Average of the day's temperature.        
    HEIGHT : string
        Altitude of the simulated object over the surface, in km.
    SPR : string
        Site pressure, in mbars.
    BETA : string
        Ångström’s turbidity coefficient, ß (i.e., aerosol optical depth at 1000 nm)
        If BETA and TAU5 are used as inputs, BETA is selected as priority since
        TAU5 would be used to calcualte an internal SMARTS BETA value.
    TAU5 : string
        Aerosol optical depth at 500 nm, τ5.
        If BETA and TAU5 are used as inputs, BETA is selected as priority since
        TAU5 would be used to calcualte an internal SMARTS BETA value.
    TILT : string
        Tilt angel of the receiving surface (0 to 90 decimal deg.), e.g. 90.0
        for a vertical plane. Use -999 for a sun-tracking surface.
    WAZIM : string
        Surface azimuth (0 to 360 decimal deg.) counted clockwise from North;
        e.g., 270 deg. for a surface facing West. Use -999 for a sun-tracking
        surface.
    RHOG : string
        Local broadband Lambertian foreground albedo (for tilted plane calculations),
        usually between 0.05 and 0.90.
        For SRRL Data, this is 
    material : string
        Unique identifier for ground cover. Pass None to retreive a list of
        all valid materials.
    WLMN : string
        Minimum wavelength to retreive
    WLMX : string
        Maximum wavelength to retreive

    Returns
    -------
    data : pandas
        Matrix with first column representing wavelength (in nm) and second
        column representing albedo of specified material at the wavelength
    
    '''

    if float(ALTIT) > 800:
        print("Altitude should be in km. Are you in Mt. Everest or above or",
              "using meters? This might fail but we'll attempt to continue.")
    
    ## Card 1: Comment. 64 characters max. In theory no spaces but yes underscores.
    CMNT = 'SRRL Spectra'    
    
    ## Card 2: ISPR is an option for site's pressure.
    # ISPR = 0 to input SPR on Card 2a
    # ISPR = 1 to input SPR, ALTIT and HEIGHT on Card 2a
    # ISPR = 2 to input LATIT, ALTIT and HEIGHT on Card 2a.
    ISPR = '1'
    
    # Card 2a (if ISPR = 0): SPR
    SPR = SPR #mbar
    
    # Card 2a (if ISPR = 1): SPR, ALTIT, HEIGHT
    # SPR: Surface pressure (mb).
    # ALTIT: Site's altitude, i.e., elevation of the ground surface above sea level (km); must be
    # <= 100 km. In case of a flying object, ALTIT refers to the ground surface below it.
    # HEIGHT: Height of the simulated object above the ground surface underneath (km); must be
    # <= 100 km (new input).
    # The total ALTIT + HEIGHT is the altitude of the simulated object above sea level and
    # must be <= 100 km.
    
    # Card 2a (if ISPR = 2): LATIT, ALTIT, HEIGHT
    # LATIT: Site's latitude (decimal degrees, positive North, negative South); e.g., -17.533 for
    # Papeete, Tahiti. If LATIT is unknown, enter 45.0.
    # ALTIT: Site's altitude, i.e., elevation of the ground surface above sea level (km); must be
    # <= 100 km. In case of a flying object, ALTIT refers to the ground surface below it.
    # HEIGHT: Height of the simulated object above the ground surface underneath (km); must be
    # <= 100 km (new input).
    # The total ALTIT + HEIGHT is the altitude of the simulated object above sea level and
    # must be <= 100 km.
    
    ALTIT = ALTIT
    HEIGHT = HEIGHT
    #LATIT = LATIT
    
    ## Card 3: IATMOS is an option to select the proper default atmosphere
    # Its value can be either 0 or 1.
    # Set IATMOS = 0 to define a realistic (i.e., non-reference) atmosphere. Card 3a will then have to
    # provide TAIR, RH, SEASON, TDAY.
    # Set IATMOS = 1 to select one of 10 default reference atmospheres (i.e., for ideal conditions). The
    # shortened name of this atmosphere must be provided by ATMOS on Card 3a.
    
    IATMOS = '0'
    
    # Card 3a (if IATMOS = 1): ATMOS
    # ATMOS is the name of the selected reference atmosphere; 4 characters max. This name can
    # be one of the following: 
    #    USSA   (U.S. Standard Atmosphere)   MLS   (Mid-Latitude Summer) 
    #    MLW   (Mid-Latitude Winter)   SAS   (Sub-Arctic Summer) 
    #   SAW   (Sub-Arctic Winter)   TRL   (Tropical)   STS   (Sub-Tropical Summer)
    #   STW   (Sub-Tropical Winter)   AS   (Arctic Summer)   AW   (Arctic Winter)
    
    ATMOS = 'USSA'
    
    # Card 3a(if IATMOS = 0): TAIR, RH, SEASON, TDAY.
    # RH: Relative humidity at site level (%).
    # SEASON: Can be either `WINTER` or `SUMMER`, for calculation of precipitable water and
    # stratospheric temperature. If the true season is Fall, select WINTER. Select SUMMER if the
    # true season is Spring. SEASON slightly affects the ozone effective temperature and the
    # aerosol optical characteristics.
    # TAIR: Atmospheric temperature at site level (°C). Acceptable range: -120 < TAIR < 50.
    # TDAY: Average daily temperature at site level (°C). For a flying object (HEIGHT > 0), this
    # is a reference temperature for various calculations, therefore it is important to provide a
    # realistic value in this case in particular. Acceptable range: -120 < TDAY < 50.
    
    RH = RH
    TAIR = TAIR
    SEASON = SEASON
    TDAY = TDAY
    
    ## Card 4: IH2O is an option to select the correct water vapor data. All water vapor calculations involve
    # precipitable water, W. The following values of IH2O are possible:
    # 0, to input W on Card 4a
    # 1, if W is to be defaulted to a value prescribed by the selected reference atmosphere and the site
    # altitude (thus if IATMOS = 1 on Card 3). If IATMOS != 1, USSA will be defaulted for this step.
    # 2, if W is to be calculated by the program from TAIR and RH (thus if IATMOS = 0 on Card 3). This
    # calculation is only approximate (particularly if HEIGHT > 0) and therefore this option is not
    # recommended.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    
    IH2O = '0'
    
    # Card 4a: (if IH2O = 0): W is precipitable water above the site altitude
    # in units of cm, or equivalently, g/cm2; it must be <= 12.
    
    W = W
    
    ## Card 5: IO3 is an option to select the appropriate ozone abundance input.
    # IO3 = 0 to input IALT and AbO3 on Card 5a
    # IO3 = 1 to use a default value for AbO3 according to the reference atmosphere selected by
    # IATMOS. If IATMOS != 1, USSA will be defaulted for this calculation.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    IO3 = '1'

    # Card 5a (if IO3 = 0): IALT, AbO3
    # IALT is an option to select the appropriate ozone column altitude correction.
    # IALT = 0 bypasses the altitude correction, so that the value of AbO3 on
    # Card 5a is used as is. IALT = 1 should be rather used if a vertical
    # profile correction needs to be applied (in case of an elevated site when
    # the value of AbO3 is known only at sea level). 
    IALT = ''
    AbO3 = ''
    
    ## Card 6 IGAS is an option to define the correct conditions for gaseous absorption and atmospheric pollution. 
    # IGAS = 0 if ILOAD on Card 6a is to be read so that extra gaseous absorption calculations
    # (corresponding to the gas load in the lower troposphere due to pollution or absence thereof) can be
    # initiated;
    # IGAS =1 if all gas abundances (except carbon dioxide, ozone and water vapor see Cards 4a, 5a,
    # and 7) are to be defaulted, using average vertical profiles.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    
    IGAS = '0'
    
    # Card 6a  (if IGAS = 0): ILOAD is an option for tropospheric pollution, only used if IGAS = 0.
    # For ILOAD = 0, Card 6b will be read with the concentrations of 10 pollutants.
    # ILOAD = 1 selects default PRISTINE ATMOSPHERIC conditions, leading to slightly
    # reduced abundances of some gases compared to the initial default obtained with the selected
    # reference atmosphere.
    # Setting ILOAD to 2-4 will increase the concentration of the 10 pollutants to possibly
    # represent typical urban conditions: LIGHT POLLUTION (ILOAD = 2), MODERATE
    # POLLUTION (ILOAD = 3), and SEVERE POLLUTION (ILOAD = 4).
    
    ILOAD = '1'
    
    # Card 6b (if IGAS = 0 and ILOAD = 0): ApCH2O, ApCH4, ApCO, ApHNO2,
    # ApHNO3, ApNO, ApNO2, ApNO3, ApO3, ApSO2
    # ApCH2O: Formaldehyde volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApCH4: Methane volumetric concentration in the assumed 1-km deep tropospheric pollution
    # layer (ppmv).
    # ApCO: Carbon monoxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv), Card 6b.
    # ApHNO2: Nitrous acid volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApHNO3: Nitric acid volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO: Nitric oxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO2: Nitrogen dioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO3: Nitrogen trioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApO3: Ozone volumetric concentration in the assumed 1-km deep tropospheric pollution
    # layer (ppmv).
    # ApSO2: Sulfur dioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    
    ApCH2O = ''
    ApCH4 = ''
    ApCO = ''
    ApHNO2 = ''
    ApHNO3 = ''
    ApNO = ''
    ApNO2 = ''
    ApNO3 = ''
    ApO3 = ''
    ApSO2 =''
    
    ## Card 7 qCO2 carbon dioxide columnar volumetric concentration (ppmv).
    qCO2 = '0.0'
    
    # Card 7a ISPCTR 
    # is an option to select the proper extraterrestrial
    # spectrum. This option allows to choose one out of ten possible spectral
    # files (``Spctrm_n.dat``, where n = 0-8 or n = U).  
    # -1  Spctrm_U.dat  N/A User User
    # 0  Spctrm_0.dat  N/A Gueymard, 2004 (synthetic) 1366.10
    # 1  Spctrm_1.dat  N/A Gueymard, unpublished (synthetic) 1367.00
    # 2  Spctrm_2.dat  cebchkur MODTRAN, Cebula/Chance/Kurucz 1362.12
    # 3  Spctrm_3.dat  chkur MODTRAN, Chance/Kurucz 1359.75
    # 4  Spctrm_4.dat  newkur MODTRAN, New Kurucz 1368.00
    # 5  Spctrm_5.dat  oldkur MODTRAN, Old Kurucz 1373.16
    # 6  Spctrm_6.dat  thkur MODTRAN, Thuillier/Kurucz 1376.23
    # 7  Spctrm_7.dat  MODTRAN2 Wehrli/WRC/WMO, 1985 1367.00
    # 8  Spctrm_8.dat  N/A ASTM E490, 2000 (synthetic) 1366.10
    
    ISPCTR ='0'
    
    ## Card 8: AEROS selects the aerosol model, with one of the following twelve possible choices:
    #  S&F_RURAL ,  S&F_URBAN ,  S&F_MARIT ,  S&F_TROPO , These four choices
    # refer respectively to the Rural, Urban, Maritime and Tropospheric aerosol
    # models (Shettle and Fenn, 1979), which are humidity dependent and common with MODTRAN. 
    #  SRA_CONTL ,  SRA_URBAN ,  SRA_MARIT , These three choices refer
    # respectively to the Continental, Urban, and Maritime aerosol models of
    # the IAMAP preliminary standard atmosphere (IAMAP, 1986). 
    #  B&D_C ,  B&D_C1 , These two choices refer respectively to the Braslau &
    # Dave aerosol type C and C1, themselves based on Deirmendjian's Haze L model. 
    #  DESERT_MIN ,  DESERT_MAX  DESERT_MIN corresponds to background (normal)
    # conditions in desert areas, whereas DESERT_MAX corresponds to extremely
    # turbid conditions (sandstorms).  
    # 'USER' Card 8a is then necessary to input user-supplied aerosol information.
    
    AEROS = 'USER' #'S&F_TROPO' 
    # Card 8a: 
    # if AEROS =  USER : ALPHA1, ALPHA2, OMEGL, GG These 4 variables must represent broadband average values only!
    # ALPHA1: Average value of Ångström's wavelength exponent $\alpha$ for wavelengths < 500 nm
    # (generally between 0.0 and 2.6).
    # ALPHA2: Average value of Ångström's wavelength exponent $\alpha$ for wavelengths >= 500 nm
    # (generally between 0.0 and 2.6).
    # OMEGL: Aerosol single scattering albedo (generally between 0.6 and 1.0).
    # GG: Aerosol asymmetry parameter (generally between 0.5 and 0.9).
    ALPHA1 = ALPHA1
    ALPHA2 = ALPHA2
    OMEGL = OMEGL
    GG = GG
    
    ## Card 9: ITURB is an option to select the correct turbidity data input. The different options are:
    # 0, to read TAU5 on Card 9a
    # 1, to read BETA on Card 9a
    # 2, to read BCHUEP on Card 9a
    # 3, to read RANGE on Card 9a
    # 4, to read VISI on Card 9a
    # 5, to read TAU550 on Card 9a (new option).
    
    ITURB = '1'
    
    #Card 9a Turbidity value
    if BETA is not None:
        BETA = BETA
        TAU5 = ''
    else:
        TAU5 = TAU5
        BETA = '' 
    BCHUEP = '' #if ITURB == 2
    RANGE = '' #if ITURB == 3
    VISI = '' #if ITURB == 4
    TAU550 = '' #if ITURB == 5
    
    ## Card 10: Far Field Albedo for backscattering
    IALBDX = _material_to_code(material)
    
    # Card 10a:
    RHOX = ''
                            # Zonal broadband Lambertian ground albedo (for backscattering calculations); must
                            # be between 0 and 1.
                            
    # Card 10b: ITILT is an option for tilted surface calculations. 
    #Select ITILT= 0 for no such calculation, 
    #ITILT = 1 to initiate these calculations using information on Card 10c.
    ITILT = '1'
    
    # Card 10c:
    # IALBDG is identical to IALBDX (see Card 10) except that it relates to the foreground local
    # albedo seen by a tilted surface. The list of options is identical to that of IALBDG and thus
    # extends from 1 to 64 (new).
    # TILT: Tilt angle of the receiving surface (0 to 90 decimal deg.); e.g. 90.0 for a vertical
    # plane. Use -999 for a sun-tracking surface.
    # WAZIM: Surface azimuth (0 to 360 decimal deg.) counted clockwise from North; e.g., 270
    # deg. for a surface facing West. Use -999 for a sun-tracking surface.
    
    IALBDG = '-1'
    TILT = TILT
    WAZIM = WAZIM
    
    # Card 10d:
    # RHOG: Local broadband Lambertian foreground albedo (for tilted plane calculations), Card
    # 10d (if IALBDG = -1); usually between 0.05 and 0.90.
    RHOG = RHOG
    
    ## Card 11: Spectral range for all Calculations
    WLMN = min_wvl #Min wavelength
    WLMX = max_wvl #Max wavelength
    SUNCOR = '1.0' 
        #Correction factor for irradiance is a correction factor equal to the inverse squared actual radius vector, or true Sun-Earth
        # distance; e.g., SUNCOR = 1.024.
        # SUNCOR varies naturally between 0.966 and 1.034, adding 3.4% to the irradiance in January
        # and reducing it by 3.4% in July. It is calculated by the program if the solar position is calculated
        # from date & time, i.e., if IMASS = 3 on Card 17, thus overwriting the input SUNCOR value on
        # Card 11. If solar position is directly input instead (IMASS = 3), SUNCOR should be set to 1.0 if
        # the average extraterrestrial irradiance (or solar constant, see SOLARC) is to be used, or to any
        # other number between 0.966 and 1.034 to correct it for distance if so desired.

    SOLARC = '1367.0' #Solar constant
    
    
    ## Card 12: Output results selection:
    # IPRT is an option to select the results to be printed on Files 16 and 17. Only broadband results are
    # output (to File 16) if IPRT = 0. Spectral results are added to File 16,
    # and Card 12a is read, if IPRT = 1. Spectral results are rather printed to
    # File 17 (in a spreadsheet-like format) if IPRT = 2. Finally, spectral
    # results are printed to both File 16 and 17 if IPRT = 3. Cards 
    # 12b and 12c are read if IPRT = 2 or 3 (see IOTOT and IOUT).
    IPRT = '2'
    
    # Card 12a: Min, Max and Step wavelength (nm) (Output can be different than
    # calculation...
    WPMN = WLMN
    WPMX = WLMX
    INTVL = '.5'
    
    # Card 12b: Total number of output variables:
    #IOTOT = XXX #This is determined with the input of this function
    
    # Card 12c: Variables to output selection 
    #(space separated numbers 1-43 according to the table below:
    IOUT = IOUT
    
    
    ## Card 13: Circumsolar Calculation
    # ICIRC is an option controlling the calculation of circumsolar radiation, which is useful when
    # simulating any type of radiometer (spectral or broadband) equipped with a collimator.
    # ICIRC = 0 bypasses these calculations.
    # ICIRC = 1 indicates that a typical radiometer needs to be simulated. The geometry of its collimator
    # must then defined on Card 13a.
    
    ICIRC = '0'
    
    #Card 13a (if ICIRC = 1): SLOPE, APERT, LIMIT
    SLOPE = ''
    APERT = ''
    LIMIT = ''
    
    ## Card 14 Option for using the scanning/smoothing virtual filter of the postprocessor.
    # The smoothed results are output on a spreadsheet-ready file, File 18 (smarts295.scn.txt). This postprocessor is
    # activated if ISCAN = 1, not if ISCAN = 0. Card 14a is read if ISCAN = 1.
    
    ISCAN = '0'
    
    # Card 14a (if ISCAN = 1): IFILT, WV1, WV2, STEP, FWHM
    IFILT = ''
    WV1 = ''
    WV2 = ''
    STEP = ''
    FWHM = ''
    
    ## Card 15 ILLUM: Option for illuminance, luminous efficacy and photosynthetically active radiation (PAR)
    # calculations. These calculations take place if ILLUM = -1, 1, -2 or 2, and are bypassed if ILLUM = 0.
    # With ILLUM = -1 or 1, illuminance calculations are based on the CIE photopic curve (or Vlambda
    # curve) of 1924, as supplied in File ``VLambda.dat``. With ILLUM = -2 or 2, the same calculations are
    # done but the revised CIE photopic curve of 1988 is rather used (from File ``VMLambda.dat``). Note
    # that selecting ILLUM = 1 or -1 will override WLMN and WLMX (see Card 11) so that calculations
    # are done between at least 360 and 830 nm.
    # Moreover, if ILLUM = 1 or 2, luminous efficacy calculations are added to the illuminance
    # calculations. This overrides the values of WLMN and WLMX on Card 11, and replaces them by 280
    # and 4000, respectively.
    
    ILLUM = '0'
    
    ## Card  16: Option for special broadband UV calculations. Select IUV = 0 for no special UV calculation, 
    # IUV = 1 to initiate such calculations. These include UVA, UVB, UV index, and
    # different action weighted irradiances of interest in photobiology.
    # Note that IUV = 1 overrides WLMN and WLMX so that calculations are done between at least 280
    # and 400 nm. The spectral results are also printed between at least 280 and 400 nm, irrespective of
    # the IPRT, WPMN, and WPMX values.
    
    IUV = '0'
    
    ## Card 17:
    # Option for solar position and air mass calculations. Set IMASS to:
    # 0, if inputs are to be ZENIT, AZIM on Card 17a
    # 1, if inputs are to be ELEV, AZIM on Card 17a
    # 2, if input is to be AMASS on Card 17a
    # 3, if inputs are to be YEAR, MONTH, DAY, HOUR, LATIT, LONGIT, ZONE on Card 17a
    # 4, if inputs are to be MONTH, LATIT, DSTEP on Card 17a (for a daily calculation).
    IMASS = '3'

    
    # Card 17a: IMASS = 0 Zenith and azimuth
    ZENITH = ''
    AZIM = ''
    
    # Card 17a: IMASS = 1 Elevation and Azimuth
    ELEV = ''
    
    # Card 17a: IMASS = 2 Input air mass directly
    AMASS = ''
    
    # Card 17a: IMASS = 3 Input date, time and coordinates
    YEAR = YEAR
    MONTH = MONTH
    DAY = DAY
    HOUR = HOUR
    LATIT = LATIT
    LONGIT = LONGIT
    ZONE = ZONE
    
    # Card 17a: IMASS = 4 Input Moth, Latitude and DSTEP
    DSTEP = ''

    output = _smartsAll(CMNT, ISPR, SPR, ALTIT, HEIGHT, LATIT, IATMOS, ATMOS, RH, TAIR, SEASON, TDAY, IH2O, W, IO3, IALT, AbO3, IGAS, ILOAD, ApCH2O, ApCH4, ApCO, ApHNO2, ApHNO3, ApNO,ApNO2, ApNO3, ApO3, ApSO2, qCO2, ISPCTR, AEROS, ALPHA1, ALPHA2, OMEGL, GG, ITURB, TAU5, BETA, BCHUEP, RANGE, VISI, TAU550, IALBDX, RHOX, ITILT, IALBDG,TILT, WAZIM,  RHOG, WLMN, WLMX, SUNCOR, SOLARC, IPRT, WPMN, WPMX, INTVL, IOUT, ICIRC, SLOPE, APERT, LIMIT, ISCAN, IFILT, WV1, WV2, STEP, FWHM, ILLUM,IUV, IMASS, ZENITH, AZIM, ELEV, AMASS, YEAR, MONTH, DAY, HOUR, LONGIT, ZONE, DSTEP)

    return output


def SMARTSSRRLPOA(IOUT,YEAR,MONTH,DAY,HOUR, LATIT, LONGIT, ALTIT, ZONE, 
               W, RH, TAIR, SEASON, TDAY, SPR, TAU5, TILT, WAZIM,
               RHOG, HEIGHT='0',
               material='DryGrass', min_wvl='280', max_wvl='4000'):

    r'''
    This function calculates the spectral albedo for a given material. If no 
    material is provided, the function will return a list of all valid 
    materials.

    Parameters
    ----------
    material : string
        Unique identifier for ground cover. Pass None to retreive a list of
        all valid materials.
    WLMN : string
        Minimum wavelength to retreive
    WLMX : string
        Maximum wavelength to retreive
    YEAR : string
        Year
    MONTH : string
        Month
    DAY : string
        Day
    HOUR : string
        Hour, in 24 hour format.
    LATIT : string
        Latitude of the location.
    LONGIT : string
        Longitude of the location.
    ALTIT : string
        elevation of the ground surface above sea level [km].
        WARNING: Please note that TMY3 data is in meters, convert before using this
        function.
    ZONE : string
        Timezone
    W : string
        Precipitable water above the site altitude, in units of cm or equivalently
        g/cm2/
    RH : string
        Relative Humidity
    TAIR : string
        Temperature.
    SEASON : string
        Season, either 'WINTER' or 'SUMMER'. If Spring, use 'SUMMER'. If
        Autumn, use 'WINTER'.
    TDAY : string
        Average of the day's temperature.        
    HEIGHT : string
        Altitude of the simulated object over the surface, in km.
    SPR : string
        Site pressure, in mbars.
    TAU5 : string
        Broadband turbidity
    TILT : string
        Tilt angel of the receiving surface (0 to 90 decimal deg.), e.g. 90.0
        for a vertical plane. Use -999 for a sun-tracking surface.
    WAZIM : string
        Surface azimuth (0 to 360 decimal deg.) counted clockwise from North;
        e.g., 270 deg. for a surface facing West. Use -999 for a sun-tracking
        surface.
    RHOG : string
        Local broadband Lambertian foreground albedo (for tilted plane calculations),
        usually between 0.05 and 0.90.

    Returns
    -------
    data : pandas
        Matrix with first column representing wavelength (in nm) and second
        column representing albedo of specified material at the wavelength
    
    '''

    if float(ALTIT) > 800:
        print("Altitude should be in km. Are you in Mt. Everest or above or",
              "using meters? This might fail but we'll attempt to continue.")
    
    ## Card 1: Comment. 64 characters max. In theory no spaces but yes underscores.
    CMNT = 'SRRL Spectra'    
    
    ## Card 2: ISPR is an option for site's pressure.
    # ISPR = 0 to input SPR on Card 2a
    # ISPR = 1 to input SPR, ALTIT and HEIGHT on Card 2a
    # ISPR = 2 to input LATIT, ALTIT and HEIGHT on Card 2a.
    ISPR = '1'
    
    # Card 2a (if ISPR = 0): SPR
    SPR = SPR #mbar
    
    # Card 2a (if ISPR = 1): SPR, ALTIT, HEIGHT
    # SPR: Surface pressure (mb).
    # ALTIT: Site's altitude, i.e., elevation of the ground surface above sea level (km); must be
    # <= 100 km. In case of a flying object, ALTIT refers to the ground surface below it.
    # HEIGHT: Height of the simulated object above the ground surface underneath (km); must be
    # <= 100 km (new input).
    # The total ALTIT + HEIGHT is the altitude of the simulated object above sea level and
    # must be <= 100 km.
    
    # Card 2a (if ISPR = 2): LATIT, ALTIT, HEIGHT
    # LATIT: Site's latitude (decimal degrees, positive North, negative South); e.g., -17.533 for
    # Papeete, Tahiti. If LATIT is unknown, enter 45.0.
    # ALTIT: Site's altitude, i.e., elevation of the ground surface above sea level (km); must be
    # <= 100 km. In case of a flying object, ALTIT refers to the ground surface below it.
    # HEIGHT: Height of the simulated object above the ground surface underneath (km); must be
    # <= 100 km (new input).
    # The total ALTIT + HEIGHT is the altitude of the simulated object above sea level and
    # must be <= 100 km.
    
    ALTIT = ALTIT
    HEIGHT = HEIGHT
    #LATIT = LATIT
    
    ## Card 3: IATMOS is an option to select the proper default atmosphere
    # Its value can be either 0 or 1.
    # Set IATMOS = 0 to define a realistic (i.e., non-reference) atmosphere. Card 3a will then have to
    # provide TAIR, RH, SEASON, TDAY.
    # Set IATMOS = 1 to select one of 10 default reference atmospheres (i.e., for ideal conditions). The
    # shortened name of this atmosphere must be provided by ATMOS on Card 3a.
    
    IATMOS = '0'
    
    # Card 3a (if IATMOS = 1): ATMOS
    # ATMOS is the name of the selected reference atmosphere; 4 characters max. This name can
    # be one of the following: 
    #    USSA   (U.S. Standard Atmosphere)   MLS   (Mid-Latitude Summer) 
    #    MLW   (Mid-Latitude Winter)   SAS   (Sub-Arctic Summer) 
    #   SAW   (Sub-Arctic Winter)   TRL   (Tropical)   STS   (Sub-Tropical Summer)
    #   STW   (Sub-Tropical Winter)   AS   (Arctic Summer)   AW   (Arctic Winter)
    
    ATMOS = 'USSA'
    
    # Card 3a(if IATMOS = 0): TAIR, RH, SEASON, TDAY.
    # RH: Relative humidity at site level (%).
    # SEASON: Can be either `WINTER` or `SUMMER`, for calculation of precipitable water and
    # stratospheric temperature. If the true season is Fall, select WINTER. Select SUMMER if the
    # true season is Spring. SEASON slightly affects the ozone effective temperature and the
    # aerosol optical characteristics.
    # TAIR: Atmospheric temperature at site level (°C). Acceptable range: -120 < TAIR < 50.
    # TDAY: Average daily temperature at site level (°C). For a flying object (HEIGHT > 0), this
    # is a reference temperature for various calculations, therefore it is important to provide a
    # realistic value in this case in particular. Acceptable range: -120 < TDAY < 50.
    
    RH = RH
    TAIR = TAIR
    SEASON = SEASON
    TDAY = TDAY
    
    ## Card 4: IH2O is an option to select the correct water vapor data. All water vapor calculations involve
    # precipitable water, W. The following values of IH2O are possible:
    # 0, to input W on Card 4a
    # 1, if W is to be defaulted to a value prescribed by the selected reference atmosphere and the site
    # altitude (thus if IATMOS = 1 on Card 3). If IATMOS != 1, USSA will be defaulted for this step.
    # 2, if W is to be calculated by the program from TAIR and RH (thus if IATMOS = 0 on Card 3). This
    # calculation is only approximate (particularly if HEIGHT > 0) and therefore this option is not
    # recommended.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    
    IH2O = '0'
    
    # Card 4a: (if IH2O = 0): W is precipitable water above the site altitude
    # in units of cm, or equivalently, g/cm2; it must be <= 12.
    
    W = W
    
    ## Card 5: IO3 is an option to select the appropriate ozone abundance input.
    # IO3 = 0 to input IALT and AbO3 on Card 5a
    # IO3 = 1 to use a default value for AbO3 according to the reference atmosphere selected by
    # IATMOS. If IATMOS != 1, USSA will be defaulted for this calculation.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    IO3 = '1'

    # Card 5a (if IO3 = 0): IALT, AbO3
    # IALT is an option to select the appropriate ozone column altitude correction.
    # IALT = 0 bypasses the altitude correction, so that the value of AbO3 on
    # Card 5a is used as is. IALT = 1 should be rather used if a vertical
    # profile correction needs to be applied (in case of an elevated site when
    # the value of AbO3 is known only at sea level). 
    IALT = ''
    AbO3 = ''
    
    ## Card 6 IGAS is an option to define the correct conditions for gaseous absorption and atmospheric pollution. 
    # IGAS = 0 if ILOAD on Card 6a is to be read so that extra gaseous absorption calculations
    # (corresponding to the gas load in the lower troposphere due to pollution or absence thereof) can be
    # initiated;
    # IGAS =1 if all gas abundances (except carbon dioxide, ozone and water vapor see Cards 4a, 5a,
    # and 7) are to be defaulted, using average vertical profiles.
    # If IATMOS = 0 is selected, then IH2O should be 0 or 2; IO3 and IGAS should be 0.
    # If IATMOS = 1 is selected, then IH2O, IO3, and IGAS may take any value. All user inputs
    # have precedence over the defaults.
    
    IGAS = '0'
    
    # Card 6a  (if IGAS = 0): ILOAD is an option for tropospheric pollution, only used if IGAS = 0.
    # For ILOAD = 0, Card 6b will be read with the concentrations of 10 pollutants.
    # ILOAD = 1 selects default PRISTINE ATMOSPHERIC conditions, leading to slightly
    # reduced abundances of some gases compared to the initial default obtained with the selected
    # reference atmosphere.
    # Setting ILOAD to 2-4 will increase the concentration of the 10 pollutants to possibly
    # represent typical urban conditions: LIGHT POLLUTION (ILOAD = 2), MODERATE
    # POLLUTION (ILOAD = 3), and SEVERE POLLUTION (ILOAD = 4).
    
    ILOAD = '1'
    
    # Card 6b (if IGAS = 0 and ILOAD = 0): ApCH2O, ApCH4, ApCO, ApHNO2,
    # ApHNO3, ApNO, ApNO2, ApNO3, ApO3, ApSO2
    # ApCH2O: Formaldehyde volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApCH4: Methane volumetric concentration in the assumed 1-km deep tropospheric pollution
    # layer (ppmv).
    # ApCO: Carbon monoxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv), Card 6b.
    # ApHNO2: Nitrous acid volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApHNO3: Nitric acid volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO: Nitric oxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO2: Nitrogen dioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApNO3: Nitrogen trioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    # ApO3: Ozone volumetric concentration in the assumed 1-km deep tropospheric pollution
    # layer (ppmv).
    # ApSO2: Sulfur dioxide volumetric concentration in the assumed 1-km deep tropospheric
    # pollution layer (ppmv).
    
    ApCH2O = ''
    ApCH4 = ''
    ApCO = ''
    ApHNO2 = ''
    ApHNO3 = ''
    ApNO = ''
    ApNO2 = ''
    ApNO3 = ''
    ApO3 = ''
    ApSO2 =''
    
    ## Card 7 qCO2 carbon dioxide columnar volumetric concentration (ppmv).
    qCO2 = '0.0'
    
    # Card 7a ISPCTR 
    # is an option to select the proper extraterrestrial
    # spectrum. This option allows to choose one out of ten possible spectral
    # files (``Spctrm_n.dat``, where n = 0-8 or n = U).  
    # -1  Spctrm_U.dat  N/A User User
    # 0  Spctrm_0.dat  N/A Gueymard, 2004 (synthetic) 1366.10
    # 1  Spctrm_1.dat  N/A Gueymard, unpublished (synthetic) 1367.00
    # 2  Spctrm_2.dat  cebchkur MODTRAN, Cebula/Chance/Kurucz 1362.12
    # 3  Spctrm_3.dat  chkur MODTRAN, Chance/Kurucz 1359.75
    # 4  Spctrm_4.dat  newkur MODTRAN, New Kurucz 1368.00
    # 5  Spctrm_5.dat  oldkur MODTRAN, Old Kurucz 1373.16
    # 6  Spctrm_6.dat  thkur MODTRAN, Thuillier/Kurucz 1376.23
    # 7  Spctrm_7.dat  MODTRAN2 Wehrli/WRC/WMO, 1985 1367.00
    # 8  Spctrm_8.dat  N/A ASTM E490, 2000 (synthetic) 1366.10
    
    ISPCTR ='0'
    
    ## Card 8: AEROS selects the aerosol model, with one of the following twelve possible choices:
    #  S&F_RURAL ,  S&F_URBAN ,  S&F_MARIT ,  S&F_TROPO , These four choices
    # refer respectively to the Rural, Urban, Maritime and Tropospheric aerosol
    # models (Shettle and Fenn, 1979), which are humidity dependent and common with MODTRAN. 
    #  SRA_CONTL ,  SRA_URBAN ,  SRA_MARIT , These three choices refer
    # respectively to the Continental, Urban, and Maritime aerosol models of
    # the IAMAP preliminary standard atmosphere (IAMAP, 1986). 
    #  B&D_C ,  B&D_C1 , These two choices refer respectively to the Braslau &
    # Dave aerosol type C and C1, themselves based on Deirmendjian's Haze L model. 
    #  DESERT_MIN ,  DESERT_MAX  DESERT_MIN corresponds to background (normal)
    # conditions in desert areas, whereas DESERT_MAX corresponds to extremely
    # turbid conditions (sandstorms).  
    # 'USER' Card 8a is then necessary to input user-supplied aerosol information.
    
    AEROS = 'S&F_TROPO' 
    # Card 8a: 
    # if AEROS =  USER : ALPHA1, ALPHA2, OMEGL, GG These 4 variables must represent broadband average values only!
    # ALPHA1: Average value of Ångström's wavelength exponent $\alpha$ for wavelengths < 500 nm
    # (generally between 0.0 and 2.6).
    # ALPHA2: Average value of Ångström's wavelength exponent $\alpha$ for wavelengths >= 500 nm
    # (generally between 0.0 and 2.6).
    # OMEGL: Aerosol single scattering albedo (generally between 0.6 and 1.0).
    # GG: Aerosol asymmetry parameter (generally between 0.5 and 0.9).
    ALPHA1 = ''
    ALPHA2 = ''
    OMEGL = ''
    GG = ''
    
    ## Card 9: ITURB is an option to select the correct turbidity data input. The different options are:
    # 0, to read TAU5 on Card 9a
    # 1, to read BETA on Card 9a
    # 2, to read BCHUEP on Card 9a
    # 3, to read RANGE on Card 9a
    # 4, to read VISI on Card 9a
    # 5, to read TAU550 on Card 9a (new option).
    
    ITURB = '0'
    
    #Card 9a Turbidity value
    TAU5 = TAU5 #'0.00' #if ITURB == 0
    BETA = '' #if ITURB == 1
    BCHUEP = '' #if ITURB == 2
    RANGE = '' #if ITURB == 3
    VISI = '' #if ITURB == 4
    TAU550 = '' #if ITURB == 5
    
    ## Card 10: Far Field Albedo for backscattering
    IALBDX = _material_to_code(material)
    
    # Card 10a:
    RHOX = ''
                            # Zonal broadband Lambertian ground albedo (for backscattering calculations); must
                            # be between 0 and 1.
                            
    # Card 10b: ITILT is an option for tilted surface calculations. 
    #Select ITILT= 0 for no such calculation, 
    #ITILT = 1 to initiate these calculations using information on Card 10c.
    ITILT = '1'
    
    # Card 10c:
    # IALBDG is identical to IALBDX (see Card 10) except that it relates to the foreground local
    # albedo seen by a tilted surface. The list of options is identical to that of IALBDG and thus
    # extends from 1 to 64 (new).
    # TILT: Tilt angle of the receiving surface (0 to 90 decimal deg.); e.g. 90.0 for a vertical
    # plane. Use -999 for a sun-tracking surface.
    # WAZIM: Surface azimuth (0 to 360 decimal deg.) counted clockwise from North; e.g., 270
    # deg. for a surface facing West. Use -999 for a sun-tracking surface.
    
    IALBDG = '-1'
    TILT = TILT
    WAZIM = WAZIM
    
    # Card 10d:
    # RHOG: Local broadband Lambertian foreground albedo (for tilted plane calculations), Card
    # 10d (if IALBDG = -1); usually between 0.05 and 0.90.
    RHOG = RHOG
    
    ## Card 11: Spectral range for all Calculations
    WLMN = min_wvl #Min wavelength
    WLMX = max_wvl #Max wavelength
    SUNCOR = '1.0' 
        #Correction factor for irradiance is a correction factor equal to the inverse squared actual radius vector, or true Sun-Earth
        # distance; e.g., SUNCOR = 1.024.
        # SUNCOR varies naturally between 0.966 and 1.034, adding 3.4% to the irradiance in January
        # and reducing it by 3.4% in July. It is calculated by the program if the solar position is calculated
        # from date & time, i.e., if IMASS = 3 on Card 17, thus overwriting the input SUNCOR value on
        # Card 11. If solar position is directly input instead (IMASS = 3), SUNCOR should be set to 1.0 if
        # the average extraterrestrial irradiance (or solar constant, see SOLARC) is to be used, or to any
        # other number between 0.966 and 1.034 to correct it for distance if so desired.

    SOLARC = '1367.0' #Solar constant
    
    
    ## Card 12: Output results selection:
    # IPRT is an option to select the results to be printed on Files 16 and 17. Only broadband results are
    # output (to File 16) if IPRT = 0. Spectral results are added to File 16,
    # and Card 12a is read, if IPRT = 1. Spectral results are rather printed to
    # File 17 (in a spreadsheet-like format) if IPRT = 2. Finally, spectral
    # results are printed to both File 16 and 17 if IPRT = 3. Cards 
    # 12b and 12c are read if IPRT = 2 or 3 (see IOTOT and IOUT).
    IPRT = '2'
    
    # Card 12a: Min, Max and Step wavelength (nm) (Output can be different than
    # calculation...
    WPMN = WLMN
    WPMX = WLMX
    INTVL = '.5'
    
    # Card 12b: Total number of output variables:
    #IOTOT = XXX #This is determined with the input of this function
    
    # Card 12c: Variables to output selection 
    #(space separated numbers 1-43 according to the table below:
    IOUT = IOUT
    
    
    ## Card 13: Circumsolar Calculation
    # ICIRC is an option controlling the calculation of circumsolar radiation, which is useful when
    # simulating any type of radiometer (spectral or broadband) equipped with a collimator.
    # ICIRC = 0 bypasses these calculations.
    # ICIRC = 1 indicates that a typical radiometer needs to be simulated. The geometry of its collimator
    # must then defined on Card 13a.
    
    ICIRC = '0'
    
    #Card 13a (if ICIRC = 1): SLOPE, APERT, LIMIT
    SLOPE = ''
    APERT = ''
    LIMIT = ''
    
    ## Card 14 Option for using the scanning/smoothing virtual filter of the postprocessor.
    # The smoothed results are output on a spreadsheet-ready file, File 18 (``smarts295.scn.txt``). This postprocessor is
    # activated if ISCAN = 1, not if ISCAN = 0. Card 14a is read if ISCAN = 1.
    
    ISCAN = '0'
    
    # Card 14a (if ISCAN = 1): IFILT, WV1, WV2, STEP, FWHM
    IFILT = ''
    WV1 = ''
    WV2 = ''
    STEP = ''
    FWHM = ''
    
    ## Card 15 ILLUM: Option for illuminance, luminous efficacy and photosynthetically active radiation (PAR)
    # calculations. These calculations take place if ILLUM = -1, 1, -2 or 2, and are bypassed if ILLUM = 0.
    # With ILLUM = -1 or 1, illuminance calculations are based on the CIE photopic curve (or Vlambda
    # curve) of 1924, as supplied in File ``VLambda.dat``. With ILLUM = -2 or 2, the same calculations are
    # done but the revised CIE photopic curve of 1988 is rather used (from File ``VMLambda.dat``). Note
    # that selecting ILLUM = 1 or -1 will override WLMN and WLMX (see Card 11) so that calculations
    # are done between at least 360 and 830 nm.
    # Moreover, if ILLUM = 1 or 2, luminous efficacy calculations are added to the illuminance
    # calculations. This overrides the values of WLMN and WLMX on Card 11, and replaces them by 280
    # and 4000, respectively.
    
    ILLUM = '0'
    
    ## Card  16: Option for special broadband UV calculations. Select IUV = 0 for no special UV calculation, 
    # IUV = 1 to initiate such calculations. These include UVA, UVB, UV index, and
    # different action weighted irradiances of interest in photobiology.
    # Note that IUV = 1 overrides WLMN and WLMX so that calculations are done between at least 280
    # and 400 nm. The spectral results are also printed between at least 280 and 400 nm, irrespective of
    # the IPRT, WPMN, and WPMX values.
    
    IUV = '0'
    
    ## Card 17:
    # Option for solar position and air mass calculations. Set IMASS to:
    # 0, if inputs are to be ZENIT, AZIM on Card 17a
    # 1, if inputs are to be ELEV, AZIM on Card 17a
    # 2, if input is to be AMASS on Card 17a
    # 3, if inputs are to be YEAR, MONTH, DAY, HOUR, LATIT, LONGIT, ZONE on Card 17a
    # 4, if inputs are to be MONTH, LATIT, DSTEP on Card 17a (for a daily calculation).
    IMASS = '3'

    
    # Card 17a: IMASS = 0 Zenith and azimuth
    ZENITH = ''
    AZIM = ''
    
    # Card 17a: IMASS = 1 Elevation and Azimuth
    ELEV = ''
    
    # Card 17a: IMASS = 2 Input air mass directly
    AMASS = ''
    
    # Card 17a: IMASS = 3 Input date, time and coordinates
    YEAR = YEAR
    MONTH = MONTH
    DAY = DAY
    HOUR = HOUR
    LATIT = LATIT
    LONGIT = LONGIT
    ZONE = ZONE
    
    # Card 17a: IMASS = 4 Input Moth, Latitude and DSTEP
    DSTEP = ''

    output = _smartsAll(CMNT, ISPR, SPR, ALTIT, HEIGHT, LATIT, IATMOS, ATMOS, RH, TAIR, SEASON, TDAY, IH2O, W, IO3, IALT, AbO3, IGAS, ILOAD, ApCH2O, ApCH4, ApCO, ApHNO2, ApHNO3, ApNO,ApNO2, ApNO3, ApO3, ApSO2, qCO2, ISPCTR, AEROS, ALPHA1, ALPHA2, OMEGL, GG, ITURB, TAU5, BETA, BCHUEP, RANGE, VISI, TAU550, IALBDX, RHOX, ITILT, IALBDG,TILT, WAZIM,  RHOG, WLMN, WLMX, SUNCOR, SOLARC, IPRT, WPMN, WPMX, INTVL, IOUT, ICIRC, SLOPE, APERT, LIMIT, ISCAN, IFILT, WV1, WV2, STEP, FWHM, ILLUM,IUV, IMASS, ZENITH, AZIM, ELEV, AMASS, YEAR, MONTH, DAY, HOUR, LONGIT, ZONE, DSTEP)

    return output


def _smartsAll(CMNT, ISPR, SPR, ALTIT, HEIGHT, LATIT, IATMOS, ATMOS, RH, TAIR, SEASON, TDAY, IH2O, W, IO3, IALT, AbO3, IGAS, ILOAD, ApCH2O, ApCH4, ApCO, ApHNO2, ApHNO3, ApNO,ApNO2, ApNO3, ApO3, ApSO2, qCO2, ISPCTR, AEROS, ALPHA1, ALPHA2, OMEGL, GG, ITURB, TAU5, BETA, BCHUEP, RANGE, VISI, TAU550, IALBDX, RHOX, ITILT, IALBDG,TILT, WAZIM,  RHOG, WLMN, WLMX, SUNCOR, SOLARC, IPRT, WPMN, WPMX, INTVL, IOUT, ICIRC, SLOPE, APERT, LIMIT, ISCAN, IFILT, WV1, WV2, STEP, FWHM, ILLUM,IUV, IMASS, ZENITH, AZIM, ELEV, AMASS, YEAR, MONTH, DAY, HOUR, LONGIT, ZONE, DSTEP):
    r'''
    #data = smartsAll(CMNT, ISPR, SPR, ALTIT, HEIGHT, LATIT, IATMOS, ATMOS, RH, TAIR, SEASON, TDAY, IH2O, W, IO3, IALT, AbO3, IGAS, ILOAD, ApCH2O, ApCH4, ApCO, ApHNO2, ApHNO3, ApNO,ApNO2, ApNO3, ApO3, ApSO2, qCO2, ISPCTR, AEROS, ALPHA1, ALPHA2, OMEGL, GG, ITURB, TAU5, BETA, BCHUEP, RANGE, VISI, TAU550, IALBDX, RHOX, ITILT, IALBDG,TILT, WAZIM,  RHOG, WLMN, WLMX, SUNCOR, SOLARC, IPRT, WPMN, WPMX, INTVL, IOUT, ICIRC, SLOPE, APERT, LIMIT, ISCAN, IFILT, WV1, WV2, STEP, FWHM, ILLUM,IUV, IMASS, ZENITH, ELEV, AMASS, YEAR, MONTH, DAY, HOUR, LONGIT, ZONE, DSTEP)  
    # SMARTS Control Function
    # 
    #   Inputs:
    #       All variables are labeled according to the SMARTS 2.9.5 documentation.
    #       NOTICE THAT "IOTOT" is not an input variable of the function since is determined in the function 
    #       by sizing the IOUT variable.
    #   Outputs:
    #       data, is a matrix containing the outputs with as many rows as 
    #       wavelengths+1 (includes header) and as many columns as IOTOT+1 (column 1 is wavelengths)  
    #
    '''
    
    ## Init
    import os
    import pandas as pd
    import subprocess
    
    # Check if SMARTSPATH environment variable exists and change working
    # directory if it does.
    original_wd = None
    if 'SMARTSPATH' in os.environ:
        original_wd = os.getcwd()
        os.chdir(os.environ['SMARTSPATH'])
    
    try:
        os.remove('smarts295.inp.txt')
    except:
        pass
    try:
        os.remove('smarts295.out.txt')
    except:
        pass  
    try:       
        os.remove('smarts295.ext.txt')
    except:
        pass
    try:
        os.remove('smarts295.scn.txt')
    except:
        pass
        
    f = open('smarts295.inp.txt', 'w')
    
    IOTOT = len(IOUT.split())
    
    ## Card 1: Comment.
    if len(CMNT)>62:
        CMNT = CMNT[0:61] 

    CMNT = CMNT.replace(" ", "_")
    CMNT = "'"+CMNT+"'"
    print('{}' . format(CMNT), file=f)
    
    ## Card 2: Site Pressure
    print('{}'.format(ISPR), file=f)
    
    ##Card 2a:
    if ISPR=='0':
       # case '0' #Just input pressure.
        print('{}'.format(SPR), file=f)
    elif ISPR=='1':
        # case '1' #Input pressure, altitude and height.
        print('{} {} {}'.format(SPR, ALTIT, HEIGHT), file=f)
    elif ISPR=='2':
        #case '2' #Input lat, alt and height
        print('{} {} {}'.format(LATIT, ALTIT, HEIGHT), file=f)
    else:
        print("ISPR Error. ISPR should be 0, 1 or 2. Currently ISPR = ", ISPR)    
    
    ## Card 3: Atmosphere model
    print('{}'.format(IATMOS), file=f)
    
    ## Card 3a:
    if IATMOS=='0':
        #case '0' #Input TAIR, RH, SEASON, TDAY
        print('{} {} {} {}'.format(TAIR, RH, SEASON, TDAY), file=f)
    elif IATMOS=='1':        
        #case '1' #Input reference atmosphere
        ATMOS = "'"+ATMOS+"'"
        print('{}'.format(ATMOS), file=f)
    
    ## Card 4: Water vapor data
    print('{}'.format(IH2O), file=f)
    
    ## Card 4a
    if IH2O=='0':
        #case '0'
        print('{}'.format(W), file=f)
    elif IH2O=='1':
        #case '1'
        #The subcard 4a is skipped
        pass  #      print("")
    
    ## Card 5: Ozone abundance
    print('{}'.format(IO3), file=f)
    
    ## Card 5a
    if IO3=='0':
        #case '0'
        print('{} {}'.format(IALT, AbO3), file=f)
    elif IO3=='1':
        #case '1'
        #The subcard 5a is skipped and default values are used from selected 
        #reference atmosphere in Card 3. 
        pass #      print("")
    
    ## Card 6: Gaseous absorption and atmospheric pollution
    print('{}'.format(IGAS), file=f)
    
    ## Card 6a:  Option for tropospheric pollution
    if IGAS=='0':
        # case '0'
        print('{}'.format(ILOAD), file=f)

        ## Card 6b: Concentration of Pollutants        
        if ILOAD=='0':
            #case '0'
            print('{} {} {} {} {} {} {} {} {} {} '.format(ApCH2O, ApCH4, ApCO, ApHNO2, ApHNO3, ApNO, ApNO2, ApNO3, ApO3, ApSO2), file=f)
        elif ILOAD=='1':
            #case '1'
                #The subcard 6b is skipped and values of PRISTINE
                #ATMOSPHERIC conditions are assumed
            pass #     print("")
        elif ILOAD=='2' or ILOAD =='3' or ILOAD == '4':
            #case {'2', '3', '4'}
            #The subcard 6b is skipped and value of ILOAD will be used
            #as LIGHT POLLUTION (ILOAD = 2), MODERATE POLLUTION (ILOAD = 3), 
            #and SEVERE POLLUTION (ILOAD = 4).
            pass #     print("")
             
    elif IGAS=='1':
        #case '1'
        #The subcard 6a is skipped, and values are for default average
        #profiles.
        print("")
    
    ## Card 7:  CO2 columnar volumetric concentration (ppmv)
    print('{}'.format(qCO2), file=f)
    
    ## Card 7a: Option of proper extraterrestrial spectrum
    print('{}'.format(ISPCTR), file=f)
    
    ## Card 8: Aerosol model selection out of twelve
    AEROS = "'"+AEROS+"'"

    print('{}'.format(AEROS), file=f)
    
    ## Card 8a: If the aerosol model is 'USER' for user supplied information
    if AEROS=="'USER'":
        print('{} {} {} {}'.format(ALPHA1, ALPHA2, OMEGL, GG), file=f)
    else:
        #The subcard 8a is skipped
        pass #     print("")
    
    ## Card 9: Option to select turbidity model
    print('{}'.format(ITURB), file=f)
    
    ## Card 9a
    if ITURB=='0':
        #case '0'
        print('{}'.format(TAU5), file=f)
    elif ITURB=='1':
        #case '1'
        print('{}'.format(BETA), file=f)
    elif ITURB=='2':
        #case '2'
        print('{}'.format(BCHUEP), file=f)
    elif ITURB=='3':
        #case '3'
        print('{}'.format(RANGE), file=f)
    elif ITURB=='4':
        #case '4'
        print('{}'.format(VISI), file=f)
    elif ITURB=='5':
        #case '5'
        print('{}'.format(TAU550), file=f)
    else:
        print("Error: Card 9 needs to be input. Assign a valid value to ITURB = ", ITURB)
    
    ## Card 10:  Select zonal albedo
    print('{}'.format(IALBDX), file=f)
    
    ## Card 10a: Input fix broadband lambertial albedo RHOX
    if IALBDX == '-1':
        print('{}'.format(RHOX), file=f)
    else:
        pass #     print("")
        #The subcard 10a is skipped.
    
    ## Card 10b: Tilted surface calculation flag
    print('{}'.format(ITILT), file=f)
    
    ## Card 10c: Tilt surface calculation parameters
    if ITILT == '1':
        print('{} {} {}'.format(IALBDG, TILT, WAZIM), file=f)
        
        ##Card 10d: If tilt calculations are performed and zonal albedo of
        ##foreground.
        if IALBDG == '-1': 
            print('{}'.format(RHOG), file=f)
        else:
            pass #     print("")
            #The subcard is skipped 
    
    
    ## Card 11: Spectral ranges for calculations
    print('{} {} {} {}'.format(WLMN, WLMX, SUNCOR, SOLARC), file=f)
    
    ## Card 12: Output selection.
    print('{}'.format(IPRT), file=f)
    
    ## Card 12a: For spectral results (IPRT >= 1) 
    if float(IPRT) >= 1:
        print('{} {} {}'.format(WPMN, WPMX, INTVL), file=f)
        
        ## Card 12b & Card 12c: 
        if float(IPRT) == 2 or float(IPRT) == 3:
            print('{}'.format(IOTOT), file=f)
            print('{}'.format(IOUT), file=f)
        else:
            pass #     print("")
            #The subcards 12b and 12c are skipped.
    else:
        pass #     print("")
        #The subcard 12a is skipped
    
    ## Card 13: Circumsolar calculations
    print('{}'.format(ICIRC), file=f)
    
    ## Card 13a:  Simulated radiometer parameters
    if ICIRC == '1':
        print('{} {} {}'.format(SLOPE, APERT, LIMIT), file=f)
    else:
        pass #     print("")
        #The subcard 13a is skipped since no circumsolar calculations or
        #simulated radiometers have been requested.

    
    ## Card 14:  Scanning/Smoothing virtual filter postprocessor
    print('{}'.format(ISCAN), file=f)
    
    ## Card 14a:  Simulated radiometer parameters
    if ISCAN == '1': 
        print('{} {} {} {} {}'.format(IFILT, WV1, WV2, STEP, FWHM), file=f)
    else:
        pass #     print("")
        #The subcard 14a is skipped since no postprocessing is simulated.    
    
    ## Card 15: Illuminace, luminous efficacy and photosythetically active radiarion calculations
    print('{}'.format(ILLUM), file=f)
    
    ## Card 16: Special broadband UV calculations
    print('{}'.format(IUV), file=f)
    
    ## Card 17:  Option for solar position and air mass calculations
    print('{}'.format(IMASS), file=f)
    
    ## Card 17a: Solar position parameters:
    if IMASS=='0':
        #case '0' #Enter Zenith and Azimuth of the sun
        print('{} {}'.format(ZENITH, AZIM), file=f)
    elif IMASS=='1':
        #case '1' #Enter Elevation and Azimuth of the sun
        print('{} {}'.format(ELEV, AZIM), file=f)
    elif IMASS=='2':
        #case '2' #Enter air mass directly
        print('{}'.format(AMASS), file=f)
    elif IMASS=='3':
        #case '3' #Enter date, time and latitude
        print('{} {} {} {} {} {} {}'.format(YEAR, MONTH, DAY, HOUR, LATIT, LONGIT, ZONE), file=f)
    elif IMASS=='4':
        #case '4' #Enter date and time and step in min for a daily calculation.
        print('{}, {}, {}'.format(MONTH, LATIT, DSTEP), file=f)
    
    ## Input Finalization
    print('', file=f)
    f.close()
    
    ## Run SMARTS 2.9.5
    #dump = os.system('smarts295bat.exe')
    commands = ['smarts295bat', 'smarts295bat.exe']
    command = None
    for cmd in commands:
        if os.path.exists(cmd):
            command = cmd
            break

    if not command:
        print('Could not find SMARTS2 executable.')
        data = None
    else:
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=open("output.txt", "w"), shell=True)
        p.wait()
        
        ## Read SMARTS 2.9.5 Output File
        data = pd.read_csv('smarts295.ext.txt', delim_whitespace=True)    

    try:
        os.remove('smarts295.inp.txt')
    except:
        pass #     print("") 
    try:
        os.remove('smarts295.out.txt')
    except:
        pass #     print("")     
    try:       
        os.remove('smarts295.ext.txt')
    except:
        pass #     print("") 
    try:
        os.remove('smarts295.scn.txt')
    except:
        pass #     print("") 
    
    # Return to original working directory.    
    if original_wd:
        os.chdir(original_wd)

    return data