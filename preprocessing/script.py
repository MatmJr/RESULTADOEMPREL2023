import pandas as pd
from io import StringIO    

def createOrdenedMaskedDaset(arquivo, novo_nome:str):
    with open(arquivo, 'r') as file:
        content = file.read()

    # Substitua o '/' por quebras de linha
    content = content.replace(' / ', '\n')

    # Use o StringIO para simular um arquivo e leia o conteúdo como CSV
    notas = pd.read_csv(StringIO(content), sep=',', header=None, names=["Inscricao", "Nome", "Nota 1", "Nota 2", "Nota Final"])

    def mask_middle_names(name):
        words = name.split()
        if len(words) > 2:
            return words[0] + ' ' + '***' + ' ' + words[-1]
        return name
    
    def clean_final_score(value):
        # Se o valor não for uma string, retorne o valor diretamente
        if not isinstance(value, str):
            return value
    
        # Pegando a última parte após o espaço (se houver um espaço) como o valor real da nota
        cleaned_value = value.split()[-1] if " " in value else value
    
        # Removendo pontos extras no final, se houver
        while cleaned_value.endswith('.'):
            cleaned_value = cleaned_value[:-1]
        
        return cleaned_value

    # Aplicando mask_middle_names na coluna "Nome"
    notas['Nome'] = notas['Nome'].str.strip().apply(mask_middle_names)
    
    # Convertendo a coluna "Nota Final" para string e aplicando clean_final_score
    notas['Nota Final'] = notas['Nota Final'].astype(str).apply(clean_final_score).astype(float)

    #ordenar os resultados
    classificacao = notas.sort_values(by='Nota Final', ascending=False).reset_index(drop=True)

    # Salvando o DataFrame em um novo arquivo .txt
    classificacao.to_csv(novo_nome+'.txt', sep=',', index=False)