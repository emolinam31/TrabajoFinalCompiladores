import os
import re


def computar_pr(producciones):
    primero = {no_terminal: set() for no_terminal in producciones}

    while True:
        actualizado = False
        for no_terminal in producciones:
            for produccion in producciones[no_terminal]:
                if produccion == 'epsilon':
                    if 'epsilon' not in primero[no_terminal]:
                        primero[no_terminal].add('epsilon')
                        actualizado = True
                else:
                    for simbolo in produccion:
                        if simbolo in producciones:
                            antes = len(primero[no_terminal])
                            primero[no_terminal].update(primero[simbolo] - {'epsilon'})
                            if len(primero[no_terminal]) > antes:
                                actualizado = True
                            if 'epsilon' not in primero[simbolo]:
                                break
                        else:
                            if simbolo not in primero[no_terminal]:
                                primero[no_terminal].add(simbolo)
                                actualizado = True
                            break
                    else:
                        if 'epsilon' not in primero[no_terminal]:
                            primero[no_terminal].add('epsilon')
                            actualizado = True
        if not actualizado:
            break

    return primero


def computar_sig(producciones, primero):
    siguiente = {no_terminal: set() for no_terminal in producciones}
    simbolo_inicio = next(iter(producciones))
    siguiente[simbolo_inicio].add('$')

    while True:
        actualizado = False
        for no_terminal, reglas in producciones.items():
            for regla in reglas:
                siguiente_temporal = siguiente[no_terminal].copy()
                for i in range(len(regla) - 1, -1, -1):
                    simbolo = regla[i]
                    if simbolo in producciones:
                        anterior = siguiente[simbolo].copy()
                        siguiente[simbolo].update(siguiente_temporal)
                        if siguiente[simbolo] != anterior:
                            actualizado = True
                        if 'epsilon' in primero[simbolo]:
                            siguiente_temporal = siguiente_temporal.union(primero[simbolo] - {'epsilon'})
                        else:
                            siguiente_temporal = primero[simbolo]
                    else:
                        siguiente_temporal = {simbolo}
        if not actualizado:
            break

    return siguiente


def computar_primero_alternas(producciones):
    primero = {no_terminal: set() for no_terminal in producciones}

    while True:
        actualizado = False
        for no_terminal in producciones:
            for produccion in producciones[no_terminal]:
                if produccion == 'epsilon':
                    if 'epsilon' not in primero[no_terminal]:
                        primero[no_terminal].add('epsilon')
                        actualizado = True
                else:
                    # Separa los símbolos considerando los paréntesis como entidades independientes
                    simbolos = re.findall(r'\w+|[()]', produccion)
                    for simbolo in simbolos:
                        if simbolo in producciones:
                            antes = len(primero[no_terminal])
                            primero[no_terminal].update(primero[simbolo] - {'epsilon'})
                            if len(primero[no_terminal]) > antes:
                                actualizado = True
                            if 'epsilon' not in primero[simbolo]:
                                break
                        else:
                            if simbolo not in primero[no_terminal]:
                                primero[no_terminal].add(simbolo)
                                actualizado = True
                            break
                    else:
                        if 'epsilon' not in primero[no_terminal]:
                            primero[no_terminal].add('epsilon')
                            actualizado = True
        if not actualizado:
            break

    return primero


def computar_siguiente_alternas(producciones, primero):
    siguiente = {no_terminal: set() for no_terminal in producciones}
    simbolo_inicio = next(iter(producciones))
    siguiente[simbolo_inicio].add('$')

    while True:
        actualizado = False
        for no_terminal, reglas in producciones.items():
            for regla in reglas:
                siguiente_temporal = siguiente[no_terminal].copy()
                # Separa los símbolos considerando los paréntesis como entidades independientes
                simbolos = re.findall(r'\w+|[()]', regla)
                for i in range(len(simbolos) - 1, -1, -1):
                    simbolo = simbolos[i]
                    if simbolo in producciones:
                        anterior = siguiente[simbolo].copy()
                        siguiente[simbolo].update(siguiente_temporal)
                        if siguiente[simbolo] != anterior:
                            actualizado = True
                        if 'epsilon' in primero[simbolo]:
                            siguiente_temporal = siguiente_temporal.union(primero[simbolo] - {'epsilon'})
                        else:
                            siguiente_temporal = primero[simbolo]
                    else:
                        siguiente_temporal = {simbolo}
        if not actualizado:
            break

    return siguiente


def main():
    entrada = ("C:/Users/Masters pC/Desktop/EAFIT/3 SEMESTRE/Lenguajes Formales y "
               "Compiladores/TrabajoFinal_Compiladores/glcs.in")
    salida = ("C:/Users/Masters pC/Desktop/EAFIT/3 SEMESTRE/Lenguajes Formales y "
              "Compiladores/TrabajoFinal_Compiladores/pr_sig.out")

    if not os.path.exists(entrada):
        print(f"Error: El archivo de entrada {entrada} no existe.")
        return

    try:
        with open(entrada, 'r') as infile:
            casos = int(infile.readline().strip())
            resultados = []

            for caso_numero in range(casos):
                k = int(infile.readline().strip())
                producciones = {}
                for _ in range(k):
                    linea = infile.readline().strip()
                    no_terminal, prod = linea.split('->')
                    no_terminal = no_terminal.strip()
                    alternativas = [alt.strip() for alt in prod.split('|')]
                    producciones[no_terminal] = alternativas

                if all(no_terminal.isupper() for no_terminal in producciones):
                    primero = computar_pr(producciones)
                    siguiente = computar_sig(producciones, primero)
                elif all((len(no_terminal) > 1) for no_terminal in producciones):
                    primero = computar_primero_alternas(producciones)
                    siguiente = computar_siguiente_alternas(producciones, primero)

                resultado = []
                resultado.append(f"{k}")
                for no_terminal in producciones:
                    conjunto_primero = ', '.join(sorted(primero[no_terminal]))
                    resultado.append(f"Pr({no_terminal}) = {{{conjunto_primero}}}")
                for no_terminal in producciones:
                    follow_set = ', '.join(sorted(siguiente[no_terminal]))
                    resultado.append(f"Sig({no_terminal}) = {{{follow_set}}}")
                resultados.append(resultado)

        with open(salida, 'w') as outfile:
            outfile.write(f"{casos}\n")
            for resultado in resultados:
                outfile.write('\n'.join(resultado) + '\n')

        print(f"\nEl archivo de salida se ha generado correctamente en {salida}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
