from enum import Enum


class TODOListStatusEnum(str, Enum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluída"



class ExceptionErrorMsgs(str, Enum):
    TODO_NOT_FOUND = "TODO does not exist."
    NOT_ONE_TODO = "There are no TODOs."