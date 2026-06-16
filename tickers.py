"""
Ticker universe: S&P 500, S&P 400 MidCap, AEX, DAX, CAC 40, FTSE 100,
IBEX 35, SMI, BEL 20, OMX, and other major European indices.
"""

# ── S&P 500 ──────────────────────────────────────────────────────────────────
SP500 = [
    "AAPL","MSFT","NVDA","AMZN","META","GOOGL","GOOG","BRK-B","LLY","AVGO",
    "JPM","V","TSLA","UNH","XOM","MA","COST","PG","JNJ","ABBV","HD","MRK",
    "CVX","CRM","BAC","NFLX","AMD","KO","WMT","PEP","TMO","ADBE","ACN","MCD",
    "LIN","DHR","CSCO","ABT","TXN","NKE","PM","NEE","WFC","RTX","AMGN","ORCL",
    "INTC","IBM","QCOM","HON","LOW","GE","SPGI","UNP","CAT","ELV","BLK","ISRG",
    "GS","SBUX","AXP","SYK","MDLZ","GILD","ADI","REGN","MMC","DE","VRTX","CI",
    "BSX","NOW","ZTS","BDX","CB","AMT","PLD","AON","MO","ETN","DUK","ITW",
    "SO","SHW","CL","TJX","MMM","FDX","NSC","EW","APD","PNC","USB","HUM",
    "EOG","SLB","PSA","OXY","KLAC","LRCX","SNPS","CDNS","FTNT","MCHP","ON",
    "ANET","PANW","CRWD","ABNB","UBER","DDOG","SNOW","ZS","NET","TEAM","MDB",
    "GD","LMT","NOC","BA","HII","TDG","HWM","TXT","L","AFL","MET","PRU",
    "ALL","TRV","PGR","AIG","HIG","LNC","GL","AIZ","WRB","RE","RNR","AJG",
    "AON","WTW","BRO","ACGL","RLI","MKL","HCI","ERIE","UVE","KMPR",
    "DVA","UHS","HCA","THC","CNC","MOH","CVS","WAB","CSX","R","JBHT",
    "CHRW","EXPD","XPO","SAIA","ODFL","WERN","HUBG","FWRD","MRTN","CVLG",
    "VZ","T","TMUS","LUMN","CABO","CHTR","CMCSA","DIS",
    "FOX","FOXA","WBD","NWSA","NWS","NYT","GCI","IAC","Z","TRIP",
    "EXPE","BKNG","PCLN","HLT","MAR","H","IHG","CHH","VAC","TNL","RCL",
    "CCL","NCLH","MGM","WYNN","LVS","CZR","PENN","DKNG","ACMR",
    "AES","AEE","AEP","AWK","D","DTE","ED","EIX","ETR","ES","EXC","FE",
    "LNT","NI","OGE","PNW","PPL","SCCO","SRE","WEC","XEL","CNP","CMS",
    "EVRG","OGS","NWN","MSEX","AWR","ARTNA","YORW","CTWS","GWRS",
    "ADM","BG","DAR","INGR","MOS","CF","NTR","FMC","CTVA","ICL","SMG",
    "AGCO","CNH","DE","TTC","ITT",
    "PH","ROK","EMR","HUBB","NDSN","AME","GNRC","ROP","IEX","XYL","WTS",
    "A","FTV","TRMB","KEYS","GRMN","LII","JCI","CARR","OTIS",
    "IR","TT","MAS","PNR","ALLE","AOS","SWK","SNA","LDOS",
    "SAIC","DXC","HPQ","HPE","NTAP","SWKS","QRVO","TER",
    "EA","TTWO","RBLX","U","MTCH","BMBL","SNAP",
    "PINS","RDN","MTG","ESNT","NMIH","HASI","LADR","GPMT","RC","ACRE",
    "ARI","BXMT","KREF","MFA","NLY","AGNC","TWO","CIM","IVR","EFC",
    "ORC","ARR","CHMI","MITT","ANH","PMT","NREF","KBWY","MORT",
]

# ── S&P 400 MidCap (sample — most liquid) ────────────────────────────────────
SP400_MIDCAP = [
    "ACHC","ACM","ACLX","AEO","AGCO","AIRC","AIT","AIZ","ALE","ALK",
    "ALLE","AMCX","AMD","AMRC","ANF","ANIK","APLE","APOG","ARI",
    "ARW","ASGN","ASH","ATO","ATR","AUB","AVT","AWI","BANR","BCC",
    "BCPC","BDC","BFH","BFST","BIG","BJRI","BKH","BLD","BLDR","BMI",
    "BOOT","BOX","BPOP","BR","BRC","BRKR","BRX","BSY","BTU","BUSE",
    "BWA","CABO","CACI","CALM","CALX","CATY","CBT","CC","CDAY","CDP",
    "CHEF","CHX","CINF","CKH","CLFD","CLH","CLS","CLW",
    "CMC","CNK","CNO","CODI","COIN","COLB","CPK","CRGY","CRI",
    "CRK","CRS","CSL","CTRE","CUBE","CUZ","CVE","CVLT","CVU",
    "CWEN","CWK","CWT","CXM","CXW","DAN","DCOM","DEN","DIOD","DNB",
    "DRH","DRVN","DSP","DVN","DY","EAT","EBC","EGRX","EIGI","ELF",
    "ELS","EME","ENOV","ENSG","EPC","EPRT","ESE","ESRT","ETH",
    "EWBC","EXEL","EXP","EXPI","FAF","FBMS","FBP","FELE","FF",
    "FGEN","FISI","FL","FLGT","FLO","FR","FUL","FULT","GATX","GBX",
    "GCI","GEO","GEOS","GFF","GKOS","GNL","GPRE","GTN","GTY",
    "GVA","HAE","HALO","HBI","HCI","HCSG","HHC","HLX","HMST","HOMB",
    "HOPE","HP","HXL","IBP","IDCC","IIIN","IIIV","IMKTA","INGR",
    "INSP","INSW","IONS","IPAR","IRDM","JBL","JELD","JHG","JJSF","JNPR",
    "JOBY","KAI","KBH","KFY","KLIC","KMT","KNF","KNX","KRC","KRG",
    "LH","LKFN","LNN","LOPE","LPLA","LTC","MATX","MBC","MBWM","MCY",
    "MEC","MGRC","MHO","MLKN","MMSI","MNKD","MNR","MNST","MOG-A","MORN",
    "MPW","MRCY","MSA","MSM","MTH","MTUS","MWA","NBTB","NCR","NDAQ",
    "NEU","NFG","NKTR","NNN","NPO","NPTN","NSA","NTLA","NUS","NVT",
    "NYCB","OFG","OGE","OGN","OII","OKE","OLPX","OMCL","ORI","OSCR",
    "OSK","OTTR","OZK","PATK","PAYO","PDCE","PDM","PEB","PFBC","PFS",
    "PHM","PK","PLXS","PNFP","PNM","POLY","POWL","PPBI","PPBI",
    "PRGO","PRK","PSB","PTC","PTEN","PUMP","PVH","RDNT","REG","REZI",
    "RMBS","RNR","ROIC","RPM","RRX","RUSHA","RXO","SAIA",
    "SAM","SBOW","SCI","SHO","SITE","SIX","SKYW","SLG","SM",
    "SMBC","SMPL","SNEX","SONO","SPB","SPSC","SR","STC","STEL","STLD",
    "STR","STRL","SUN","SUPN","SWX","SXT","TAL","TBBK",
    "TDC","TGNA","THS","TILE","TKR","TMHC","TOWN","TPVG","TRN","TRMK",
    "TRNO","TSCO","TUP","TX","UBSI","UFI","UFPI","UMH","UNFI","UNUM",
    "URBN","USPH","VCEL","VFC","VIRT","VNO","VPG","VRRM","VSCO","VSH",
    "VVV","WAFD","WBS","WDFC","WEN","WERN","WEX","WH","WKC",
    "WOR","WSC","WSR","WTFC","WWW","XNCR","XRX","YOU","ZD","ZI",
]

# ── AEX (Amsterdam) ──────────────────────────────────────────────────────────
AEX = [
    "ASML.AS","HEIA.AS","INGA.AS","PHIA.AS","ADYEN.AS","NN.AS",
    "AKZA.AS","MT.AS","ABN.AS","AGN.AS","RAND.AS",
    "WKL.AS","KPN.AS","BESI.AS","IMCD.AS","AD.AS",
    "GLPG.AS","UMG.AS","WDP.AS","ASRNL.AS","EXO.AS",
]

# ── DAX (Frankfurt) ──────────────────────────────────────────────────────────
DAX = [
    "ADS.DE","AIR.DE","ALV.DE","BAS.DE","BAYN.DE","BMW.DE","BNR.DE",
    "CON.DE","DB1.DE","DBK.DE","DHL.DE","DTE.DE","ENR.DE","EOAN.DE",
    "FRE.DE","HEI.DE","HEN3.DE","IFX.DE","LIN.DE","MBG.DE","MRK.DE",
    "MTX.DE","MUV2.DE","P911.DE","PAH3.DE","PUMA.DE","QIA.DE","RHM.DE",
    "RWE.DE","SAP.DE","SHL.DE","SIE.DE","SRT3.DE","SY1.DE","VNA.DE",
    "VOW3.DE","ZAL.DE","AFX.DE","AIXA.DE","DHER.DE",
]

# ── CAC 40 (Paris) ───────────────────────────────────────────────────────────
CAC40 = [
    "AI.PA","AIR.PA","ALO.PA","ATO.PA","BN.PA","BNP.PA","CA.PA","CAP.PA",
    "CS.PA","DG.PA","DSY.PA","ENGI.PA","EL.PA","ERF.PA","GLE.PA","HO.PA",
    "IMP.PA","KER.PA","LR.PA","MC.PA","ML.PA","OR.PA","ORA.PA","PUB.PA",
    "RI.PA","RMS.PA","SAF.PA","SAN.PA","SGO.PA","STLA.PA","STM.PA",
    "SU.PA","TEP.PA","TFI.PA","TISC.PA","UG.PA","VIE.PA","VIV.PA",
    "WLN.PA","FR.PA",
]

# ── FTSE 100 (London) ────────────────────────────────────────────────────────
FTSE100 = [
    "AAL.L","ABF.L","ADM.L","AHT.L","ANTO.L","AV.L","AZN.L","BA.L",
    "BARC.L","BATS.L","BEZ.L","BKG.L","BLND.L","BLT.L","BNZL.L","BP.L",
    "BRBY.L","BT-A.L","CCH.L","CPG.L","CRDA.L","CRH.L","DCC.L","DGE.L",
    "DLG.L","ECM.L","ENT.L","EXPN.L","EZJ.L","FERG.L","FLTR.L","FLTRF.L",
    "GLEN.L","GSK.L","HL.L","HLMA.L","HMSO.L","HSBA.L","HWDN.L","IAG.L",
    "ICG.L","ICP.L","IHG.L","III.L","IMB.L","INF.L","ITRK.L","JD.L",
    "JMAT.L","KGF.L","LAND.L","LGEN.L","LLOY.L","LMP.L","LSEG.L","MKS.L",
    "MNDI.L","MNG.L","MRO.L","NG.L","NWG.L","NXT.L","OCDO.L","PHNX.L",
    "PSON.L","PSN.L","PSH.L","RB.L","RDSA.L","REL.L","RIO.L","RKT.L",
    "RMV.L","RR.L","RS1.L","SBRY.L","SDR.L","SGE.L","SGRO.L","SHEL.L",
    "SKG.L","SMDS.L","SMIN.L","SMT.L","SN.L","SPX.L","SSE.L","STAN.L",
    "SVT.L","TSCO.L","TW.L","ULVR.L","UU.L","VOD.L","WEIR.L","WPP.L",
    "WTB.L","BDEV.L","ABG.L","ABDN.L",
]

# ── IBEX 35 (Madrid) ────────────────────────────────────────────────────────
IBEX35 = [
    "ACS.MC","ACX.MC","AENA.MC","AMS.MC","ANA.MC","BBVA.MC","BKT.MC",
    "CABK.MC","CIE.MC","COL.MC","ELE.MC","ENC.MC","ENI.MC","FDR.MC",
    "FER.MC","GRF.MC","IAG.MC","IBE.MC","IDR.MC","ICAG.MC","INM.MC",
    "LOG.MC","MAP.MC","MRL.MC","MTI.MC","MTS.MC","NTGY.MC","PHM.MC",
    "REP.MC","ROVI.MC","SAB.MC","SAN.MC","SGRE.MC","SOL.MC","TEF.MC",
]

# ── SMI (Zürich) ─────────────────────────────────────────────────────────────
SMI = [
    "ABBN.SW","ADEN.SW","ALC.SW","BALN.SW","CFR.SW","CSGN.SW","GEBN.SW",
    "GIVN.SW","HOLN.SW","LONN.SW","NESN.SW","NOVN.SW","PGHN.SW","ROG.SW",
    "SCMN.SW","SGSN.SW","SIKA.SW","SLHN.SW","SOON.SW","SRENH.SW","STMN.SW",
    "UBSG.SW","UHRN.SW","VACN.SW","VIFN.SW","ZURN.SW",
]

# ── BEL 20 (Brussel) ────────────────────────────────────────────────────────
BEL20 = [
    "ABI.BR","ACKB.BR","AGS.BR","APAM.BR","ARGX.BR","BPOST.BR","COLR.BR",
    "D8.BR","ELI.BR","GBLB.BR","GBL.BR","IFB.BR","KBC.BR","LOTB.BR",
    "MELE.BR","PROX.BR","SOLB.BR","TESB.BR","UMI.BR","WDP.BR",
]

# ── OMX Stockholm (Sweden) ──────────────────────────────────────────────────
OMX_STOCKHOLM = [
    "ALFA.ST","ASSA-B.ST","ATCO-A.ST","ATCO-B.ST","AXFO.ST","BOL.ST",
    "ELUX-B.ST","ERIC-B.ST","ESSP.ST","GETI-B.ST","HEXA-B.ST","HM-B.ST",
    "INVE-B.ST","KINV-B.ST","LATO-B.ST","NDA-SE.ST","NIBE-B.ST","SCA-B.ST",
    "SEB-A.ST","SECU-B.ST","SKA-B.ST","SKF-B.ST","SWED-A.ST","SWMA.ST",
    "TELE2-B.ST","TLSN.ST","VOLV-B.ST","VOLCAR-B.ST",
]

# ── OMX Helsinki (Finland) ──────────────────────────────────────────────────
OMX_HELSINKI = [
    "ELISA.HE","FORTUM.HE","HUH1V.HE","KEMIRA.HE","KNEBV.HE","METSO.HE",
    "NESTE.HE","NOKIA.HE","ORNBV.HE","OUT1V.HE","SAMPO.HE","STERV.HE",
    "TIETO.HE","TLS1V.HE","UPM.HE","WRT1V.HE",
]

# ── OMX Copenhagen (Denmark) ────────────────────────────────────────────────
OMX_COPENHAGEN = [
    "AMBU-B.CO","CARL-B.CO","CHR.CO","COLO-B.CO","DSV.CO","FLS.CO",
    "GMAB.CO","GN.CO","ISS.CO","MAERSK-A.CO","MAERSK-B.CO","NETC.CO",
    "NFLX.CO","NKT.CO","NOVOB.CO","ORSTED.CO","PNDORA.CO","RBREW.CO",
    "ROCK-B.CO","SIM.CO","SYDB.CO","TOP.CO","TRYG.CO","VWS.CO","ZEAL.CO",
]

# ── PSI (Lissabon) ──────────────────────────────────────────────────────────
PSI = [
    "ALTR.LS","BCP.LS","CTT.LS","EDP.LS","EDPR.LS","ESON.LS","GALP.LS",
    "GPA.LS","JMT.LS","NBA.LS","NOS.LS","NVG.LS","REN.LS","SLBEN.LS",
    "SEM.LS","SGPS.LS","SON.LS","SONAE.LS","TDSA.LS",
]

# ── ATX (Wenen) ─────────────────────────────────────────────────────────────
ATX = [
    "ANDR.VI","AT1.VI","ATS.VI","BAWG.VI","BG.VI","EBS.VI","EVN.VI",
    "FMA.VI","IIA.VI","OMV.VI","POST.VI","RBI.VI","SCO.VI","SPI.VI",
    "STLZF.VI","UQA.VI","VER.VI","VIG.VI","VOE.VI","WIE.VI",
]

# ── MIB (Milan) ─────────────────────────────────────────────────────────────
MIB = [
    "A2A.MI","AMP.MI","ATL.MI","BAMI.MI","BMPS.MI","BPE.MI","BRE.MI",
    "BZU.MI","CPR.MI","DIA.MI","ENEL.MI","ENI.MI","ERG.MI","EXSY.MI",
    "FCA.MI","G.MI","HER.MI","IG.MI","ISP.MI","ITW.MI","LDO.MI","MB.MI",
    "MONC.MI","PST.MI","RACE.MI","REC.MI","SPM.MI","SRG.MI","STM.MI",
    "STLAM.MI","TEN.MI","TIT.MI","TRN.MI","UCG.MI","UNI.MI","WBD.MI",
]

# ── Nasdaq-100 extra (tech focus) ────────────────────────────────────────────
NASDAQ100_EXTRA = [
    "ADSK","ALGN","ALXN","ANSS","ASML","BIDU","BIIB","BMRN",
    "CDNS","CERN","CHKP","CTAS","CTSH","DLTR","DOCU","DXCM","EA","EBAY",
    "EXC","FAST","FISV","FOX","FOXA","GILD","IDXX","ILMN","INCY","IPGP",
    "ISRG","JD","KDP","KHC","KLAC","LBTYA","LBTYK","LOGI","LRCX","MAR",
    "MCHP","MDLZ","MNST","MRNA","MRVL","MTCH","MU","NTES","NVTQ","NXPI",
    "OKTA","PCAR","PTON","PYPL","QCOM","REGN","ROST","SBUX","SGEN","SIRI",
    "SPLK","SWKS","TTWO","TXN","VRSK","VRSN","VRTX","WBA","WDAY","WDC",
    "XRAY","XEL","ZM","ZS",
]

# ── Lightweight name lookup (avoids extra API calls during scan) ────────────
# Only the most commonly hit large caps are mapped; everything else falls
# back to showing the raw ticker, which is still perfectly usable.
TICKER_NAMES = {
    "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "NVIDIA", "AMZN": "Amazon",
    "META": "Meta Platforms", "GOOGL": "Alphabet (A)", "GOOG": "Alphabet (C)",
    "BRK-B": "Berkshire Hathaway", "LLY": "Eli Lilly", "AVGO": "Broadcom",
    "JPM": "JPMorgan Chase", "V": "Visa", "TSLA": "Tesla", "UNH": "UnitedHealth",
    "XOM": "Exxon Mobil", "MA": "Mastercard", "COST": "Costco", "PG": "Procter & Gamble",
    "JNJ": "Johnson & Johnson", "ABBV": "AbbVie", "HD": "Home Depot", "MRK": "Merck",
    "CVX": "Chevron", "CRM": "Salesforce", "BAC": "Bank of America", "NFLX": "Netflix",
    "AMD": "AMD", "KO": "Coca-Cola", "WMT": "Walmart", "PEP": "PepsiCo",
    "TMO": "Thermo Fisher", "ADBE": "Adobe", "ACN": "Accenture", "MCD": "McDonald's",
    "CSCO": "Cisco", "ORCL": "Oracle", "INTC": "Intel", "IBM": "IBM",
    "QCOM": "Qualcomm", "TXN": "Texas Instruments", "NKE": "Nike", "DIS": "Disney",
    "ABT": "Abbott Labs", "WFC": "Wells Fargo", "GS": "Goldman Sachs",
    "MS": "Morgan Stanley", "C": "Citigroup", "UBER": "Uber", "ABNB": "Airbnb",
    "ASML.AS": "ASML", "HEIA.AS": "Heineken", "ADYEN.AS": "Adyen",
    "PHIA.AS": "Philips", "AKZA.AS": "AkzoNobel", "KPN.AS": "KPN",
    "WKL.AS": "Wolters Kluwer", "IMCD.AS": "IMCD", "BESI.AS": "BE Semiconductor",
    "SAP.DE": "SAP", "SIE.DE": "Siemens", "ALV.DE": "Allianz", "BMW.DE": "BMW",
    "VOW3.DE": "Volkswagen", "BAS.DE": "BASF", "BAYN.DE": "Bayer",
    "DTE.DE": "Deutsche Telekom", "MBG.DE": "Mercedes-Benz", "AIR.DE": "Airbus",
    "MC.PA": "LVMH", "OR.PA": "L'Oréal", "SAN.PA": "Sanofi", "TTE.PA": "TotalEnergies",
    "AI.PA": "Air Liquide", "BNP.PA": "BNP Paribas", "SU.PA": "Schneider Electric",
    "AZN.L": "AstraZeneca", "HSBA.L": "HSBC", "SHEL.L": "Shell", "BP.L": "BP",
    "ULVR.L": "Unilever", "GSK.L": "GSK", "RIO.L": "Rio Tinto", "VOD.L": "Vodafone",
    "SAN.MC": "Banco Santander", "BBVA.MC": "BBVA", "IBE.MC": "Iberdrola",
    "TEF.MC": "Telefónica", "ITX.MC": "Inditex",
    "NESN.SW": "Nestlé", "ROG.SW": "Roche", "NOVN.SW": "Novartis", "UBSG.SW": "UBS",
    "ABI.BR": "AB InBev", "ARGX.BR": "argenx", "KBC.BR": "KBC Group",
    "ERIC-B.ST": "Ericsson", "HM-B.ST": "H&M", "VOLV-B.ST": "Volvo",
    "NOKIA.HE": "Nokia", "NESTE.HE": "Neste",
    "NOVOB.CO": "Novo Nordisk", "ORSTED.CO": "Ørsted", "MAERSK-B.CO": "Maersk",
    "ENI.MI": "Eni", "RACE.MI": "Ferrari", "STLAM.MI": "Stellantis",
}

def get_company_name(ticker: str) -> str:
    """Return a friendly company name if known, otherwise the raw ticker."""
    return TICKER_NAMES.get(ticker, ticker)

# ── All-in universe ──────────────────────────────────────────────────────────
def get_universe(exchanges: list[str]) -> list[str]:
    """Return deduplicated list of tickers for the selected exchanges."""
    mapping = {
        "S&P 500":        SP500,
        "S&P 400 MidCap": SP400_MIDCAP,
        "Nasdaq-100":     NASDAQ100_EXTRA,
        "AEX":            AEX,
        "DAX":            DAX,
        "CAC 40":         CAC40,
        "FTSE 100":       FTSE100,
        "IBEX 35":        IBEX35,
        "SMI":            SMI,
        "BEL 20":         BEL20,
        "OMX Stockholm":  OMX_STOCKHOLM,
        "OMX Helsinki":   OMX_HELSINKI,
        "OMX Copenhagen": OMX_COPENHAGEN,
        "PSI":            PSI,
        "ATX":            ATX,
        "MIB":            MIB,
    }
    seen, result = set(), []
    for ex in exchanges:
        for t in mapping.get(ex, []):
            if t not in seen:
                seen.add(t)
                result.append(t)
    return result

ALL_EXCHANGES = [
    "S&P 500", "S&P 400 MidCap", "Nasdaq-100",
    "AEX", "DAX", "CAC 40", "FTSE 100", "IBEX 35",
    "SMI", "BEL 20", "OMX Stockholm", "OMX Helsinki",
    "OMX Copenhagen", "PSI", "ATX", "MIB",
]
