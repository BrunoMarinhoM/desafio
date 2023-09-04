def sugestao(jornada_esperada:list, pontos_realizados:list):
    from copy import deepcopy
    import datetime
    
    jornada_esperada_dir = {'Entradas':{}, 'Intervalos':{}, 'Saidas':{}}

    output = []
    quantidade_esperada = {
        'Entradas' : 0,
        'Intervalos' : 0,
        'Saidas' : 0,
    }

    quantidade_realizada = {
        'Entradas' : 0,
        'Intervalos' : 0,
        'Saidas' : 0,
    }

    definicao = {
        1 : 'Entrada',
        2 : 'Intervalo',
        3 : 'Saída',
    }




    for i in jornada_esperada:
        
        i[1] = datetime.timedelta(hours = int(i[1].split(':')[0]), minutes = int(i[1].split(':')[1]), seconds = int(i[1].split(':')[2])) #formatando a hora de forma a conseguir operar com ela

        if definicao[i[0]] == 'Entrada':
            quantidade_esperada['Entradas'] += 1 #contando a quantidade de Entradas
            jornada_esperada_dir['Entradas'][quantidade_esperada['Entradas']] = i[1] #ordenando as entradas/intervalos/saidas numa estrutura de dado mais útil p esse caso

        elif definicao[i[0]] == 'Intervalo':
            quantidade_esperada['Intervalos'] += 1
            jornada_esperada_dir['Intervalos'][quantidade_esperada['Intervalos']] = i[1]
        elif definicao[i[0]] == 'Saída':
            quantidade_esperada['Saidas'] += 1
            jornada_esperada_dir['Saidas'][quantidade_esperada['Saidas']] = i[1]




    for i in pontos_realizados:

        i[1] = datetime.timedelta(hours = int(i[1].split(':')[0]), minutes = int(i[1].split(':')[1]), seconds = int(i[1].split(':')[2]))

        if definicao[i[0]] == 'Entrada':

            quantidade_realizada['Entradas'] += 1


        elif definicao[i[0]] == 'Intervalo':
            quantidade_realizada['Intervalos'] += 1

        elif definicao[i[0]] == 'Saída':
            quantidade_realizada['Saidas'] += 1

    if quantidade_realizada['Entradas'] == 0 or definicao[pontos_realizados[0][0]] != 'Entrada' :

        #
        if pontos_realizados[0][1] - jornada_esperada[0][1] <= datetime.timedelta(minutes = 45) or len(pontos_realizados) == len(jornada_esperada):

            jornada_sugerida = deepcopy(pontos_realizados) #Nova jornada sugestão para substituir a atual

            jornada_sugerida[0][0] = 1 #muda o primeiro ponto da jornada realizada para uma entrada

            output += [definicao[pontos_realizados[0][0]] + ' às ' + str(pontos_realizados[0][1]) + ' alterar para ' + 'entrada às ' + str(pontos_realizados[0][1])]

        else:
            jornada_sugerida = deepcopy(pontos_realizados)
            jornada_sugerida.insert(0, jornada_esperada[0]) #insere a entrada esperada como entrada
            output += ['Nem uma entrada foi adicionada! Adicionar entrada']


    
    if quantidade_realizada['Saidas'] == 0 or definicao[pontos_realizados[-1][0]] != 'Saída':

        if pontos_realizados[-1][1] - jornada_esperada[-1][1] <= datetime.timedelta(minutes = 45):
            
            jornada_sugerida = deepcopy(pontos_realizados)
            
            jornada_sugerida[-1][0] = 3 #define o último ponto realizado no dia como saída

            output += [definicao[pontos_realizados[-1][0]] + ' às ' + str(pontos_realizados[-1][1]) + ' alterar para ' + 'saída às ' + str(jornada_esperada[-1][1])]

        else:
            jornada_sugerida = deepcopy(pontos_realizados)
            jornada_sugerida += [3, jornada_esperada[-1][1]] #adiciona a saída esperada como saída
            output += ['Nem uma saída foi adicionada! Adicionar saída']




    
    pseudo_intervalos_realizados = [[False, False, []] for i in range(0, quantidade_esperada['Intervalos'])] #define o [tipo, horário, ponto_todo]
    
    intervalo_counter = 0

    for ponto in pontos_realizados:

        if definicao[ponto[0]] == 'Intervalo':
                
            for i in range(0, len(jornada_esperada)):

                param = jornada_esperada[i][1] - ponto[1]
                
                if param <= datetime.timedelta(seconds = -1):
                    param = ponto[1] - jornada_esperada[i][1]
    
                if param <= datetime.timedelta(minutes=40) and definicao[jornada_esperada[i][0]] == 'Intervalo':
                    pseudo_intervalos_realizados[intervalo_counter] = [True, True, ponto]


        else: 
            for i in range(0, len(jornada_esperada)): 
                if ponto[1] - jornada_esperada[i][1] <= datetime.timedelta(minutes = 40) and definicao[jornada_esperada[i][0]] == 'Intervalo':
                    pseudo_intervalos_realizados[intervalo_counter] = [False, True, ponto]
                    
        intervalo_counter += 1

    for intervalo in range(0, len(pseudo_intervalos_realizados)):
    

        if pseudo_intervalos_realizados[intervalo][0] == False and pseudo_intervalos_realizados[intervalo][1] == False:
            output += ['Adicionar intervalo às ' + str(jornada_esperada_dir['Intervalos'][intervalo+1])+ '?']

        elif pseudo_intervalos_realizados[intervalo][0] == False and pseudo_intervalos_realizados[intervalo][1] == True:

            output += ['Substituir ' + definicao[pseudo_intervalos_realizados[intervalo][2][0]] + ' às ' + str(pseudo_intervalos_realizados[intervalo][2][1]) + ' por um intervalo?']

            
    return output

    

jornada_esperada = [
    [1, '07:00:00'],
    [2, '11:00:00'],
    [2, '12:00:00'],
    [3, '17:00:00'],

]

pontos_realizados = [
    [2, '07:13:00'],
    [2, '09:50:00'],
    [2, '10:10:00'],
    [2, '15:00:00'],
    [3, '16:10:00'],
]


print(sugestao(jornada_esperada, pontos_realizados))

    #análisar horaŕios batidos
    #comparar a distancia deles com os horários esperados 
    #e sugerir baseado nisso
