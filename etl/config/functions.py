import datetime

def verifica_fim_de_semana(date: datetime.date) -> bool:
    # Verifica se o dia é sábado (5) ou domingo (6)
    return date.weekday() >= 5

def verifica_ano_novo(date: datetime.date) -> bool:
    # Verifica se a data é 1º de janeiro
    return date.month == 1 and date.day == 1

def busca_ultimo_dia_util(date: datetime.date) -> datetime.date:
    # Decrementa o dia por 1 (um dia anterior)
    date -= datetime.timedelta(days=1)

    # Verifica se é feriado ou primeiro de Janeiro
    while verifica_fim_de_semana(date) or verifica_ano_novo(date):
        
        # Decrementa o dia por 1 (um dia anterior)
        date -= datetime.timedelta(days=1)
        
    return date

# Exemplo de uso
today = datetime.date.today()  # Obtém a data atual
last_business_day = busca_ultimo_dia_util(today)

print("Último dia útil:", last_business_day)
