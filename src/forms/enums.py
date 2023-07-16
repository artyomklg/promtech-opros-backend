import enum


class ItemType(str, enum.Enum):
    ChoiceQuestion = 'choiceQuestion'
    MultichoiseQuestion = 'multichoiseQuestion'
    TextQuestion = 'textQuestion'
    LongTextQuestion = 'longTextQuestion'


class Color(str, enum.Enum):
    Red = 'red'
    Orange = '#F48221'
    Yellow = 'Yellow'
    LimeGreen = 'LimeGreen'
    Aqua = 'Aqua'
    MediumBlue = 'MediumBlue'
    DarkOrchid = 'DarkOrchid'
    Black = 'Black'


class Organization(str, enum.Enum):
    OKB = 'okb.jpg'
    PROMTEX = 'promtex.jpg'
    PROMTEXIRK = 'promtexirk.jpg'
    PROMTEXKAZ = 'promtexkaz.jpg'
    ZAVOD = 'zavod.jpg'
    ATOMSPEC = 'atomspec.jpg'
    KAZZAVOD = 'kazzavod.jpg'
    LOGO1 = 'logo1.jpg'
