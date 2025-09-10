# Importe a classe base
from .RegistroBase import RegistroBase

# Importe as classes de cada arquivo
from .Registro_0 import Registro0
from .Registro_8 import Registro8
from .Registro_9 import Registro9
from .Registro_A import RegistroA
from .Registro_B import RegistroB
from .Registro_C import RegistroC
from .Registro_D import RegistroD
from .Registro_E import RegistroE
from .Registro_R import RegistroR


# Exporte as classes para que possam ser importadas diretamente do pacote
__all__ = [
    "RegistroBase",
    "Registro0",
    "Registro8",
    "Registro9",
    "RegistroA",
    "RegistroB",
    "RegistroC",
    "RegistroD",
    "RegistroE",
    "RegistroR",
]
